import io
import numpy as np
import pickle
import base64
from PIL import Image

def process_image(encoded_image):    
    # Decode image from base64
    img = Image.open(io.BytesIO(base64.b64decode(encoded_image)))

    # Preprocess the image
    number = np.round((np.array(img)/255)*16)

    # prediction
    prediction = clf.predict(number.reshape(1, -1))
    return prediction[0]

def main():
    # Open and encode the image
    with open("digit2.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    print(process_image(encoded_string))

if __name__ == "__main__":
    # load model
    with open("clf.pickle", "rb") as f:
        clf = pickle.load(f)
    main()

