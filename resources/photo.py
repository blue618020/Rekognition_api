from flask_restful import Resource
from flask import request
from datetime import datetime
from config import Config

import boto3
import json

## 얼굴 비교
class PhotoResource(Resource):
    def post(self):

        # 데이터 받아오기
        sourceImage = request.files['sourceImage']
        targetImage = request.files['targetImage']

        # 파일이름 시간순으로 가공
        current_time = datetime.now()
        sourceImage_file_name = 'sourceImage' + current_time.isoformat().replace(':','_') + '.jpg'
        targetImage_file_name = 'targetImage' + current_time.isoformat().replace(':','_') + '.jpg'

        # S3 저장
        s3 = boto3.client('s3',
                          aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)
        
        try:
            s3.upload_fileobj(sourceImage, 
                              Config.S3_BUCKET, 
                              sourceImage_file_name,
                              ExtraArgs = {'ACL':'public-read',
                                           'ContentType':'image/jpeg'})
            s3.upload_fileobj(targetImage, 
                              Config.S3_BUCKET, 
                              targetImage_file_name,
                              ExtraArgs = {'ACL':'public-read',
                                           'ContentType':'image/jpeg'})
            
        except Exception as e:
            return {'error':str(e)}, 500
        
        
        # 얼굴 비교
        s3 = boto3.client('rekognition', 
                          'ap-northeast-2',
                          aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)
        
        response = s3.compare_faces(SimilarityThreshold = 50,
                                    SourceImage = {"S3Object":{"Bucket":Config.S3_BUCKET, "Name":sourceImage_file_name}},
                                    TargetImage = {"S3Object":{"Bucket":Config.S3_BUCKET, "Name":targetImage_file_name}})
        
        # 결과 응답
        # 응답 시 "Similarity" 가 얼굴 일치 정보
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('The face at ' +
                str(position['Left']) + ' ' +
                str(position['Top']) +
                ' matches with ' + similarity + '% confidence')


        # 얼굴 일치하지 않으면 response 리스트가 비어버림
        if len(response['FaceMatches']) == 0:
            return {'result':'success', 'response':'얼굴이 일치하지 않습니다.'}
     
        return {'result':'success', 'response':response['FaceMatches']}


## 얼굴 표정 인식
class PhotoExpression(Resource):
    def post(self):
        # 데이터 받아오기
        sourceImage = request.files['sourceImage']

        # 파일이름 시간순으로 가공
        current_time = datetime.now()
        sourceImage_file_name = 'sourceImage' + current_time.isoformat().replace(':','_') + '.jpg'
        
        # S3 저장
        s3 = boto3.client('s3',
                          aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)
        
        try:
            s3.upload_fileobj(sourceImage, 
                              Config.S3_BUCKET, 
                              sourceImage_file_name,
                              ExtraArgs = {'ACL':'public-read',
                                           'ContentType':'image/jpeg'})
            
        except Exception as e:
            return {'error':str(e)}, 500
        
    
        # 얼굴 표정 인식 실행
        response = s3.detect_faces(Image={'S3Object':{'Bucket':Config.S3_BUCKET,'Name':sourceImage_file_name}},
                                   Attributes=['ALL']) 
                                # 모든 얼굴 특징, 포즈, 표정, 성별 등을 분석하도록 설정

        # 결과 응답
        print('Detected faces for ' + sourceImage)    
        for faceDetail in response['FaceDetails']:
            print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
                + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

            print('Here are the other attributes:')
            print(json.dumps(faceDetail, indent=4, sort_keys=True))

            # 개별 얼굴 세부 정보에 대한 예측 액세스 및 인쇄 (번역투)
            print("Gender: " + str(faceDetail['Gender']))
            print("Smile: " + str(faceDetail['Smile']))
            print("Eyeglasses: " + str(faceDetail['Eyeglasses']))
            print("Emotions: " + str(faceDetail['Emotions'][0]))

        return len(response['FaceDetails'])
    