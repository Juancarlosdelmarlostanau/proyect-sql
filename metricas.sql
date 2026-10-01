-- METRICAS
USE proyectomysql;

CREATE OR REPLACE VIEW v_analisis AS
SELECT p.id_pais, p.country, p.regional_indicator,
       r.ranking, r.happiness_score,
       b.pib,
       s.social_support, s.freedom_to_make_life_choices,
       s.generosity, s.perceptions_of_corruption,
       i.acceso_electrico, i.acceso_agua
FROM pais p
LEFT JOIN ranking         r ON r.id_pais = p.id_pais
LEFT JOIN pib_bm          b ON b.id_pais = p.id_pais
LEFT JOIN social          s ON s.id_pais = p.id_pais
LEFT JOIN infraestructura i ON i.id_pais = p.id_pais;

-- 1.PROMEDIO DE PERCEPCION DE FELICIDAD POR REGION ....0 A 10
-- Calcula la felicidad promedio de los países de cada región y la ordena de mayor a menor. Resume el nivel típico de felicidad de cada región y permite ver cuáles están por encima o por debajo del resto. También muestra cuántos países tiene cada región, para saber qué tan confiable es el promedio.
SELECT p.regional_indicator,
       COUNT(*) AS n_paises,
       ROUND(AVG(r.happiness_score), 1) AS promedio_felicidad
FROM pais p
INNER JOIN ranking r ON p.id_pais = r.id_pais
GROUP BY p.regional_indicator
ORDER BY promedio_felicidad DESC;

-- 2. RANKING DE REGIONES SEGUNLOS PROMEDIOS DE REGION, PIB, APOYO SOCIAL, CORRUPCION
-- Cada una promedia la variable por región y ordena de mayor a menor, así que la primera fila es el puesto 1. Sirve para ver si las regiones que lideran en una dimensión lideran también en las otras. En corrupción, el puesto 1 es la región con más percepción de corrupción, si en tus datos "más alto" significa "más corrupto".
SELECT p.regional_indicator,
       ROUND(AVG(f.promedio_felicidad), 1) AS promedio_felicidad,
       ROUND(AVG(b.promedio_pib), 1) AS promedio_pib,
       ROUND(AVG(s.promedio_apoyo), 1)*10 AS promedio_apoyo_social,
       ROUND(AVG(s.promedio_corrupcion), 1)*10 AS promedio_corrupcion
FROM pais p
LEFT JOIN(SELECT id_pais, AVG(happiness_score) AS promedio_felicidad
FROM ranking
GROUP BY id_pais) f ON p.id_pais = f.id_pais

LEFT JOIN (SELECT id_pais, AVG(pib) AS promedio_pib
FROM pib_bm 
GROUP BY id_pais) b  ON p.id_pais = b.id_pais

LEFT JOIN (SELECT id_pais, 
        AVG(social_support) AS promedio_apoyo,
        AVG(perceptions_of_corruption) AS promedio_corrupcion
FROM social s
GROUP BY id_pais) s  ON p.id_pais = s.id_pais
GROUP BY p.regional_indicator
ORDER BY promedio_felicidad DESC;

-- 3 VALORES MAXIMO, MINIMO Y BRECHA POR REGION
SELECT p.regional_indicator,
       ROUND(MAX(r.happiness_score), 1)                          AS mejor_score,
       ROUND(MIN(r.happiness_score), 1)                          AS peor_score,
       ROUND(MAX(r.happiness_score) - MIN(r.happiness_score), 1) AS brecha
FROM pais p
INNER JOIN ranking r ON p.id_pais = r.id_pais
GROUP BY p.regional_indicator
ORDER BY brecha DESC;

-- 4 PORCENTAJE DE PAISES CON acceso ELECTRICO Y ACCESO DE AGUA MENOR A 90
-- AQUI LOS CEROS SON PORQUE NO  HAY VALORES MENORES DE 90 EN ESAS REGIONES
SELECT p.regional_indicator,
       ROUND(100 * SUM(CASE WHEN i.acceso_electrico < 90 THEN 1 ELSE 0 END) / COUNT(*), 1)
            AS pct_electricidad_menor_90,
       ROUND(100 * SUM(CASE WHEN i.acceso_agua < 90 THEN 1 ELSE 0 END) / COUNT(*), 1)
            AS pct_agua_menor_90,
       ROUND(100 * SUM(CASE WHEN i.acceso_electrico < 90 OR i.acceso_agua < 70 THEN 1 ELSE 0 END) / COUNT(*), 1)
            AS pct_alguno_menor_90
FROM pais p
INNER JOIN infraestructura i ON p.id_pais = i.id_pais
WHERE i.acceso_electrico IS NOT NULL
  AND i.acceso_agua IS NOT NULL
GROUP BY p.regional_indicator
ORDER BY pct_alguno_menor_90 DESC;


-- 5. BRECHA DE INFRAESTRUCTURA POR PAIS(acceso_electrico - acceso_agua)
-- lista los países concretos de cada grupo.
SELECT p.country, p.regional_indicator,
       i.acceso_electrico, i.acceso_agua,
       ROUND(i.acceso_electrico - i.acceso_agua, 3)      AS brecha,
       CASE WHEN i.acceso_electrico > i.acceso_agua THEN 'Mas electricidad que agua'
            WHEN i.acceso_electrico < i.acceso_agua THEN 'Mas agua que electricidad'
            ELSE 'Equilibrado' END                       AS tipo_desbalance
FROM pais p
INNER JOIN infraestructura i ON p.id_pais = i.id_pais
WHERE i.acceso_electrico IS NOT NULL
  AND i.acceso_agua IS NOT NULL
ORDER BY brecha DESC;



-- 6.Detalle: los paises que forman cada extremo top 10 y bottom 10
SELECT 'Top 10' AS grupo, r.ranking, p.country, p.regional_indicator, r.happiness_score
FROM pais p
INNER JOIN ranking r ON p.id_pais = r.id_pais
WHERE r.ranking <= 10
ORDER BY ranking;

SELECT 'Bottom 10' AS grupo, r.ranking, p.country, p.regional_indicator, r.happiness_score
FROM pais p
INNER JOIN ranking r ON p.id_pais = r.id_pais
WHERE r.ranking > (SELECT MAX(ranking) FROM ranking) - 10
ORDER BY ranking;



























