import os

import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()
SES_REGION = os.getenv("SES_REGION")
SES_ACCESS_KEY_ID = os.getenv("SES_ACCESS_KEY_ID")
SES_SECRET_ACCESS_KEY = os.getenv("SES_SECRET_ACCESS_KEY")
if not all([SES_REGION, SES_ACCESS_KEY_ID, SES_SECRET_ACCESS_KEY]):
    raise EnvironmentError("Missing SES configuration in environment variables.")

ses_client = boto3.client(
    "ses",
    config=Config(region_name=SES_REGION),
    aws_access_key_id=SES_ACCESS_KEY_ID,
    aws_secret_access_key=SES_SECRET_ACCESS_KEY,
)

sesv2_client = boto3.client(
    "sesv2",
    config=Config(region_name=SES_REGION),
    aws_access_key_id=SES_ACCESS_KEY_ID,
    aws_secret_access_key=SES_SECRET_ACCESS_KEY,
)
