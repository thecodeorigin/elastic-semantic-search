import pandas as pd
from utils.elasticsearch import ElasticSearchService

es_service = ElasticSearchService()


if __name__ == "__main__":
  print("Create index")
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
