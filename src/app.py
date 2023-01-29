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

@app.route("/index", methods=["POST"])
def index_data():
  print("Create index")
  es_service = ElasticSearchService()
  es_service.create_index(mapping={
    "properties": {
      "id": {
        "type": "text"
      },
      "title": {
        "type": "text"
      },
      "title_vector": {
        "type": "dense_vector",
        "dims": 768
      }
    }
  })
  print("Start indexing...")

  docs = []
  count = 0
  df = pd.read_csv("data/title.csv").fillna(' ')

  for _, row in df.iterrows():
    count += 1
    item = {
      'id': row['id'],
      'title': row['title']
    }
    docs.append(item)
    if count % 1000 == 0:
      es_service.bulk_index_data(docs=docs)
      es_service.refresh_index()
      docs = []
      print("Indexed {} documents.".format(count))
  print("Finished indexing")

@app.route("/cache-model", methods=["POST"])
def cache_model():
  print("Caching model...")
  Vectorize(sentences=["hehe"]).handle()
  print("Finished caching model")
