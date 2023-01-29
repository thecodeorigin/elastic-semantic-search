from utils.es_service import ElasticSearchService
import pandas as pd
import os

if __name__ == "__main__":
  print("1. Create index")
  es_service = ElasticSearchService(hosts="http://127.0.0.1:9200")
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
