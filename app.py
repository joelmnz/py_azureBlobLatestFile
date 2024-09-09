from flask import Flask, render_template, request
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# Load environment variables
load_dotenv()

def get_most_recent_file_datetime_backblaze():
    access_key_id = os.getenv('BACKBLAZE_ACCESS_KEY_ID')
    secret_access_key = os.getenv('BACKBLAZE_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('BACKBLAZE_BUCKET_NAME')
    consider_old_after_hrs = int(os.getenv('CONSIDER_OLD_AFTER_HRS', 24))

    if not access_key_id or not secret_access_key or not bucket_name:
        print("Backblaze credentials or bucket name is not set.")
        return None, False
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url='https://s3.us-west-002.backblazeb2.com',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            most_recent_object = max(response['Contents'], key=lambda obj: obj['LastModified'])
            now = datetime.now(timezone.utc)
            if (now - most_recent_object['LastModified']).total_seconds() > consider_old_after_hrs * 3600:
                return most_recent_object['LastModified'], True
            return most_recent_object['LastModified'], False
        return None, False
    except (NoCredentialsError, PartialCredentialsError):
        print("Invalid Backblaze credentials.")
        return None, False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, False

def get_most_recent_file_datetime_azure():
    connection_string = os.getenv('AZURE_CONNECTION_STRING')
    container_name = os.getenv('AZURE_CONTAINER_NAME')
    consider_old_after_hrs = int(os.getenv('CONSIDER_OLD_AFTER_HRS', 24))

    if not connection_string or not container_name:
        print("Azure connection string or container name is not set.")
        return None, False
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        # List all blobs and sort them by last_modified
        blobs = list(container_client.list_blobs())
        if blobs:
            most_recent_blob = max(blobs, key=lambda b: b.last_modified)
            now = datetime.now(timezone.utc)
            if (now - most_recent_blob.last_modified).total_seconds() > consider_old_after_hrs * 3600:
                return most_recent_blob.last_modified, True
            return most_recent_blob.last_modified, False
        return None, False
    except ResourceNotFoundError:
        print(f"Container '{container_name}' not found.")
        return None, False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

@app.route('/')
def dashboard():
    storage_type = request.args.get('type', 'az').lower()
    if storage_type == 'az':
        most_recent_date, is_old = get_most_recent_file_datetime_azure()
        provider_name = "Azure Blob Storage"
    elif storage_type == 'bb':
        most_recent_date, is_old = get_most_recent_file_datetime_backblaze()
        provider_name = "Backblaze B2"
    else:
        most_recent_date, is_old = None, False
        provider_name = "Unknown"

    return render_template('index.html', most_recent_date=most_recent_date, is_old=is_old, provider_name=provider_name)

if __name__ == '__main__':
    app.run(debug=True)
