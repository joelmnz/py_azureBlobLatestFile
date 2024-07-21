from flask import Flask, render_template
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

def get_most_recent_file_datetime():
    connection_string = os.getenv('AZURE_CONNECTION_STRING')
    container_name = os.getenv('AZURE_CONTAINER_NAME')
    consider_old_after_hrs = int(os.getenv('CONSIDER_OLD_AFTER_HRS', 24))

    if not connection_string or not container_name:
        print("Azure connection string or container name is not set.")
        return None
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
        return None
    except ResourceNotFoundError:
        print(f"Container '{container_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

@app.route('/')
def dashboard():
    most_recent_date, is_old = get_most_recent_file_datetime()
    return render_template('index.html', most_recent_date=most_recent_date, is_old=is_old)

if __name__ == '__main__':
    app.run(debug=True)
