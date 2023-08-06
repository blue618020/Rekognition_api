from flask import Flask
from flask_restful import Api

from resources.photo import PhotoExpression, PhotoResource

app = Flask(__name__)

api = Api(app)

# 얼굴 비교
api.add_resource(PhotoResource,'/photo')

# 얼굴 표정
api.add_resource(PhotoExpression, '/photo')

if __name__ == 'main':
    app.run()
