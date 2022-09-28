#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tools as tools
import os


UPLOAD_FOLDER = "/static"
ALLOWED_EXTENSIONS = {"txt", "csv", "xlsx"}

# app object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    # home route
    return render_template("index.html")


@app.route("/bulk", methods=["GET", "POST"])
def bulk():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and tools.allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOADER_FOLDER"], filename))
            return redirect(url_for('download_file', name=filename))

    return render_template("bulk.html")


if __name__ == "__main__":
    app.run()
