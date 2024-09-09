# Azure Blob / BackBlaze Most Recent File Time

Displays the date time of the most recent file in a Azure Blob Container and BackBlaze Bluckets (S3 compatible).

The primary purpose of this app is for use with a monitoring tool such as Uptime Kuma to tell if your backups are working.

## Dev Getting Started

```bash
# create a new virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# install requirements
pip install -r requirements.txt

# set required settings either here or via the `.env` file
cp .env-template.txt .env
# OR
# Temporary: Set environment variables for the current session
export AZURE_CONNECTION_STRING="you-connection-string-here"
export AZURE_CONTAINER_NAME="your-container-name"
# etc.. examples for BackBlaze not here, see env tempalte file or app.py
```

Note: I highly recommend using aider.chat

```bash
pip install aider-chat --upgrade

# Work with Claude 3.5 Sonnet on your repo
$ export ANTHROPIC_API_KEY=your-key-goes-here
$ aider

# OR

# Work with GPT-4o on your repo
$ export OPENAI_API_KEY=your-key-goes-here
$ aider 
```

## Docker

To build and run the Docker container:

> You can now use the `deploy.sh` script instead of the below command

```bash
# Build the Docker image
docker build -t azure-blob-latest-file .

# Run the Docker container
docker run -p 5000:5000 -e AZURE_CONNECTION_STRING="your-connection-string-here" -e AZURE_CONTAINER_NAME="your-container-name" azure-blob-latest-file
```

Alternatively, you can use Docker Compose:

```bash
# Build and run the Docker container using Docker Compose
docker-compose up --build
```

## (optional) Upload to Docker Hub

To upload the Docker image to Docker Hub:
(only requied if you need to pull from a docker remote, you can do this locally without this step, see `deploy.sh`)

```bash
# Tag the Docker image
docker tag azure-blob-latest-file your-dockerhub-username/azure-blob-latest-file:latest

# Log in to Docker Hub
docker login --username your-user-name

# Push the Docker image to Docker Hub
docker push your-dockerhub-username/azure-blob-latest-file:latest
```
