from flask import Flask, request, render_template
from utils.es_service import ElasticSearchService
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

ES_HOST = str(os.getenv("ES_HOST", "127.0.0.1"))
ES_USERNAME = str(os.getenv("ELASTIC_USERNAME", "elastic"))
ES_PASSWORD = str(os.getenv("ELASTIC_PASSWORD", "changeme"))
host = f"http://{ES_USERNAME}:{ES_PASSWORD}@{ES_HOST}:9200"

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
      return ElasticSearchService(hosts=host).semantic_search(text=query, limit=limit)
    elif method == "fts":
      return ElasticSearchService(hosts=host).fulltext_search(text=query, limit=limit)
    elif method == "fz":
      return ElasticSearchService(hosts=host).fuzzy_search(text=query, limit=limit)
  except Exception as e:
    print(e)
  return {}
