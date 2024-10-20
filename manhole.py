from flask import Flask, render_template, request, url_for
import os
from PIL import Image

app = Flask(__name__)

# Define static folders for uploads and results
UPLOAD_FOLDER = os.path.join('static', 'uploads')
RESULT_FOLDER = os.path.join('static', 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the uploaded image in the static/uploads folder
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)
        
        # Perform visual inspection and generate result image
        result_image_path = perform_visual_inspection(image_path)

        # Generate the URL for the result image
        result_image_url = url_for('static', filename=os.path.join('results', os.path.basename(result_image_path)))

        return render_template('results.html', result_image=result_image_url)

def perform_visual_inspection(image_path):
    # Dummy inspection logic: Open the image and save a result
    image = Image.open(image_path)
    # For demonstration, we'll convert the image to grayscale
    result_image_path = os.path.join(RESULT_FOLDER, 'result_' + os.path.basename(image_path))
    image.convert('L').save(result_image_path)
    return result_image_path

if __name__ == '__main__':
    app.run(debug=True)

