import json
import boto3
import time

athena_client = boto3.client('athena')
RESULT_OUTPUT_LOCATION = "s3://weather-raw-data-296066093533-us-east-1-an/athena-results/"

def lambda_handler(event, context):
    if 'question' in event:
        question = event.get('question', '').lower()
    else:
        try:
            body = json.loads(event.get('body', '{}'))
            question = body.get('question', '').lower()
        except:
            question = ""

    sql_query = ""
    if "temperatura" in question and "gdańsk" in question:
        sql_query = "SELECT temp_kelvin FROM weather_db.curated_weather WHERE city = 'Gdańsk' ORDER BY timestamp_unix DESC LIMIT 1;"
    elif "pogoda" in question and "gdańsk" in question:
        sql_query = "SELECT weather_condition FROM weather_db.curated_weather WHERE city = 'Gdańsk' ORDER BY timestamp_unix DESC LIMIT 1;"
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({"answer": "Przepraszam, obsługuję tylko pytania o temperaturę lub pogodę w Gdańsku."})
        }

    try:
        response = athena_client.start_query_execution(
            QueryString=sql_query,
            ResultConfiguration={'OutputLocation': RESULT_OUTPUT_LOCATION}
        )
        query_execution_id = response['QueryExecutionId']
    except Exception as e:
        return {'statusCode': 500, 'body': f"Błąd startu Atheny: {str(e)}"}

    status = 'RUNNING'
    while status in ['RUNNING', 'QUEUED']:
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']
        if status in ['RUNNING', 'QUEUED']:
            time.sleep(1)

    if status != 'SUCCEEDED':
        return {'statusCode': 500, 'body': json.dumps({"error": "Błąd wykonania zapytania SQL w Athena"})}

    results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    rows = results['ResultSet']['Rows']

    answer_text = "Brak danych dla tego zapytania."
    if len(rows) > 1:
        value = rows[1]['Data'][0]['VarCharValue']
        if "temperatura" in question:
            temp_celsius = round(float(value) - 273.15, 1)
            answer_text = f"Obecna temperatura w Gdańsku wynosi {temp_celsius}°C."
        else:
            answer_text = f"Warunki pogodowe w Gdańsku to: {value}."

    response_body = {
        "supported_questions": ["Jaka jest temperatura w Gdańsku?", "Jaka jest pogoda w Gdańsku?"],
        "generated_query": sql_query,
        "answer": answer_text
    }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response_body, ensure_ascii=False)
    }
