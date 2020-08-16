from .yandex_parser import yandex_parser
from app import app
from . import api
import sys
from flask import Flask, flash, request, redirect, url_for, session, jsonify, render_template, make_response
import uuid
import requests
# CLOUDINARY
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload
import cloudinary.api
from cloudinary.utils import cloudinary_url
#IMAGES
from PIL import Image
import io
from io import BytesIO
import base64

def scale_image(url):
    response = requests.get(url)
    original_image = Image.open(BytesIO(response.content)).convert('RGB')
    width, height = original_image.size

    if width>height:
        rel = height/width
        height = 224
        width = 224 + int(width*rel)

    else:
        rel = width/height
        width = 224
        height = 224 + int(width*rel)
    max_size = (width, height)
        
    
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    # original_image = original_image.crop((0, 0, 224, 224))
    print("img", original_image, url)
    return original_image


CLOUDINARY = ({
    # 'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
    # 'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    # 'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
    'cloud_name': 'nekolya75',
    'api_key': '829731229717378',
    'api_secret': 'HJk6N_DrRee9kSJhFeq0q_nPVXY',
})


cloudinary.config(cloud_name='nekolya75', api_key='829731229717378',
                  api_secret='HJk6N_DrRee9kSJhFeq0q_nPVXY')


app.config['SECRET_KEY'] = 'XYp7UAjYC6KAhjdhFKoPTHQKRgULDwMG'
arr = []  
@app.route('/', methods=["POST", "GET", "OPTIONS"])
def index(): 
    global arr
    if request.method == "POST":
        req = request.get_json(force=True)
        if req['type'] == "parse_data_yandex":
            print('req = ', req)
            search_request = req['search_request']
            folder = 'RealityNeurons/' + search_request
            urls = yandex_parser(search_request)
            success_add = 0
            for url in urls:
                try:
                    if req['session_id'] !="":
                        print(req['session_id'])
                        folder = "RealityNeurons/" + str(req['session_id'])
                        print(folder)
                        img = scale_image(url)
                        buf = BytesIO()
                        img.save(buf, format='JPEG')
                        byte_im = buf.getvalue()
                        print(success_add)
                        cloudinary.uploader.upload(byte_im, folder=folder, public_id = str(success_add))
                        success_add += 1
                except:
                    print('something wrong')
            urls = []
            for i in range(success_add):
                urls.append(str(i)+".jpg")
            arr = urls.copy()
            res = jsonify({ "status": 200, "image_ids": urls })
            return make_response(res)
            
        elif req['type'] == "upload_data":
            # code = req['image']
            # imgdata = base64.b64decode(code)
            # image = Image.open(io.BytesIO(imgdata))
            # print(img[0:6])
            pass
        
        elif req['type'] == "get_image_list":
            print('req = ', req)
            res = jsonify({ "status": 200, "image_ids": arr })
            return make_response(res)

        elif req['type'] == "remove_image":
            print('req = ', req)
            cloudinary.uploader.destroy(req['image_id'])
            print(arr, req['image_id'])
            arr.remove(req['image_id'])

        elif req['type'] == "session_begin":
            session["id"] = uuid.uuid4()
            res = make_response(jsonify({ "status": 200, "session_id": session["id"]}))
            return res

        elif req['type'] == "startTraining":
            print('req = ', req)
            class_name = req['class_name']
            session_id = req['session_id']
            print(class_name, session_id)

            api.load_data_from_urls(arr, class_name)

            api.train_model(class_name)
            
            return make_response()
        #upload_result = upload(file, use_filename='true',
                                # folder='RealityNeurons/')
        #cloudinary_url(upload_result['public_id'], format='jpg')
        return ''
    return ''
