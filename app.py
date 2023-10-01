from flask import jsonify, Flask, request, render_template
from gatedGan.generateImage import generate_image
from styleMixer.generate_image import generate_image_styleMixer
import io
import base64
import ast
import os
import random

app = Flask(__name__)

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
    stylized_image, gen_time, orig_img = generate_image(style, file, width, height)
    buffer = io.BytesIO()
    stylized_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    buffer_org = io.BytesIO()
    orig_img.save(buffer_org, format='PNG')
    base64_orig = base64.b64encode(buffer_org.getvalue()).decode('utf-8')

    # Return the base64-encoded string as a JSON response
    return jsonify({'image': base64_image, 'text': str(round(gen_time, 3)), 'orig': base64_orig})


# route only for styleMixer transform
@app.route('/transformStyleMixer', methods=['POST'])
def transform_styleMixer():
    # Get the uploaded image file
    style_file = request.files['style_image']
    content_file = request.files['content_image']

    stylized_image, gen_time = generate_image_styleMixer(style_file, content_file)
    buffer = io.BytesIO()
    stylized_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64-encoded string as a JSON response
    return jsonify({'image': base64_image, 'text': str(round(gen_time, 3))})

def randStyle(style):
    folder_path = ""
    file_names = ""
    if style == 0:
        folder_path = "./styleImg/ae"
        file_names = os.listdir(folder_path)

    elif style == 1:
        folder_path = "./styleImg/re"
        file_names = os.listdir(folder_path)

    else:
        folder_path = "./styleImg/uki"
        file_names = os.listdir(folder_path)

    random_file_name = random.choice(file_names)
    image_path = os.path.join(folder_path, random_file_name)

    return image_path


@app.route('/transformAll', methods=['POST'])
def transform_all():
    style_file = None
    # Get the uploaded image file
    content_file = request.files['content_image']
    style = ast.literal_eval(request.form['style'])
    if request.files['style_image']:
        style_file = request.files['style_image']
    else:
        style_file = randStyle(style)

    style_gan = [0, 0, 0, 1]
    if style == 0:
        style_gan = [1, 0, 0, 1]
    elif style == 1:
        style_gan = [0, 1, 0, 1]
    elif style == 2:
        style_gan = [0, 0, 1, 1]

    stylized_image_gan, gen_time_gan, _ = generate_image(style_gan, content_file, -1, -1)

    stylized_image_mix, gen_time_mix = generate_image_styleMixer(style_file, content_file)
    buffer_gan = io.BytesIO()
    stylized_image_gan.save(buffer_gan, format='PNG')
    base64_image_gan = base64.b64encode(buffer_gan.getvalue()).decode('utf-8')

    buffer_mix = io.BytesIO()
    stylized_image_mix.save(buffer_mix, format='PNG')
    base64_image_mix = base64.b64encode(buffer_mix.getvalue()).decode('utf-8')
    # Return the base64-encoded string as a JSON response
    return jsonify({'image_gan': base64_image_gan, 'image_mix': base64_image_mix,
                    'text_gan': str(round(gen_time_gan, 3)),
                    'text_mix': str(round(gen_time_mix, 3))})


@app.route('/gated', methods=['GET'])
def gatedGan():
    # modify the upload template accordingly if you need to add new transform method
    return render_template('gatedGan.html')


@app.route('/stylemixer', methods=['GET'])
def stylemixer():
    # modify the upload template accordingly if you need to add new transform method
    return render_template('stylemixer.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/tryall', methods=['GET'])
def tryall():
    return render_template('tryall.html')


if __name__ == '__main__':
    app.run(debug = True)
