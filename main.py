import re
from flask_flatpages import FlatPages
from flask import Flask, render_template, send_from_directory, redirect, request


# FLATPAGES CONFIG
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = ".md"
FLATPAGES_ROOT = "static"
ARTICLE_DIR = "articles"

# Article HTML Tag Stripper


def strip_tags(text):
    # safe_text = re.sub(re.compile("<.*?>"), "", text)
    safe_text = re.sub(re.compile("<.*?>BLOCKQUOTE"), "", text)

    return safe_text


# FLASK SERVER
app = Flask(__name__)
flatpages = FlatPages(app)
app.config.from_object(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/articles/")
def articles():
    articles = [a for a in flatpages if a.path.startswith(ARTICLE_DIR)]
    articles.sort(key=lambda item: item["date"], reverse=True)
    return render_template("articles.html", articles=articles, strip_tags=strip_tags)


@app.route("/article/<name>")
def article(name):
    path = "{}/{}".format(ARTICLE_DIR, name)
    article = flatpages.get_or_404(path)
    return render_template("article.html", article=article)


@app.route("/clients/<path:path>")
def serve_clients(path):

    # Check That Only HTML, JS & CSS Files Are Served
    if path[-5:] == ".html":
        pass
    elif path[-4:] == ".css":
        pass
    elif path[-2:] == ".js":
        pass
    else:
        return redirect(404)

    return send_from_directory("static/clients", path)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/robots.txt")
@app.route("/sitemap.xml")
def static_from_root():
    return send_from_directory("./static/bots", request.path[1:])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    # app.run()
