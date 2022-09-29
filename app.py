#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, request, \
    render_template, Response
import tools as tools
import csv
from io import BytesIO

ALLOWED_EXTENSIONS = ["txt", "csv"]

# app object
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 512


@app.route("/")
def home():
    # home route
    return render_template("index.html")


@app.route("/bulk")
def bulk():
    # create bulk upload route
    return render_template("bulk.html")


@app.route("/bulk", methods=["POST"])
def upload_bulk_file():

    # find uploaded file object
    uploaded_file = request.files["file"]

    # create file buffer object
    buffer = BytesIO()

    # if filename is valid, insert into buffer
    if tools.allowed_file(uploaded_file.filename, ALLOWED_EXTENSIONS):
        uploaded_file.save(buffer)
        buffer.seek(0)

    reader = csv.reader(buffer.getvalue().decode("UTF-8"))
    data = list(reader)
    print(data[0])

    # return buffer object as downloadable file
    return Response(
        buffer.getvalue(),
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment;filename=results.csv"})


if __name__ == "__main__":
    app.run(debug=True)
