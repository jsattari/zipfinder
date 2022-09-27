from flask import Flask, render_template

# app object
app = Flask(__name__)


@app.route("/")
def home():
    # home route
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
