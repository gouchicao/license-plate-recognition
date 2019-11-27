import tempfile
import werkzeug
import numpy as np

#import cv2

from hyperlpr import *
from PIL import Image

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


BASE_URL = '/license-plate-recognition/api/v1.0/'


class LicensePlateRecognition(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        img_file = args['file']

        if not img_file:
            return {'no file'}, 417

        with tempfile.NamedTemporaryFile() as file:
            img_data = img_file.read()
            file.write(img_data)
            
            image = Image.open(file)
            image = np.asarray(image)

            result = HyperLPR_PlateRecogntion(image)
            if not result:
                return {'no license plate'}, 417

#            frame = cv2.imread(file.name)

            res = []
            for item in result:
                print(item[0])
                det_obj = {}
                print(item[2])
                rect = item[2]
                det_obj['rectangle'] = {'x':rect[0], 'y':rect[1], 'w':rect[2]-rect[0], 'h':rect[3]-rect[1]}
                det_obj['object'] = item[0]
                det_obj['confidence'] = item[1]
                res.append(det_obj)
                
#                rect = det_obj['rectangle']
#                cv2.rectangle(frame, (rect['x'], rect['y']), (rect['x']+rect['w'], rect['y']+rect['h']), np.random.uniform(0, 255, size=(1)), thickness=2)

#            cv2.imwrite('test.jpg', frame)

        return res, 201
        
        
if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(LicensePlateRecognition, BASE_URL + 'detect')

    app.run(host='0.0.0.0', debug=True)
