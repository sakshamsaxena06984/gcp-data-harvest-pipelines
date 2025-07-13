import requests
import csv
from google.cloud import storage
import os


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} upload to {destination_blob_name} in {bucket_name}")


def getting_test_match_ranking_api_call():
    api_key = os.getenv('RAPIDAPI_KEY')
    api_host = os.getenv('RAPIDAPI_HOST')
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"
    querystring = {"formatType": "test"}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json().get('rank', [])
        csv_filename = '/tmp/batsmen_ranking.csv'

        if data:
            field_name = ['rank', 'name', 'country']

            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_name)
                for entry in data:
                    writer.writerow({field: entry.get(field) for field in field_name})

            print(f"Data fetched successfully and written to {csv_filename}")
            try:
                bucket_name = 'bkt-ranking-data-uses'
                destination_blob_name = f'{csv_filename}'
                upload_to_gcs(bucket_name, csv_filename, destination_blob_name)
            except Exception as err:
                print(f"Failed to upload file into gcs cloud storage due to : {err}")

        else:
            print("No data available from the API")

    else:
        print("Failed to fetch data : ", response.status_code)


if __name__ == "__main__":
    print("*************** Started The Test Players Ranking ***************")
    try:
        getting_test_match_ranking_api_call()
        print("*************** Job Has Been Completed Successfully (Test Players Ranking) ***************")
    except Exception as err:
        print(f"Job (Test Players Ranking) Has Failed Due to : {err}")
