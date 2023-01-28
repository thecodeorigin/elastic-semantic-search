from flask import Flask, request, render_template
from utils.elasticsearch import ElasticSearchService

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
  try:
    query = request.args.get("q", "")
    if not query:
      return {}
    return ElasticSearchService().semantic_search(text=query)
  except Exception as e:
    print("Encountered exception while search")
    print(e)
    return {}
