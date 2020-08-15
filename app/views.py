from .yandex_parser import yandex_parser
from app import app
from flask import Flask, flash, request, redirect, url_for, session, jsonify, render_template

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        #upload_result = upload(file, use_filename='true',
                                # folder='RealityNeurons/')
        #cloudinary_url(upload_result['public_id'], format='jpg')
        return redirect(url_for('success'))
        
    return render_template('index.html')


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