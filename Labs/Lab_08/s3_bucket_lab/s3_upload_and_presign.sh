#!/bin/bash

# exit if any command fails
set -e

# check input arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <local_file> <bucket_name> <expiration_seconds>"
    exit 1
fi

# assign variables
LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=$3
OBJECT_NAME=$(basename "$LOCAL_FILE")

# upload file to S3
echo "Uploading '$LOCAL_FILE' to bucket '$BUCKET_NAME'..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/$OBJECT_NAME" --acl private
echo "Upload complete."

# generate a pre-signed URL
echo "Generating pre-signed URL (expires in $EXPIRATION seconds)..."
PRESIGNED_URL=$(aws s3 presign "s3://$BUCKET_NAME/$OBJECT_NAME" --expires-in "$EXPIRATION")

# output the url
echo "Pre-signed URL:"
echo "$PRESIGNED_URL"
