from utils.es_service import ElasticSearchService
import pandas as pd
import os
from dotenv import load_dotenv
import sys

sys.tracebacklimit = 0

if __name__ == "__main__":
  try:
    load_dotenv()
    ES_HOST = str(os.getenv("ES_HOST", "127.0.0.1"))
    ES_USERNAME = str(os.getenv("ELASTIC_USERNAME", "elastic"))
    ES_PASSWORD = str(os.getenv("ELASTIC_PASSWORD", "changeme"))
    host = f"http://{ES_USERNAME}:{ES_PASSWORD}@{ES_HOST}:9200"
    print(f"Establishing connection to {host}")
    es_service = ElasticSearchService(hosts=host)
    print("1. Create index")

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
    print("2. Start indexing")

    docs = []
    count = 0

    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(current_dir, 'data', 'title.csv')
    df = pd.read_csv(data_folder).fillna(' ')

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
    print("3. Finished indexing")
  except KeyboardInterrupt:
    print("Indexing interrupted")
