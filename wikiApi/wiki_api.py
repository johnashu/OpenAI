from flask import Flask, render_template, request
import requests
import json  # Imported but not used.

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form["search_term"]
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_term}&format=json"  # F-String formatted
    r = requests.get(search_url)
    data = r.json()
    search_results = data["query"]["search"]
    search_results[0].update(
        {"term": search_term}
    )  # Search term added to display in the html
    return render_template("results.html", search_results=search_results)


@app.route("/page/<pageid>")
def page(pageid):
    page_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={pageid}&format=json&explaintext"  # F-String formatted
    r = requests.get(page_url)
    data = r.json()
    page_content = data["query"]["pages"][pageid]["extract"]
    return render_template("page.html", page_content=page_content)


if __name__ == "__main__":
    app.run(debug=True)
