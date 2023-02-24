echo "Cleaning up resources..."
docker system prune --volumes -a -f
docker volume rm $(docker volume ls -qf dangling=true)
