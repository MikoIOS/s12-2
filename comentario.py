import json
import os
import boto3
from datetime import datetime

# Inicializar el cliente de S3 fuera del handler para reutilizarlo
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Obtener el nombre del bucket desde las variables de entorno (inyectado por serverless.yml)
    bucket_name = os.environ['INGESTA_BUCKET']

    # Suponiendo que el evento trae el comentario en el body o en un campo específico
    # Aquí adaptas según cómo llegue el dato a tu Lambda
    comentario_data = event.get('body', event)

    # Generar un nombre de archivo único (ej: timestamp + uuid)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    key = f"comentarios/{timestamp}.json"

    # Estrategia Push: Enviar los datos al destino (S3)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(comentario_data).encode('utf-8'),
        ContentType='application/json'
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Comentario guardado en {bucket_name}/{key}')
    }
