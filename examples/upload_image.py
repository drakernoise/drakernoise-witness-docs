import boto3
from botocore.client import Config
import os

# Configuration
ENDPOINT = 'https://images.drakernoise.com'
ACCESS_KEY = 'YOUR_ACCESS_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
BUCKET_NAME = 'public-assets'

def upload_image(file_path):
    s3 = boto3.client('s3',
        endpoint_url=ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    file_name = os.path.basename(file_path)
    
    try:
        # Upload file
        s3.upload_file(file_path, BUCKET_NAME, file_name)
        
        # Generate Public URL
        url = f"{ENDPOINT}/{BUCKET_NAME}/{file_name}"
        print(f"Successfully uploaded: {url}")
        return url
        
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

if __name__ == "__main__":
    upload_image("test_image.jpg")
