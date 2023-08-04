from flask_restful import Resource
from flask import request
from datetime import datetime
from config import Config

import boto3


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
