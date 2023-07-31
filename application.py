from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
@cross_origin()
def process_image():
    print(1)
    file = request.files['image']
    print(2)
    npimg = np.fromfile(file, np.uint8)
    print(3)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
    edges = cv2.Canny(img,50,150)

    print(4)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(5)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    print(6)
    ret,thresh1 = cv2.threshold(blur,127,255,cv2.THRESH_BINARY_INV)
    print(7)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    print(8)

    contours_info = []
    for contour in contours:
        contour_info = [(int(point[0][0]), int(point[0][1]))
                        for point in contour]
        contours_info.append(contour_info)
        print(9)
    print(10)
    return jsonify(contours_info)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
