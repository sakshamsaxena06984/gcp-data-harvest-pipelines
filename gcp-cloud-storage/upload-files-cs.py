from google.cloud import storage


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} upload to {destination_blob_name} in {bucket_name}")
    except Exception as err:
        print(f"Failed to upload the file over Cloud-Storage due to : {err}")
