# import os
import random
import imghdr
import transformers
from io import BytesIO
from bson.binary import Binary
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from flask_pymongo import pymongo
from dotenv import load_dotenv

from tensorflow.keras.models import load_model

from config.connect_db import connect_to_mongodb
from utils.predict_functions import predict_violence_and_adult, predict_toxicity
from utils.text_similarity import check_similarity
from utils.muril import load_muril_model

# Load Environment Variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Enable CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to MongoDB
db = connect_to_mongodb()


# Home Route
@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return jsonify({"status": "active", "name": "InterceptAI", "models": ["violence"]})


# Get Image with image ID
@app.route("/image/<image_id>", methods=["GET"])
def get_image(image_id):
    try:
        image = db.tweets.find_one({"_id": ObjectId(image_id)})
        if image is None:
            return jsonify({"message": "Image not found", "success": False}), 404

        image_data = image["tweet"]
        image_format = image["format"]
        return send_file(BytesIO(image_data), mimetype=f"image/{image_format}")

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}", "success": False}), 500


# Check Images
@app.route("/model/check-image", methods=["GET", "POST"])
@cross_origin()
def checkImage():
    if request.method == "GET":
        return jsonify({"status": "active", "message": "InterceptAI: Image Check"})
    elif request.method == "POST":
        try:
            image = request.files["image"]
            image_data = Binary(image.read())
            image_format = imghdr.what(None, h=image_data)

            model1 = load_model("./models/Violence_ResNet50Model.h5")
            model2 = load_model("./models/Adult_ResNet50Model.h5")
            prediction_violence = predict_violence_and_adult(
                model1, BytesIO(image_data)
            )
            prediction_adult = predict_violence_and_adult(model2, BytesIO(image_data))
            print("Violence", int(prediction_violence))
            print("Adult", int(prediction_adult))
            if int(prediction_violence) or int(prediction_adult):
                prediction = "Inappropriate"
                predicted_val = 1
                return jsonify(
                    {
                        "success": "true",
                        "message": "Inappropriate Content",
                        "prediction": prediction,
                        "predicted_val": predicted_val,
                        "error_code": 1,
                    }
                )
            else:
                if db is None:
                    return jsonify({"success": "false", "message": "DB not connected"})
                else:
                    image_id = db.tweets.insert_one(
                        {
                            "id": random.randint(1000, 2000),
                            "tweet": image_data,
                            "tweetType": "image",
                            "name": "Sahib Singh",
                            "username": "@ssahibsingh",
                            "format": image_format,
                        }
                    ).inserted_id
                    prediction = "Appropriate"
                    predicted_val = 0
                    print("Image ID: ", image_id)
                    return jsonify(
                        {
                            "success": "true",
                            "message": "Appropriate Content",
                            "prediction": prediction,
                            "predicted_val": predicted_val,
                            "image_id": str(image_id),
                            "image": str(image_data),
                            "format": image_format,
                            "error_code": 0,
                        }
                    )
        except Exception as e:
            print(e)
            return jsonify({"success": "false", "message": "Error in Image Check"})


# Text Checker
@app.route("/model/toxic-content", methods=["GET", "POST"])
@cross_origin()
def toxicity():
    if request.method == "GET":
        return jsonify(
            {"status": "active", "message": "InterceptAI: Toxicity Detection"}
        )
    elif request.method == "POST":
        try:
            text = request.json["text"]
            model = load_model("./models/English_Toxic_comment_model1.h5")
            print(predict_toxicity(model, text))

            prediction_val = predict_toxicity(model, text)
            if prediction_val == 1:
                prediction = "toxic"
            else:
                prediction = "normal"
            return jsonify(
                {
                    "success": "true",
                    "message": "Prediction Successfull",
                    "prediction": prediction,
                    "predicted_val": int(prediction_val),
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {"success": "false", "message": "Error in Toxicity Detection"}
            )


# Check Text Similarity
@app.route("/model/similarity", methods=["GET", "POST"])
@cross_origin()
def similarity():
    if request.method == "GET":
        # model =load_model("./models/comment_toxic.h5")
        # print(predict_toxicity(model))
        return jsonify(
            {"status": "active", "message": "InterceptAI: Similarity Detection"}
        )
    elif request.method == "POST":
        try:
            text = request.json["text"]
            # check blocked word
            output = check_similarity(text)
            if output is None:
                return jsonify({"success": "false", "message": "Prediction"})
            elif output == False:
                model = load_model(
                    "./models/Muril_best_model1.h5",
                    custom_objects={"TFBertModel": transformers.TFBertModel},
                )
                output2 = load_muril_model(model, text)
                return jsonify(
                    {
                        "success": "true",
                        "message": "Prediction Successful",
                        "prediction": str(output2),
                    }
                )
            elif output == True:
                output = 1
                return jsonify(
                    {
                        "success": "true",
                        "message": "Prediction Successful",
                        "prediction": str(output),
                    }
                )
            # return jsonify({'success':'true', 'message': 'Prediction Successful', 'prediction': str(output)})
        except Exception as e:
            print(e)
            return jsonify(
                {"success": "false", "message": "Error in Similarity Detection"}
            )


# Checks Toxicity in multiple languages
@app.route("/model/muril", methods=["GET", "POST"])
@cross_origin()
def muril():
    if request.method == "GET":
        return jsonify(
            {"status": "active", "message": "InterceptAI: Similarity Detection"}
        )
    elif request.method == "POST":
        try:
            text = request.json["text"]
            model = load_model(
                "./models/Muril_best_model1.h5",
                custom_objects={"TFBertModel": transformers.TFBertModel},
            )
            output = load_muril_model(model, text)
            if output is None:
                return jsonify({"success": "false", "message": "Prediction"})
            return jsonify(
                {
                    "success": "true",
                    "message": "Prediction Successful",
                    "prediction": str(output),
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {"success": "false", "message": "Error in Similarity Detection"}
            )
