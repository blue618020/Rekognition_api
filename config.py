# 이 파일은 데이터베이스 관련 정보를 저장함
# 노출되면 안됨!!!

class Config:
    # # DB 관련 정보
    # HOST = 'yhdb.csigebpxoyml.ap-northeast-2.rds.amazonaws.com'
    # DATABASE = 'posting_db'
    # DB_USER = 'posting_db_user'
    # DB_PASSWORD = '1234'

    # # 비번 암호화
    # SALT = '0417helloqkqn'

    # # JWT 환경 변수 세팅
    # JWT_SECRET_KEY = 'hello~!by@'
    # JWT_ACCESS_TOKEN_EXPIRES = False # 특정 시간이 지나면 로그아웃 할 건가?=false
    # PROPAGATE_EXCEPTIONS = True

    # S3 관련 변수
    S3_BUCKET = 'blue-rekognition'
    S3_BASE_URL = 'https://'+S3_BUCKET+'.s3.amazonaws.com/'

