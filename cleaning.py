import pandas as pd

## cambiar de nombre la columna en df2024

def renombrar_columna(df, columna_antigua, columna_nueva):
    df = df.rename(columns={columna_antigua: columna_nueva})
    return df

## Rendondear de 5 a 2 decimales

def redondear_floats(df, decimales=2):
    df = df.copy()
    cols = df.select_dtypes(include="float").columns
    df[cols] = df[cols].round(decimales)
    return df

## Limpiar la respuesta de la para agregar el gdp

def limpiar_respuesta_api(api):
    datos_json = api.json()
    registros = datos_json[1]
    df = pd.DataFrame(registros)

    df['country_id'] = df['country'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
    df['country_value'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else None)

    df = df.drop(columns=['indicator', 'country', 'obs_status', 'decimal'])
    df = df[['country_id', 'country_value', 'date', 'value']]
    df = df.rename(columns={
        'country_id': 'id_pais',
        'country_value': 'pais',
        'date': 'año',
        'value': 'gdp_per_capita'})

    df = df[df['año'].astype(str) == '2024']
    df = df.drop(columns=['año'])
    df = df.sort_values(by='gdp_per_capita', ascending=False)
    return df

## Limpieza de api para la info electrica

def limpiar_inf_electrica(inf_electrica):
    datos_json = inf_electrica.json()
    registros = datos_json[1]
    df = pd.DataFrame(registros)

    df['country_id'] = df['country'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
    df['country_value'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else None)

    df = df.drop(columns=['indicator', 'country', 'obs_status', 'decimal', 'unit'])
    df = df[['country_id', 'country_value', 'date', 'value']]
    df = df.rename(columns={
        'country_id': 'id_pais',
        'country_value': 'pais',
        'date': 'año',
        'value': 'Acceso_inf_elect'})

    df = df[df['año'].astype(str) == '2024']
    df = df.drop(columns=['año'])
    df = df.sort_values(by='Acceso_inf_elect', ascending=False)
    return df

## Limpieza de la api para el agua
def limpiar_inf_agua(inf_agua):
    datos_json = inf_agua.json()
    registros = datos_json[1]
    df = pd.DataFrame(registros)

    df['country_id'] = df['country'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
    df['country_value'] = df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else None)

    df = df.drop(columns=['indicator', 'country', 'obs_status', 'decimal', 'unit'])
    df = df[['country_id', 'country_value', 'date', 'value']]
    df = df.rename(columns={
        'country_id': 'id_pais',
        'country_value': 'pais',
        'date': 'año',
        'value': 'Acceso_inf_agua'})

    df = df[df['año'].astype(str) == '2024']
    df = df.drop(columns=['año'])
    df = df.sort_values(by='Acceso_inf_agua', ascending=False)
    return df


## Insertar datos a la base de datos a la columna de pais
def cargar_pais(df, engine):
    df_pais = df[["id_pais", "country", "regional indicator"]].rename(columns={
        "regional indicator": "regional_indicator"
    })
    df_pais.to_sql("pais", con=engine, if_exists="append", index=False)
    return df_pais

## Insertar datos a la base de datos a la columna de ranking
def cargar_ranking(df, engine):
    df_ranking = df[["id_pais", "ranking", "ladder score"]].rename(columns={
        "ladder score": "happiness_score"
    })
    df_ranking.to_sql("ranking", con=engine, if_exists="append", index=False)
    return df_ranking

## Insertar datos a la base de la columna social
def cargar_social(df, engine):
    df_social = df[["id_pais", "social support", "freedom to make life choices",
                    "generosity", "perceptions of corruption"]].rename(columns={
        "social support": "social_support",
        "freedom to make life choices": "freedom_to_make_life_choices",
        "perceptions of corruption": "perceptions_of_corruption"
    })
    df_social.to_sql("social", con=engine, if_exists="append", index=False)
    return df_social

## Insertar datos a la base de la columna infraestructura
def cargar_infraestructura(df_infra, ids_pais, engine):
    df_infra = df_infra[df_infra["id_pais"].isin(ids_pais["id_pais"])]
    df_infra.to_sql("infraestructura", con=engine, if_exists="append", index=False)
    return df_infra
