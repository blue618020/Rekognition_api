from flask_restful import Resource
from flask import request
from datetime import datetime
from config import Config

import boto3

# Rekognition 클라이언트 생성
s3 = boto3.client('rekognition', 
                'ap-northeast-2',
                aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)
    
# 챗GPT 가 알려준 코드를 사용해봄. 되는지는 모름
class  PhotoExpression(Resource):
    def post(self):
        with open(Resource, 'rb') as image_file:
            image_bytes = image_file.read()

        response = s3.detect_faces(
            Image={
                'Bytes': image_bytes
            },
            Attributes=['ALL']  # 모든 얼굴 특징, 포즈, 표정, 성별 등을 분석하도록 설정
        )

        emotions = []
        for face_detail in response['FaceDetails']:
            if 'Emotions' in face_detail:
                for emotion in face_detail['Emotions']:
                    emotions.append({
                        'Type': emotion['Type'],
                        'Confidence': emotion['Confidence']
                    })

        # 데이터 받아오기
        sourceImage = request.files['sourceImage']

        # 얼굴 표정 인식 결과 출력
        for emotions in sourceImage:
            print(f"Emotion: {emotion['Type']}, Confidence: {emotion['Confidence']}%")

        return emotions
    
    