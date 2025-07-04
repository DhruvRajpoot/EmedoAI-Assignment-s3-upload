# S3 File Upload Script

Upload multiple files to AWS S3 with automatic name conflict resolution and logging.

## Setup

1. **Install dependencies**:
   ```bash
   pip install boto3 python-dotenv
   ```

2. **Create `.env` file**:
   ```env
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   AWS_BUCKET_NAME=your_bucket
   ```

## Usage

**Edit the file list in `main()`:**
```python
def main():
    files = ["/path/to/file1.txt", "/path/to/file2.jpg"]
    upload_files_to_s3(files)
```

**Run the script:**
```bash
python index.py
```

## Features

- ✅ Uploads multiple files to S3
- ✅ Handles filename conflicts (adds timestamp)
- ✅ Validates file size (100MB limit)
- ✅ Logs all operations to `s3_upload.log`

## Log Output
```text
2025-07-04 22:08:10 - INFO - ==================================================
2025-07-04 22:08:10 - INFO - S3 UPLOAD STARTED - 2 files
2025-07-04 22:08:10 - INFO - ==================================================
2025-07-04 22:08:10 - INFO - AWS credentials loaded
2025-07-04 22:08:11 - INFO - Connected to S3
2025-07-04 22:08:11 - INFO - File 1/2: /Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt
2025-07-04 22:08:11 - INFO - Uploading: /Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt
2025-07-04 22:08:11 - INFO - Conflict: test.txt -> test_20250704_220811.txt
2025-07-04 22:08:11 - INFO - SUCCESS: /Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt -> s3://test-bucket-dhruv-rajpoot/test_20250704_220811.txt
2025-07-04 22:08:11 - INFO - File 2/2: /Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt
2025-07-04 22:08:11 - INFO - Uploading: /Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt
2025-07-04 22:08:11 - INFO - Conflict: test.txt -> test_20250704_220811.txt
2025-07-04 22:08:11 - INFO - SUCCESS: /Users/dhruvrajpoot/Desktop/Mine/PythonScript/test.txt -> s3://test-bucket-dhruv-rajpoot/test_20250704_220811.txt
2025-07-04 22:08:11 - INFO - ==================================================
2025-07-04 22:08:11 - INFO - COMPLETE: 2/2 successful
2025-07-04 22:08:11 - INFO - ==================================================
```
