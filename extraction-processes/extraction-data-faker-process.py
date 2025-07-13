from faker import Faker
import random
import string
import csv
from google.cloud import storage


def creation_of_dummy_data():
    num_employees = 100
    fake = Faker()
    employee_data = []
    password_characters = string.ascii_letters + string.digits + 'm'

    for _ in range(num_employees):
        employee = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "job_title": fake.job().split(',')[0],
            "department": fake.job().split(',')[0],
            "email": fake.email(),
            "address": fake.address().split('\n')[0],
            "phone_number": fake.phone_number(),
            "salary": fake.random_number(digits=5),
            "password": ''.join(random.choice(password_characters) for _ in range(8))
        }

        employee_data.append(employee)

    csv_file_name = "/tmp/employee_data.csv"

    with open(csv_file_name, mode='w', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name', 'job_title', 'department', 'email', 'address', 'phone_number',
                      'salary',
                      'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(num_employees):
            writer.writerow({
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "job_title": fake.job().split(',')[0],
                "department": fake.job().split(',')[0],
                "email": fake.email(),
                "address": fake.address().split('\n')[0],
                "phone_number": fake.phone_number(),
                "salary": fake.random_number(digits=5),
                "password": ''.join(random.choice(password_characters) for _ in range(8))
            })


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} upload to {destination_blob_name} in {bucket_name}")


# with open(csv_file_name, mode='r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row)

if __name__ == "__main__":

    print("*************** Started The ETL ***************")
    try:
        creation_of_dummy_data()
        bucket_name = 'bkt-employee-data-uses'
        source_file_name = '/tmp/employee_data.csv'
        destination_blob_name = 'employee_data.csv'
        upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
        print("*************** Job Has Been Completed Successfully ***************")
    except Exception as err:
        print(f"Job Has Failed Due to : {err}")
