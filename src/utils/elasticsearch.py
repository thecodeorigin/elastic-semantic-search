from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from utils.vectorize import Vectorize


class ElasticSearchService:
  def __init__(self):
    self._index_name = "demo_simcse"
    self._client = Elasticsearch(hosts="http://127.0.0.1:9200")

  def create_index(self, mapping: dict):
    self._client.options(ignore_status=[404]).indices.delete(index=self._index_name)
    self._client.indices.create(index=self._index_name, mappings=mapping)

  def refresh_index(self):
    self._client.indices.refresh(index=self._index_name)

  def bulk_index_data(self, docs: list):
    requests = []
    titles = [doc["title"] for doc in docs]
    title_vectors = Vectorize(sentences=titles).handle()

    for i, doc in enumerate(docs):
        request = doc
        request["_op_type"] = "index"
        request["_index"] = self._index_name
        request["title_vector"] = title_vectors[i]
        requests.append(request)
    bulk(self._client, requests)

  def semantic_search(self, text: str, limit: int = 100):
    vectors = Vectorize(sentences=[text]).handle()
    query_vector = vectors[0]
    script_query = {
      "script_score": {
          "query": {
              "match_all": {}
          },
          "script": {
            "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
            "params": {"query_vector": query_vector}
          }
      }
    }
    response = self._client.options(ignore_status=[404]).search(
      index=self._index_name,
      size=limit,
      query=script_query,
      source={
        "includes": ["id", "title"]
      },
    )
    result = []
    response_time = response['took']

    for hit in response["hits"]["hits"]:
        result.append(hit["_source"]['title'])
    return {
      "response_time": response_time,
      "result": result
    }
