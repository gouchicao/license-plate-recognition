import os
import requests


API_URL = 'http://localhost:5000/license-plate-recognition/api/v1.0/'


def detect(filename):
    files = {'file': (filename, open(filename, 'rb'), 'image/png', {})}
    response = requests.post(API_URL + "detect", files=files)
    return response.json()

if __name__ == '__main__':
    json = detect('images/2.jpg')
    print('response json>\n', json)
