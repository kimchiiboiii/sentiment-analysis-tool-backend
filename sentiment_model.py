import pickle
import tensorflow as tf
from flask import jsonify
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Backend component of the sentiment analysis
# Loads the model and tokenizer, handles the 
# preprocessing code/scripts, makes the prediction
# using the model and interprets the prediction


class PreprocessingError(Exception):
    # Custom exception class for preprocessing errors
    # Type errors and value errors with the input data etc.
    pass
class PredictionError(Exception):
    # Custom exception class for prediction errors
    # TensorFlow errors, model not loaded, etc.
    pass


# Load the model
model = tf.keras.models.load_model("put_model_here.h5")

# Load the tokenizer
with open("path_to_tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)


def preprocess_text(text):
    try:
        # Implement preprocessing here
        # Tokenize, pad, validate, etc.
        sequences = tokenizer.texts_to_sequences(text)
        preprocessed_text = pad_sequences(sequences, maxlen=100)
        return preprocessed_text
    except ValueError as ve:
        raise PreprocessingError("ValueError: " + str(ve))

def interpret_prediction(prediction):
    try:
        # Implement interpretation here
        # Control flow based on how the model scores sentiment
        # e.g. if score > 1.5, extremely positive, etc.
        sentiment = "positive" if prediction > 0.5 else "negative"
        return sentiment
    except TypeError as te:
        raise Exception("TypeError: " + str(te))
    except Exception as e:
        raise Exception("error: " + str(e))
    

def predict_sentiment(text):
    # Makes the prediction
    # Function that is called by the api
    try:
        preprocessed_text = preprocess_text(text)
        prediction = model.predict(preprocessed_text)
        sentiment = interpret_prediction(prediction)
        return sentiment
    except ValueError as ve:
        raise PreprocessingError("ValueError: " + str(ve))
    except tf.errors.OpError as oe:
        raise PredictionError("TensorFlow error: " + str(oe))
    except Exception as e:
        raise Exception(str(e))