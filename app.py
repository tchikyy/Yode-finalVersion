"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import base64 
from flask_ngrok import run_with_ngrok

import torch
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
run_with_ngrok(app) 

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model(img, size=416)

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_byte_arr = io.BytesIO()
            img_base64.save(img_byte_arr, format='JPEG')
            imgg = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        return render_template("index.html", img_data=imgg)

    return render_template("index.html")

@app.route("/feed", methods=["POST"])
def feedback():
    t="thnx for the feed-back :)"
    return render_template("index.html", text=t);

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load(
        "ultralytics/yolov5", "custom", path="best.pt", force_reload=True
    ).autoshape()  # force_reload = recache latest code
    model.eval()
    app.run()  # debug=True causes Restarting with stat
