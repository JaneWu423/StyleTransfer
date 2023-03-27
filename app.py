from flask import jsonify, Flask, request, render_template
from gatedGan.generateImage import generate_image
from stylebank.transform import transformImage
import io
import base64
import ast

app = Flask(__name__)


# route only for gatedGan transform
@app.route('/stylebankTransform', methods=['POST'])
def transform():
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
    style = [ab, uki, re, 1]
    stylized_image = generate_image(style, file)
    buffer = io.BytesIO()
    stylized_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64-encoded string as a JSON response
    return jsonify({'image': base64_image})


@app.route('/stylebank', methods=['GET'])
def upload():
    # modify the upload template accordingly if you need to add new transform method
    return render_template('stylebank.html')


@app.route('/gated', methods=['GET'])
def gatedGan():
    # modify the upload template accordingly if you need to add new transform method
    return render_template('gatedGan.html')


if __name__ == '__main__':
    app.run()
