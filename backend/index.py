from io import BytesIO
import os
import random
import imghdr
from bson.binary import Binary
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from flask_pymongo import pymongo
# import tensorflow as tf

import transformers
from transformers import TFAutoModel , AutoTokenizer

from tensorflow.keras.models import load_model
from dotenv import load_dotenv


from utils.predict_functions import predictVoilenceAndAdult, predictToxicity
from utils.text_similarity import checkSimilar2
from utils.muril import loadmodel

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# print(os.getenv('MONGODB_URI'))
client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
print("**********\n MongoClient: ",client)
print("**********\n")
db = client.get_database('test') if client else None 
print("**********\n Database: ",db)
print("**********\n")


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    print(os.getenv('MONGODB_URI'))
    return jsonify({'status':'active', 'name': 'InterceptAI', 'models': ['violence']})

@app.route('/image/<image_id>', methods=['GET'])
def get_image(image_id):
    image = db.tweets.find_one({"_id": ObjectId(image_id)})
    if image is None:
        return jsonify({'message': 'Image not found', 'success':'false'}), 404
    else:
        image_data = image['tweet']
        image_format = image['format']
        return send_file(BytesIO(image_data), mimetype=('image/'+image_format))
    
# Images
@app.route('/model/check-image', methods=['GET', 'POST'])
@cross_origin()
def checkImage():
    if request.method == 'GET':
        return jsonify({'status':'active', 'message': 'InterceptAI: Image Check'})
    elif request.method == 'POST':
        image = request.files['image']
        image_data = Binary(image.read())
        image_format = imghdr.what(None, h=image_data) 

        model1 =load_model("./models/resnet50_final_violence.h5")
        model2 =load_model("./models/resnet50_final_adult.h5")
        prediction_violence = predictVoilenceAndAdult(model1, BytesIO(image_data))
        prediction_adult = predictVoilenceAndAdult(model2, BytesIO(image_data))
        print("Violence" , int(prediction_violence))
        print("Adult" , int(prediction_adult))
        if(int(prediction_violence) or int(prediction_adult)):
            prediction = "Inappropriate"
            predicted_val = 1
            return jsonify({'success':'true', 'message': 'Inappropriate Content', 'prediction': prediction, 'predicted_val': predicted_val, 'error_code': 1})
        else:
            if db is None:
                return jsonify({'success': 'false', 'message': 'DB not connected'})
            else:
                image_id = db.tweets.insert_one({'id': random.randint(1000, 2000),'tweet': image_data, 'tweetType': 'image', 'name': "Sahib Singh", 'username': '@ssahibsingh', 'format': image_format }).inserted_id
                prediction = "Appropriate"
                predicted_val = 0
                print("Image ID: ", image_id)
                return jsonify({'success':'true', 'message': 'Appropriate Content', 'prediction': prediction, 'predicted_val': predicted_val, 'image_id': str(image_id), 'image': str(image_data), 'format': image_format, 'error_code': 0})


# Text Checker
@app.route('/model/toxic-content', methods=['GET', 'POST'])
@cross_origin()
def toxicity():
    if request.method == 'GET':
        return jsonify({'status':'active', 'message': 'InterceptAI: Toxicity Detection'})
    elif request.method == 'POST':
        text=request.json['text']
        model = load_model("./models/English_Toxic_comment_model1.h5")
        print(predictToxicity(model, text))

        prediction_val = predictToxicity(model, text)
        if(prediction_val == 1):
            prediction = "toxic"
        else:
            prediction = "normal"
        return jsonify({'success':'true', 'message': 'Prediction Successfull', 'prediction': prediction, 'predicted_val': int(prediction_val)})
    




@app.route('/model/similarity', methods=['GET', 'POST'])
@cross_origin()
def similarity():
    if request.method == 'GET':
        # model =load_model("./models/comment_toxic.h5")
        # print(predictToxicity(model))
        return jsonify({'status':'active', 'message': 'InterceptAI: Similarity Detection'})
    elif request.method == 'POST':
        text = request.json['text']
        # check blocked word
        output = checkSimilar2(text)
        if output is None:
            return jsonify({'success':'false', 'message': 'Prediction'})
        elif output == False:
            model = load_model('./models/Muril_best_model1.h5', custom_objects={"TFBertModel": transformers.TFBertModel})
            output2 = loadmodel(model, text)
            return jsonify({'success':'true', 'message': 'Prediction Successful', 'prediction': str(output2)})
        elif output == True:
            output = 1
            return jsonify({'success':'true', 'message': 'Prediction Successful', 'prediction': str(output)})
        # return jsonify({'success':'true', 'message': 'Prediction Successful', 'prediction': str(output)})
    
@app.route('/model/muril', methods=['GET', 'POST'])
@cross_origin()
def muril():
    if request.method == 'GET':
        return jsonify({'status':'active', 'message': 'InterceptAI: Similarity Detection'})
    elif request.method == 'POST':
        text = request.json['text']
        model = load_model('./models/Muril_best_model1.h5', custom_objects={"TFBertModel": transformers.TFBertModel})
        output = loadmodel(model, text)
        if output is None:
            return jsonify({'success':'false', 'message': 'Prediction'})
        return jsonify({'success':'true', 'message': 'Prediction Successful', 'prediction': str(output)})
    




# @app.route('/model/violence', methods=['GET', 'POST'])
# @cross_origin()
# def voilence():
#     if request.method == 'GET':
#         return jsonify({'status':'active', 'message': 'InterceptAI: Voilence Detection'})
#     elif request.method == 'POST':
#         image = request.files['image']
#         image_data = Binary(image.read())

#         model =load_model("./models/resnet50_final_violence.h5")
#         prediction = predictVoilenceAndAdult(model, BytesIO(image_data))

#         print(int(prediction))
#         predicted_val = int(prediction)          
#         if prediction == 1:
#             prediction = "violence"
#         else:
#             prediction = "no violence"

#         return jsonify({'status':'active', 'message': 'Prediction', 'prediction': prediction, 'predicted_val': predicted_val})
    
# @app.route('/model/adult', methods=['GET', 'POST'])
# @cross_origin()
# def adult():
#     if request.method == 'GET':
#         return jsonify({'status':'active', 'message': 'InterceptAI: Voilence Detection'})
#     elif request.method == 'POST':
#         image = request.files['image']
#         image_data = Binary(image.read())

#         model =load_model("./models/resnet50_final_adult.h5")
#         prediction = predictVoilenceAndAdult(model, BytesIO(image_data))

#         print(int(prediction))
#         predicted_val = int(prediction)
#         if prediction == 1:
#             # predicted_val = 0
#             prediction = "normal"
#         else:
#             # predicted_val = 1
#             prediction = "adult"
#         return jsonify({'status':'active', 'message': 'Prediction', 'prediction': prediction, 'predicted_val': predicted_val})

