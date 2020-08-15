from .yandex_parser import yandex_parser
from app import app
import sys
from flask import Flask, flash, request, redirect, url_for, session, jsonify, render_template, make_response
import uuid
from PIL import Image
import requests
from io import BytesIO


app.config['SECRET_KEY'] = 'XYp7UAjYC6KAhjdhFKoPTHQKRgULDwMG'

@app.route('/', methods=["POST", "GET", "OPTIONS"])
def index():    
    if request.method == "POST":
        req = request.get_json(force=True)
        print('req = ', req)
        if req['type'] == "parse_data_yandex":
            search_request = req['search_request']
            urls = yandex_parser(search_request)
            res = jsonify({ "status": 200, "image_ids": urls })
            return make_response(res)
            
        elif req['type'] == "upload_data":
            pass
        
        elif req['type'] == "get_image_list":
            pass

        elif req['type'] == "session_begin":
            session["id"] = uuid.uuid4()
            res = make_response(jsonify({ "status": 200, "session_id": session["id"]}))
            return res
        #upload_result = upload(file, use_filename='true',
                                # folder='RealityNeurons/')
        #cloudinary_url(upload_result['public_id'], format='jpg')
        return redirect(url_for('success'))
    return ''
        

@app.route('/mew/', methods=["POST", "GET"])
def yandex_load():
    if request.method == "POST":
        text = request.form['text']
        if text !="":
            folder = 'RealityNeurons/'+text
            urls = yandex_parser(text)
            # for url in urls:
            #     cloudinary.uploader.upload(url, folder=folder)
            urls = list(urls)
            res = {"urls":urls}
            return jsonify(res)
    return render_template('mew.html')

@app.route('/error/')
def error():
    return 'error'

@app.route('/success/')
def success():
    return 'success page'