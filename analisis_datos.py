import pandas as pd
import awswrangler as wr

path = "s3://datosmasivos-g4-dataset/processed/"
cols = ["product_category", "total_sales", "age", "transaction_date", "churned"]

df = wr.s3.read_parquet(path=path, columns=cols)
print(f" Analizando {len(df):,} registros del S3.\n")

analisis_ventas = (
    df.groupby('product_category')['total_sales']
    .agg(['sum', 'mean'])
    .sort_values(by='sum', ascending=False)
)

top_categoria = analisis_ventas.index[0]
max_ventas = analisis_ventas['sum'].iloc[0]
promedio_top = analisis_ventas['mean'].iloc[0]

print("\nANÁLISIS DE CATEGORÍAS")
print(f"La categoría con mayores ingresos es '{top_categoria}' con un total de ${max_ventas:,.2f}.")
print(f"El ticket promedio en esta categoría es de ${promedio_top:,.2f}.")

edad_promedio = df['age'].mean()
edad_min = df['age'].min()
edad_max = df['age'].max()
edad_mediana = df['age'].median()

print("\nANÁLISIS DEMOGRÁFICO")
print(f"La edad promedio de los clientes es de {edad_promedio:.2f} años.")
print(f"La mediana de edad es de {edad_mediana:.2f} años.")
print(f"El rango de edad va desde {edad_min} hasta {edad_max} años.")

df['transaction_date'] = pd.to_datetime(df['transaction_date'])

ventas_diarias = (
    df.groupby(df['transaction_date'].dt.date)['total_sales']
    .sum()
)

promedio_diario = ventas_diarias.mean()
max_dia = ventas_diarias.idxmax()
max_valor = ventas_diarias.max()
min_dia = ventas_diarias.idxmin()
min_valor = ventas_diarias.min()

print("\nANÁLISIS DE TENDENCIAS")
print(f"El promedio de ventas diarias es de ${promedio_diario:,.2f}.")
print(f"El valor máximo de ventas se registró el {max_dia} con ${max_valor:,.2f}.")
print(f"El valor mínimo de ventas se registró el {min_dia} con ${min_valor:,.2f}.")
print(f"La diferencia entre el valor máximo y mínimo de ventas diarias es de ${max_valor - min_valor:,.2f}.")
