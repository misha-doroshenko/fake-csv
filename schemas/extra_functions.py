import csv
import io
import random

import boto3
from botocore.config import Config
from django.core.files.storage import default_storage
from faker import Faker

from fake_csv.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from schemas.models import FileCSV, Column


def full_name_generate(rows: int) -> list:
    fake = Faker()
    full_names = []

    for i in range(rows):
        full_names.append(fake.name())

    return full_names


def job_generate(rows: int) -> list:
    fake = Faker()
    jobs = []

    for i in range(rows):
        jobs.append(fake.job())

    return jobs


def email_generate(rows: int) -> list:
    fake = Faker()
    emails = []

    for i in range(rows):
        emails.append(fake.unique.email())

    return emails


def phone_number_generate(rows: int) -> list:
    fake = Faker()
    phone_numbers = []

    for i in range(rows):
        phone_numbers.append(fake.unique.phone_number())

    return phone_numbers


def company_generate(rows: int) -> list:
    fake = Faker()
    companies = []

    for i in range(rows):
        companies.append(fake.company())

    return companies


def address_generate(rows: int) -> list:
    fake = Faker()
    addresses = []

    for i in range(rows):
        addresses.append(fake.address())

    return addresses


def date_generate(rows: int) -> list:
    fake = Faker()
    dates = []

    for i in range(rows):
        dates.append(fake.date_time())

    return dates


def integer_generate(rows: int, min_val: int, max_val: int) -> list:
    integers = []

    for i in range(rows):
        integers.append(random.randint(min_val, max_val))

    return integers


def generate_data(types: list, rows: int) -> list:
    data = []
    for instance in types:
        if instance.type == "FN":
            data.append(full_name_generate(rows))
        if instance.type == "PN":
            data.append(phone_number_generate(rows))
        if instance.type == "Job":
            data.append(job_generate(rows))
        if instance.type == "Email":
            data.append(email_generate(rows))
        if instance.type == "CN":
            data.append(company_generate(rows))
        if instance.type == "Address":
            data.append(address_generate(rows))
        if instance.type == "Date":
            data.append(date_generate(rows))
        if instance.type == "Int":
            if instance.min_int and instance.max_int:
                data.append(
                    integer_generate(
                        rows, instance.min_int, instance.max_int
                    )
                )
            else:
                data.append(
                    integer_generate(
                        rows, 0, 100
                    )
                )

    return data


def generate_presigned_url(file_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='eu-north-1'
    )
    bucket_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": "fakecsv-files",
            "Key": file_name
        },
        ExpiresIn=3600
    )

    return bucket_url


def create_save_csv(data, file_name, column_separator, string_character):
    s = io.StringIO()
    csv.writer(
        s, quoting=csv.QUOTE_NONNUMERIC,
        delimiter=column_separator,
        quotechar=string_character
    ).writerows(data)
    s.seek(0)

    buf = io.BytesIO()

    buf.write(s.getvalue().encode())
    buf.seek(0)

    default_storage.save(file_name, buf)  # saving csv file to s3 bucket


def fill_data(pk: int, rows: int) -> list:
    column_names = list(Column.objects.filter(schema_id=pk).only("name"))
    types = list(Column.objects.filter(schema_id=pk).only("type", "min_int", "max_int"))

    data = generate_data(types, rows)
    result = []

    for i in range(rows):
        l_temp = []
        for li in data:
            l_temp.append(li[i])
        result.append(l_temp)
    result.insert(0, [column.name for column in column_names])

    return result
