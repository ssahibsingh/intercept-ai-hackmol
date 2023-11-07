import tensorflow as tf
from transformers import AutoTokenizer


def load_muril_model(model, text):
    hf_path = "google/muril-base-cased"
    tokenizer = AutoTokenizer.from_pretrained(hf_path)

    encodings = tokenizer(
        text, max_length=64, padding="max_length", truncation=True, return_tensors="tf"
    )

    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]

    # Preprocess input
    inputs = [input_ids, attention_mask]

    # Make prediction
    prediction = model(inputs)[0]

    return int(prediction > 0.5)
