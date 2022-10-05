#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, request, \
    render_template, Response
import tools as tools
import csv
import os
from io import BytesIO, StringIO

ALLOWED_EXTENSIONS = ["txt", "csv"]
MAX_CONTENT_LENGTH = 524288

# app object
app = Flask(__name__)


@app.route("/")
def home():
    # home route
    return render_template("index.html")


@app.route("/", methods=["POST"])
def single_address_finder():
    # single address request route
    text = [request.form['field1_name']]

    try:
        # check address
        address_tup = tools.get_address_values(text)

    except Exception as e:
        zip_codes = f"Oh no! An error occured: {e}"

    else:
        # if address check is a string, return the error
        if isinstance(address_tup[0], str):
            return address_tup[0]

        else:
            # turn tuple of address values into xml
            xml_str = tools.get_xml(address_tup)

            # query with xml
            zip_codes = tools.get_zips(xml_str)

    return render_template("index.html", zip_codes=zip_codes[0])


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

        # if file is too large, go to error page
        if buffer.seek(0, os.SEEK_END) > MAX_CONTENT_LENGTH:
            return render_template("too_large.html")

    else:
        # if file extension is not accepted, go to this page
        return render_template("bad_filename.html")

    # read file into file buffer using csv reader
    reader = csv.reader(buffer.getvalue().decode("UTF-8"))

    # turn reader object into list
    data = list(reader)

    # zip data with numerical range
    zipped_data = list(zip(range(0, len(data)), data))

    # create empty dict for new data
    data_dict = {}

    # loop through zipped data and query each address
    for tupe in zipped_data:
        if tupe[1]:
            data_dict[tupe[0]] = [tupe[1][0], "new_val"]

    # create string file buffer
    csvfile = StringIO()
    writer = csv.writer(csvfile)

    # parse values from data_dict into file buffer
    for value in data_dict.values():
        writer.writerow([value[0], value[1]])

    # go to start of string file buffer
    csvfile.seek(0)

    # return buffer object as downloadable file
    return Response(
        csvfile.getvalue(),
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment;filename=results.csv"}), \
        buffer.close(), \
        csvfile.close()


if __name__ == "__main__":
    app.run(debug=True)
