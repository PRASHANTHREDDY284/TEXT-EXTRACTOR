import os
from flask import Flask, render_template, request, redirect, url_for, flash
import easyocr
import asyncio
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

async def process_image(image_path):
    try:
        reader = easyocr.Reader(['en'])
        ocr_result = reader.readtext(image_path, paragraph=True)
        return ocr_result
    except Exception as e:
        print(f'Error during OCR: {e}')
        return None

def batch_process_images(image_paths):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(run_ocr_tasks(image_paths, loop))
    return results

async def run_ocr_tasks(image_paths, loop):
    tasks = [process_image(image_path) for image_path in image_paths]
    return await asyncio.gather(*tasks, return_exceptions=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        flash('No file part in the request', 'error')
        return redirect(url_for('home'))

    file = request.files['image']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('home'))

    if not allowed_file(file.filename):
        flash('Invalid file format. Please upload a valid image file (png, jpg, jpeg)', 'error')
        return redirect(url_for('home'))

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        ocr_results = batch_process_images([file_path])

        if ocr_results:
            flash('OCR performed successfully', 'success')
            app.logger.info("OCR Result: %s", ocr_results)
            return redirect(url_for('result', ocr_text=ocr_results[0][0][1]))
        else:
            flash('OCR failed or produced an empty result. Please select another image.', 'error')
            return redirect(url_for('home'))

    except Exception as e:
        flash('An error occurred during processing. Please try again.', 'error')
        app.logger.error(f'Error during processing: {e}')
        return redirect(url_for('home'))

@app.route('/result')
def result():
    ocr_text = request.args.get('ocr_text', '')  # Get OCR text from the request arguments
    return render_template('result.html', ocr_text=ocr_text)

if __name__ == '__main__':
    app.run(debug=True)
