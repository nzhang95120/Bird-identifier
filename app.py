
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

def create_class_map(base_path='birds/test'):
    species = sorted(os.listdir(base_path))  # Ensure alphabetical order
    class_map = {idx: name.replace('_', ' ').title() for idx, name in enumerate(species)}
    return class_map

print("Loading model...")
model = load_model('bird_classifier/model.keras')
print("Model loaded successfully.")

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Missing image file', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected image', 400
    if file:
        img = image.load_img(file, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array_expanded_dims = np.expand_dims(img_array, axis=0)
        
        prediction = model.predict(img_array_expanded_dims)
        class_idx = np.argmax(prediction, axis=1)
        
        class_map = create_class_map()
        predicted_class = class_map.get(class_idx[0], "Unknown class")
        
        return predicted_class

if __name__ == '__main__':
    print("Starting Flask app...")

    app.run(debug=True)
