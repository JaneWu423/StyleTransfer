from flask import jsonify,Flask, request, render_template, send_file, make_response
from generateImage import generate_image
import io
import base64
import ast


app = Flask(__name__)

@app.route('/transform', methods=['POST'])
def transform():
    # Get the uploaded image file
    file = request.files['image']
    style = ast.literal_eval(request.form['style'])

    # style = [1, 0, 0, 1]
    stylized_image = generate_image(style, file)
    buffer = io.BytesIO()
    stylized_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64-encoded string as a JSON response
    return jsonify({'image': base64_image})

@app.route('/upload', methods=['GET'])
def upload():
    # Get the uploaded file from the request
    # file = request.files['image']
    # style = [1, 0 , 0, 1]
    # stylized_image = generate_image(style, file)
    # transformed_image_file = io.BytesIO()
    # stylized_image.save(transformed_image_file, format='PNG')
    #
    # # Return the transformed image as a response
    # transformed_image_file.seek(0)
    # return send_file(transformed_image_file, mimetype='image/png')


    # Render the result page with the stylized image
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
