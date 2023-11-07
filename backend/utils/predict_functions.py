import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from pathlib import Path
from tensorflow.keras.preprocessing import image as image_utils
from tensorflow.keras.preprocessing.sequence import pad_sequences


def predict_violence_and_adult(model, img):
    print("**********\n Predicting.... \n\n")

    test_img = image_utils.load_img(img, target_size=(224, 224))
    img_arr = image_utils.img_to_array(test_img)
    img_arr = tf.expand_dims(img_arr, 0)

    prediction = model.predict(img_arr)
    predicted_class = np.round(prediction[0])

    print("Predicted Class: ", predicted_class)
    print("**********\n")

    return predicted_class[0]


def predict_toxicity(model, text):
    with open("tokenizer.pickle", "rb") as handle:
        tokenizer = pickle.load(handle)

    my = tokenizer.texts_to_sequences([text])
    test_padded = pad_sequences(my, maxlen=100, padding="pre", truncating="pre")
    predicted = model.predict(test_padded)
    allpred = (predicted > 0.5).astype("int")

    return max(allpred[0])
