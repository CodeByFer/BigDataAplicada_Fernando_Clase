import pandas as pd

# 1. Cargar CSV desde capa Bronce
df = pd.read_csv("csv/Datos_2022/Calificaciones.csv", sep=",")

print(df)

#1.1 Nombre de los campos para evitar errores
nota="nota_numerica"
curso="curso"
modulo="contenido"
# 2. Transformación 1: Limpieza
df = df.dropna(subset=[nota])

# 3. Transformación 2: Validación de calidad
df[nota] = pd.to_numeric(df[nota], errors="coerce")
df = df[(df[nota] >= 0) & (df[nota] <= 10)]

# 4. Agregación para Capa Oro
df_gold = (
    df.groupby([curso, modulo])
      .agg(
          nota_media=(nota, "mean"),
          total_alumnos=(nota, "count")
      )
      .reset_index()
)

# 5. Escritura en formato Parquet
df_gold.to_parquet(
    "calificaciones_oro.parquet",
    engine="pyarrow",
    index=False
)
