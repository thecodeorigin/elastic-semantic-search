FROM python:3.10-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install poetry and export PATH
RUN pip install poetry==1.3.2
ENV PATH="$HOME/.local/bin:$PATH"

# Create app directory
WORKDIR /app

# Disable virtualenv creation
RUN poetry config virtualenvs.create false
# Set max workers to 10 (default: number of cores + 4), this could cause max connection pool errors
RUN poetry config installer.max-workers 10

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-interaction --no-ansi --no-root --no-cache -vv

# Purge cache as it will make the final image large
RUN pip cache purge && rm -rf ~/.cache/pypoetry/artifacts && rm -rf ~/.cache/pypoetry/cache

# Copy app source
COPY . .

# Load model from Hugging Face
RUN python3 src/cache_model.py

CMD [ "python3", "-m" , "flask", "--app=src/start_be", "run", "--host=0.0.0.0"]
