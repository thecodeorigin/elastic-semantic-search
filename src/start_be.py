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
    method = request.args.get("method", "semantic")
    limit = request.args.get("limit", 100)
    if method == "sts":
      return ElasticSearchService().semantic_search(text=query, limit=limit)
    elif method == "fts":
      return ElasticSearchService().fulltext_search(text=query, limit=limit)
    elif method == "fz":
      return ElasticSearchService().fuzzy_search(text=query, limit=limit)
  except Exception as e:
    print(e)
  return {}
