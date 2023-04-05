from flask import jsonify, Flask, request, render_template
from gatedGan.generateImage import generate_image
from stylebank.transform import transformImage
from styleMixer.generate_image import generate_image_styleMixer
import io
import base64
import ast

app = Flask(__name__)


# route only for gatedGan transform
@app.route('/stylebankTransform', methods=['POST'])
def stylebankTransform():
    # Get the uploaded image file
    file = request.files['image']
    style = ast.literal_eval(request.form['style'])

    stylized_image = transformImage(file, style)

    buffer = io.BytesIO()
    stylized_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64-encoded string as a JSON response
    return jsonify({'image': base64_image})


@app.route('/transformGated', methods=['POST'])
def transformGated():
    # Get the uploaded image file
    file = request.files['image']
    ab = ast.literal_eval(request.form['style1'])
    uki = ast.literal_eval(request.form['style2'])
    re = ast.literal_eval(request.form['style3'])
    width = -1
    height = -1
    if request.form['resizeWidth']:
        width = ast.literal_eval(request.form['resizeWidth'])
    if request.form['resizeHeight']:
        height = ast.literal_eval(request.form['resizeHeight'])
    style = [ab, uki, re, 1]
    stylized_image, gen_time = generate_image(style, file, width, height)
    buffer = io.BytesIO()
    stylized_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64-encoded string as a JSON response
    return jsonify({'image': base64_image, 'text': str(round(gen_time,3))})


# route only for styleMixer transform
@app.route('/transformStyleMixer', methods=['POST'])
def transform_styleMixer():
    # Get the uploaded image file
    style_file = request.files['style_image']
    content_file = request.files['content_image']

    stylized_image = generate_image_styleMixer(style_file, content_file)
    buffer = io.BytesIO()
    stylized_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64-encoded string as a JSON response
    return jsonify({'image': base64_image})


@app.route('/stylebank', methods=['GET'])
def stylebank():
    # modify the upload template accordingly if you need to add new transform method
    return render_template('stylebank.html')


@app.route('/gated', methods=['GET'])
def gatedGan():
    # modify the upload template accordingly if you need to add new transform method
    return render_template('gatedGan.html')

@app.route('/stylemixer', methods=['GET'])
def stylemixer():
    # modify the upload template accordingly if you need to add new transform method
    return render_template('stylemixer.html')


if __name__ == '__main__':
    app.run()
