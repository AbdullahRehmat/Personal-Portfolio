from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/robots.txt")
@app.route("/sitemap.xml")
def static_from_root():
    return send_from_directory("./static/bots", request.path[1:])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    #app.run()
