import json
import urllib.request
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    api_key = "***"
    city = "Gdansk"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    bucket_name = "weather-raw-data-296066093533-us-east-1-an"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        return {"statusCode": 500, "body": f"Blad pobierania z API: {str(e)}"}
        
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"weather_{city}_{timestamp}.json"
    
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data)
        )
    except Exception as e:
        return {"statusCode": 500, "body": f"Blad zapisu do S3: {str(e)}"}
        
    return {
        'statusCode': 200,
        'body': f'Zapisano plik {file_name} do S3!'
    }
