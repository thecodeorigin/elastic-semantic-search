echo "Stopping all containers..."
docker compose --profile backend --profile backend-cuda down
echo "Cleaning up resources..."
docker system prune --volumes -a -f
docker volume rm $(docker volume ls -qf dangling=true)
