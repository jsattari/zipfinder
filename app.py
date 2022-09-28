#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, request, \
    redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import tools as tools
import os
import csv

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = ["txt", "csv"]

# app object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 10


@app.route("/")
def home():
    # home route
    return render_template("index.html")


@app.route("/bulk")
def bulk():
    return render_template("bulk.html")


@app.route("/bulk", methods=["POST"])
def upload_bulk_file():
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)

    if tools.allowed_file(filename, ALLOWED_EXTENSIONS):
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for("bulk"))


@app.route('/uploads/<filename>')
def upload(filename):

    with open(
        os.path.join(
            app.config['UPLOAD_FOLDER'], filename), "r") as data_file:

        reader = csv.reader(data_file)
        data = dict(reader)

        print(data)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
