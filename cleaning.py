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
