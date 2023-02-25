import transformers
import tensorflow as tf
from transformers import TFAutoModel , AutoTokenizer
# model = tf.keras.models.load_model(, custom_objects={"TFBertModel": transformers.TFBertModel})

hf_path = "google/muril-base-cased" 
tokenizer = AutoTokenizer.from_pretrained(hf_path)

def loadmodel(model, text):
    encs = tokenizer(text,
                        max_length = 64,
                        padding= 'max_length',
                        truncation=True,
                        return_tensors ='tf'
                        )
    input_ids  = encs['input_ids']
    attention_mask = encs['attention_mask']
    # Preprocess input
    inputs  = [input_ids , attention_mask]
    # Make prediction
    prediction = model(inputs)[0]

    return int((prediction)>0.5)

    

