import json
import urllib.request
from cryptography.fernet import Fernet
import base64
import gzip
import time
import boto3
from dotenv import load_dotenv
import os

# 1. Extract : 데이터 들고와서 decrypted 리스트
url = "http://ec2-3-37-12-122.ap-northeast-2.compute.amazonaws.com/api/data/log" # data source url
response = urllib.request.urlopen(url)
data = json.loads(response.read())

result = [d['data'].strip("'") for d in data]
# print(result[0])

key = b't-jdqnDewRx9kWithdsTMS21eLrri70TpkMq2A59jX8=' # 주어진 복호화 키
fernet = Fernet(key)
decrypted = []

for encrypted in result:
    decrypt = fernet.decrypt(encrypted).decode('ascii')
    decrypt_dict = eval(decrypt)
    decrypted.append(decrypt_dict)



# 2. Transform-(1) 데이터 압축(간결화) 진행 
compressed_data = []

for datum in decrypted:
    # user_id 압축
    uuid_64 = datum['user_id']

    # 바이트 문자열로 변환
    uuid_bytes = bytes.fromhex(uuid_64)

    # 44자의 UUID 문자열로 변환  
    uuid_44 = base64.urlsafe_b64encode(uuid_bytes).decode('utf-8')
    datum.update(user_id = uuid_44)

    # method 압축
    method = datum['method']
    datum['method'] = 1 if method == 'GET' else 2 

    # url 압축 (대부분 /api/products/product/, 해당사항을 1로)
    url = datum['url']
    datum['url'] = 1 if url == '/api/products/product/' else 2
    

    # inDate 압축
    datum['inDate'] = datum['inDate'].replace("-", "").replace("T", "").replace(":", "").replace(".", "").replace("Z", "")

    compressed_data.append(datum)
  
# 3. Load : s3에 적재
load_dotenv() 
s3_client = boto3.client('s3',
                        aws_access_key_id=os.environ['ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['ACCESS_SECRET_KEY']) #S3 연결


# 2.Transform-(2) : 로그 데이터를 gzip 압축하여 S3에 저장
def put_log_to_s3(log_data): 
    key = f"data/{time.strftime('%Y/%m/%d/%H')}/{time.strftime('%Y%m%d%H%M')}.json.gz" #업로드 경로 및 파일명
    compressed_bytes = gzip.compress(json.dumps(log_data).encode('utf-8')) #압축
    
    s3_client.put_object( 
        Bucket='de.project.c1',
        Key=key,
        Body=compressed_bytes, 
    ) #s3 업로드

put_log_to_s3(compressed_data)
print("업로드 완료")