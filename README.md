# Semantic search in ElasticSearch using PhoBert

This is a simple implementation of semantic search into Elasticsearch:

- In this demo, we will use [PhoBert](https://www.aclweb.org/anthology/2020.findings-emnlp.92/), a pre-trained language models made specially for Vietnamese language.

- Including in this demo is also a simple Flask server for you to have a quick demo on what the results would be.

## Prerequisites

- Ubuntu (Recommended)
- [Docker](https://docs.docker.com/desktop/install/linux-install)

If you are planning to run the Flask app locally, you also need

- Python 3.10 or above (Recommended installing by [pyenv](https://github.com/pyenv/pyenv))
- [Poetry](https://python-poetry.org)

## Installation

### Quickstart

#### Start every services (Elasticsearch + Kibana + Flask server)

_The final image may take up to ~7GB and it can take some time to finish building._

```zsh
# Without CUDA
sh cmd.run.all.sh

# With CUDA
sh cmd.run.all-cuda.sh
```

#### Stop all services

```zsh
sh cmd.stop.all.sh
```

#### Index data to Elasicsearch (Using Docker)

_This process can take a long time as it is indexing over 100000, you can try reducing the file size manually._

```zsh
docker exec -it es-semantic-flask python3 index_es.py
```

#### You may need this (lol)

```zsh
docker system prune -a
```

### Lightweight (Without Flask on Docker)

#### Start core service (Elasticsearch + Kibana)

```zsh
sh cmd.run.core.sh
```

#### Install required packages

```zsh
poetry install
```

#### Load model locally

```zsh
python src/utils/loadmodel.py
```

#### Index data to Elasicsearch (Using Python)

_This process can take a long time as it is indexing over 100000, you can try reducing the file size manually._

```zsh
python src/index_es.py
```

#### Start Flask server

```zsh
python3 -m flask --app=app run --host=0.0.0.0
```

## Usage

Access the site at <http://127.0.0.1:5000>

## Contact

Email: quangtupct@gmail.com

Facebook: [fb.com/tu.nguyenquang01](fb.com/tu.nguyenquang01)

Linkedin: [linkedin.com/in/quangtudng](linkedin.com/in/quangtudng)
