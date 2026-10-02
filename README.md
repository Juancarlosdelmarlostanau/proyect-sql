# Qué factores se asocian a la felicidad de un país: PIB e infraestructura básica

## Objetivo
Analizar si la riqueza (PIB per cápita) y el acceso a electricidad y agua
se relacionan con el nivel de felicidad de los países, para identificar
qué factores merece la pena priorizar en políticas de desarrollo.

## Contexto del negocio
Un organismo de cooperación con el banco mundial que busca hacer un analisis sobre la poblacion que tiene una mayor persepcion de la felicidad

## Dataset
- World Happiness Report (CSV): 140 países, ranking, happiness score,
  apoyo social, libertad, generosidad y percepción de corrupción.
- API del Banco Mundial (2024): PIB per cápita, acceso a electricidad
  y acceso a agua.
- Base de datos MySQL con 5 tablas: `pais`, `ranking`, `social`,
  `pib_bm`, `infraestructura` (clave: `id_pais`).

## Calidad del dato
- 17 países sin código ISO tras el cruce de datos (nombres no coincidentes).
- Argelia venía en español y con la región mal asignada.
- La API incluye agregados (p. ej. "World") que no son países; se filtraron.
- No todos los países tienen dato de 2024.

## Preguntas clave
1. ¿Los países más ricos son los más felices?
2. ¿El acceso a electricidad y agua se asocia con el happiness score?
3. ¿Qué pesa más: lo económico o lo social (apoyo, libertad)?

## Proceso de análisis
Limpieza en Python (pandas), corrección de códigos, carga a MySQL con
SQLAlchemy, consultas SQL con JOIN entre tablas y análisis exploratorio.

## Resultados / Insights
*Existe una relación entre desarrollo y felicidad. Las regiones con mayor desarrollo económico y social suelen ser también las que reportan mayor bienestar percibido.
*El apoyo social es un factor clave. Acompaña de cerca a la felicidad, mientras que otros indicadores, como la percepción de corrupción, distinguen menos entre regiones.
*El acceso a servicios básicos marca diferencias. Las regiones con menor acceso a electricidad y agua se encuentran entre las menos felices, y el acceso al agua es el déficit más extendido.
*Las regiones no son homogéneas. Hay desigualdades importantes dentro de ellas, por lo que el promedio regional no basta para describir la situación de cada país.
*Los extremos se concentran geográficamente. Los países más y menos felices pertenecen a muy pocas regiones, lo que refleja una fuerte desigualdad global.

## Recomendaciones
Buscar analisar mas datos para tener un estudio mas robusto, buscar como la educacion o la salud.

## Limitaciones
Correlación no es causalidad; un solo año; países sin dato;
el score es autodeclarado y subjetivo.

## Próximos pasos
Añadir series de varios años, más indicadores (salud, educación)
y un dashboard.

## Cómo replicar
Enlace al repositorio: `cleaning.py`, notebook y script SQL del esquema.