from flask import Flask
from flask_restful import Api

from resources.photo import PhotoResource

app = Flask(__name__)

api = Api(app)

# 사진 업로드 
api.add_resource(PhotoResource,'/photo')

if __name__ == 'main':
    app.run()
