echo "Starting all containers (without CUDA)"
docker compose --profile backend up -d --build
echo "Indexing data to ElasticSearch, this may take a while... (Press Ctrl+C to stop)"

until docker exec -it es-semantic-flask bash -c "python3 index_es.py"
do
  echo "Failed to index...Retrying in 10 seconds..."
  sleep 10
done
