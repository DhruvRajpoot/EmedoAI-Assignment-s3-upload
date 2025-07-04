import boto3
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename='s3_upload.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


def check_file_conflict(s3_client, bucket, file_name):
    """Check if file exists in S3 and return new name if conflict exists."""
    try:
        s3_client.head_object(Bucket=bucket, Key=file_name)
        name, ext = os.path.splitext(file_name)
        new_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        logger.info(f"Conflict: {file_name} -> {new_name}")
        return new_name
    except:
        return file_name


def upload_file(s3_client, file_path, bucket):
    """Upload one file to S3."""
    logger.info(f"Uploading: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False

    try:
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > 100:
            logger.warning(f"File too large: {size_mb:.2f} MB")
            return False
    except Exception as e:
        logger.error(f"Size check failed: {e}")
        return False

    file_name = os.path.basename(file_path)
    file_name = check_file_conflict(s3_client, bucket, file_name)

    try:
        s3_client.upload_file(file_path, bucket, file_name)
        logger.info(f"SUCCESS: {file_path} -> s3://{bucket}/{file_name}")
        return True
    except Exception as e:
        logger.error(f"FAILED: {file_path} - {str(e)}")
        return False


def upload_files_to_s3(file_list):
    """Upload multiple files to S3 with comprehensive logging."""
    logger.info("=" * 50)
    logger.info(f"S3 UPLOAD STARTED - {len(file_list)} files")
    logger.info("=" * 50)

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")
    bucket_name = os.getenv("AWS_BUCKET_NAME")

    if not aws_access_key or not aws_secret_key or not aws_region:
        logger.error("Missing AWS credentials")
        return False
    
    logger.info(f"AWS credentials loaded")

    try:
        s3_client = boto3.client('s3', 
                                aws_access_key_id=aws_access_key,
                                aws_secret_access_key=aws_secret_key,
                                region_name=aws_region)
        logger.info("Connected to S3")
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False

    success_count = 0
    failed_count = 0
    
    for i, file_path in enumerate(file_list, 1):
        logger.info(f"File {i}/{len(file_list)}: {file_path}")
        if upload_file(s3_client, file_path, bucket_name):
            success_count += 1
        else:
            failed_count += 1
    
    logger.info("=" * 50)
    logger.info(f"COMPLETE: {success_count}/{len(file_list)} successful")
    logger.info("=" * 50)
    
    return success_count == len(file_list)


def main():
    files = ["/Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt",
             "/Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt"]
    upload_files_to_s3(files)


if __name__ == "__main__":
    main()
