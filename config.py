# 이 파일은 데이터베이스 관련 정보를 저장함
# 노출되면 안됨!!!

class Config:

    # S3 관련 변수
    S3_BUCKET = 'blue-rekognition'
    S3_BASE_URL = 'https://'+S3_BUCKET+'.s3.amazonaws.com/'

    # aws 액세스 키
    AWS_ACCESS_KEY_ID = 'AKIAY7EHY7KFUDFIS47Q'
    AWS_SECRET_ACCESS_KEY = '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'