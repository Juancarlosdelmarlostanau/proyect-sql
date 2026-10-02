import pandas as pd
from sqlalchemy import text

## Vaciar las tablas antes de cargar (primero las hijas, al final la padre)
def vaciar_tablas(engine, tablas=("infraestructura", "pib_bm", "social", "ranking", "pais")):
    with engine.begin() as conexion:
        for tabla in tablas:
            conexion.execute(text(f"DELETE FROM {tabla}"))

## Insertar datos a la tabla pais
def cargar_pais(df, engine):
    df_pais = (
        df[["id_pais", "country", "regional indicator"]]
        .rename(columns={"regional indicator": "regional_indicator"})
        .drop_duplicates(subset="id_pais")
    )
    df_pais.to_sql("pais", con=engine, if_exists="append", index=False)
    return df_pais

## Insertar datos a la tabla ranking
def cargar_ranking(df, engine):
    df_ranking = df[["id_pais", "ranking", "ladder score"]].rename(columns={
        "ladder score": "happiness_score"
    })
    df_ranking.to_sql("ranking", con=engine, if_exists="append", index=False)
    return df_ranking

## Insertar datos a la tabla social
def cargar_social(df, engine):
    df_social = df[["id_pais", "social support", "freedom to make life choices",
                    "generosity", "perceptions of corruption"]].rename(columns={
        "social support": "social_support",
        "freedom to make life choices": "freedom_to_make_life_choices",
        "perceptions of corruption": "perceptions_of_corruption"
    })
    df_social.to_sql("social", con=engine, if_exists="append", index=False)
    return df_social

## Insertar datos a la tabla infraestructura
def cargar_infraestructura(df_infra, ids_pais, engine):
    df_infra = df_infra[df_infra["id_pais"].isin(ids_pais["id_pais"])]
    df_infra.to_sql("infraestructura", con=engine, if_exists="append", index=False)
    return df_infra


## Limpiar electrica
def limpiar_respuesta_api(api):
    datos_json = api.json()
    registros = datos_json[1]
    df = pd.DataFrame(registros)

    df['country_id'] = df['country'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
    df['country_value'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else None)

    df = df.drop(columns=['indicator', 'country', 'obs_status', 'decimal'])
    columnas_ordenadas = ['country_id', 'country_value', 'date', 'value']
    df = df[columnas_ordenadas]
    df = df.rename(columns={
        'country_id': 'id_pais',
        'country_value': 'pais',
        'date': 'año',
        'value': 'gdp_per_capita'})
    
    df = df[df['año'].astype(str) == '2024']
    df = df.drop(columns=['año'])
    df = df.sort_values(by='gdp_per_capita', ascending=False)
    return df

df_pib_2024 = limpiar_respuesta_api(api)
