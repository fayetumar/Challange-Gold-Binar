#Importing Libraries
import re
import sqlite3
import pandas as pd
import os

from datetime import datetime
from flask import Flask, jsonify,request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from fileinput import filename
from werkzeug.utils import secure_filename
from cleaning import preprocess

#Defining app
app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing and Modeling')
        },
    host = LazyString(lambda:request.host)
)

#Swager configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path":  "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)

#connect database
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()
#Defining and executing the query for table data if it not avaliable
conn.execute('''CREATE TABLE IF NOT EXISTS data (text varchar(255), text_clean varchar(255));''')

#Basic API 'Hello World'
@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/',methods=['GET'])
def hello_world():
    json_response = {
        'status_code': 200,
        'description': "Menyapa Hello World",
        'data': "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

#Text cleansing
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')
    text_clean = preprocess(text)

    with conn:
        c.execute('''INSERT INTO data(text, text_clean) VALUES (? , ?);''', (text, text_clean))
        conn.commit()

    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': text_clean,
    }
    
    response_data = jsonify(json_response)
    return response_data

#Defining allowed extensions
allowed_extensions = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


#API for processing inputted file
@swag_from("docs/file_upload.yml", methods = ['POST'])
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files['file']
    print("request file")
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        time_stamp = (datetime.now().strftime('%d-%m-%Y_%H%M%S'))

        new_filename = f'{filename.split(".")[0]}_{time_stamp}.csv'
        
        
        save_location = os.path.join('input', new_filename)
        file.save(save_location)


        filepath = 'input/' + str(new_filename)

        data = pd.read_csv(filepath, encoding='latin-1')
        first_column_pre_process = data.loc[:, 'Tweet']

        cleaned_word = []

        for text in first_column_pre_process:
            print('proses')
            file_clean = preprocess(text)
            print("file clean")
            with conn:
                c.execute('''INSERT INTO data(text, text_clean) VALUES (? , ?);''',(text, file_clean))
                conn.commit()

            cleaned_word.append(file_clean)
        

        new_data_frame = pd.DataFrame(cleaned_word, columns= ['Cleaned Text'])
        outputfilepath = f'output/{new_filename}'
        new_data_frame.to_csv(outputfilepath)

    json_response = {
        'status_code' : 200,
        'description' : "File yang sudah diproses",
        'data' : "open this link to download : http://127.0.0.1:5000/download",
    }

    response_data = jsonify(json_response)
    return response_data    

if __name__ == '__main__':
    app.run()