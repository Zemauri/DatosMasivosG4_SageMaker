import boto3
from datetime import datetime

# Inicializar el cliente de DynamoDB en la región us-east-1
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Conectar a la tabla existente Results_Dataset
table = dynamodb.Table('Results_Dataset')

# Preparar todos los resultados del análisis para guardar en DynamoDB
# Cada diccionario contiene un par de 'Resultado' (la pregunta/descripción) y 'valor' (la respuesta)
results_to_save = [
    {
        'Resultado': f"La categoría con mayores ingresos es '{top_categoria}' con un total de",
        'valor': f"${max_ventas:,.2f}"
    },
    {
        'Resultado': f"El ticket promedio en la categoría {top_categoria} es de",
        'valor': f"${promedio_top:,.2f}"
    },
    {
        'Resultado': "La edad promedio de los clientes es de",
        'valor': f"{edad_promedio:.2f} años"
    },
    {
        'Resultado': "La mediana de edad es de",
        'valor': f"{edad_mediana:.2f} años"
    },
    {
        'Resultado': "El rango de edad va desde",
        'valor': f"{edad_min} hasta {edad_max} años"
    },
    {
        'Resultado': "El promedio de ventas diarias es de",
        'valor': f"${promedio_diario:,.2f}"
    },
    {
        'Resultado': f"El valor máximo de ventas se registró el {max_dia} con",
        'valor': f"${max_valor:,.2f}"
    },
    {
        'Resultado': f"El valor mínimo de ventas se registró el {min_dia} con",
        'valor': f"${min_valor:,.2f}"
    },
    {
        'Resultado': "La diferencia entre el valor máximo y mínimo de ventas diarias es de",
        'valor': f"${max_valor - min_valor:,.2f}"
    },
    {
        'Resultado': "Total de registros analizados",
        'valor': f"{len(df):,}"
    }
]

# Obtener la marca de tiempo actual en formato ISO para identificar cuándo se guardaron los datos
timestamp = datetime.now().isoformat()

# Contador para llevar registro de cuántos items se han guardado exitosamente
saved_count = 0

# Iterar sobre cada resultado y guardarlo en DynamoDB
for result in results_to_save:
    # Crear un item con los atributos requeridos: Resultado, valor y timestamp
    item = {
        'Resultado': result['Resultado'],  # Atributo String: La pregunta o descripción
        'valor': result['valor'],          # Atributo String: El valor o respuesta
        'timestamp': timestamp             # Marca de tiempo para identificar cuándo se guardó
    }
    
    # Insertar el item en la tabla de DynamoDB
    table.put_item(Item=item)
    
    # Incrementar el contador de items guardados
    saved_count += 1
    
    # Imprimir confirmación de que el item fue guardado exitosamente
    print(f"✓ Guardado: {result['Resultado']} → {result['valor']}")

# Imprimir resumen final con el total de resultados guardados y la marca de tiempo
print(f"\n{saved_count} resultados guardados exitosamente en la tabla Results_Dataset")
print(f"Timestamp: {timestamp}")