from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handler():  # put application's code here
    if 'image' not in request.files:
        return 'No file uploaded', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        input_image = Image.open(file.stream)
        output_image = remove(input_image, post_process_mask=True)
        img_io = BytesIO()
        output_image.save(img_io, 'png')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='background_removed.png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
