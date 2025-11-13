import boto3
import requests
import os

# configuration

bucket = 'ds2002-f25-apy8af'
expiration_seconds = 604800 # 7 days
url_to_fetch = 'https://cdna.artstation.com/p/assets/images/images/044/335/198/original/kenny-mays-piplup-3.gif?1639695051'  # example gif
local_file = 'downloaded.gif' # local filename to save

# 1. download file from the internet

print(f"Fetching file from {url_to_fetch}...")
response = requests.get(url_to_fetch)
response.raise_for_status()  # raises an error if the download failed

with open(local_file, 'wb') as f:
    f.write(response.content)

print(f"File saved locally as {local_file}")

# 2. upload to S3

s3 = boto3.client('s3', region_name='us-east-1')
file_key = os.path.basename(local_file)

print(f"Uploading {local_file} to bucket {bucket}...")
with open(local_file, 'rb') as data:
    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=file_key,
        ACL='private'  # keep private, use presigned url
    )

print("Upload complete.")


# 3. generate presigned URL

presigned_url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': bucket, 'Key': file_key},
    ExpiresIn=expiration_seconds
)

print(presigned_url)
