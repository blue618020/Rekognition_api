# 이 파일은 데이터베이스 관련 정보를 저장함
# 노출되면 안됨!!!

class Config:

    # S3 관련 변수
    S3_BUCKET = 'blue-rekognition'
    S3_BASE_URL = 'https://'+S3_BUCKET+'.s3.amazonaws.com/'

