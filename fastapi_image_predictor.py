import io
import numpy as np
import pickle
import base64
from PIL import Image
from fastapi import FastAPI, Request, HTTPException
import os

# Initialize the FastAPI app
app = FastAPI()

# Allowed models (Add your model filenames here)
ALLOWED_MODELS = {'clf.pickle'}

# Directory where models are stored
MODEL_DIR = './models'  

# Function to process the image
def process_image(encoded_image):
    # Decode the image from base64
    try:
        img = Image.open(io.BytesIO(base64.b64decode(encoded_image)))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image data")

    # Preprocess the image
    number = np.round((np.array(img) / 255) * 16)

    return number.reshape(1, -1)

# Endpoint to predict the image
@app.post("/predict/")
async def predict(request: Request):
    # Parse the request body as JSON
    req = await request.json()

    # Extract the base64 encoded image from the JSON request
    encoded_image = req.get("image")
    if not encoded_image:
        raise HTTPException(status_code=400, detail="Image data is required")

    # Extract the model name from the JSON request
    model_name = req.get("model")
    if not model_name:
        raise HTTPException(status_code=400, detail="Model name is required")

    # Validate the model name
    if model_name not in ALLOWED_MODELS:
        raise HTTPException(status_code=400, detail="Invalid model name")

    # Construct the full path to the model file
    model_path = os.path.join(MODEL_DIR, model_name)

    # Check if the model file exists
    if not os.path.isfile(model_path):
        raise HTTPException(status_code=400, detail="Model file not found")

    # Load the model
    try:
        with open(model_path, "rb") as f:
            clf = pickle.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading the model")

    # Process the image and obtain the prediction
    try:
        processed_image = process_image(encoded_image)
        prediction = clf.predict(processed_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during prediction")

    # Return the prediction as a JSON response
    return {"request_id": req.get("request_id"), "prediction": int(prediction[0])}
