import boto3
import json
import re

version_dict = {}
env = 'dev'
AWS_KEY = "************"
AWS_SECRET = "****************"

s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_KEY,
                         aws_secret_access_key=AWS_SECRET
                         )

s3_res = boto3.resource('s3',
                        aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET
                        )

bucket = s3_res.Bucket('rovercraft2')
bucket_configs = bucket.objects.filter(Prefix='config/')
for o in bucket_configs:
    group = re.match("^config/v(\d+).*" + f"{env}.json", o.key, re.IGNORECASE)
    if group:
        version_dict[group[0]] = [int(group[1])]

max_version = max(version_dict, key=version_dict.get)
try:
    response = s3_client.get_object(Bucket="rovercraft2", Key=max_version)
    data = response['Body']
    result = json.load(data)
except:
    raise
print(result['appsyncHost'])
