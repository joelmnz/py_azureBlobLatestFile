# Azure Blob Containers Most Recent File Time

Displays the date time of the most recent file in a Azure Blob Container. The primary purpose of this app is for use with a monitoring tool such as Uptime Kuma to tell if your backups are working.

# Dev Getting Started

```bash
# create a new virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# install requirements
pip install -r requirements.txt

# set required settings either here or via the `.env` file
# Temporary: Set environment variables for the current session
export AZURE_CONNECTION_STRING="you-connection-string-here"
export AZURE_CONTAINER_NAME="your-container-name"
```

Note: I highly recommend using aider.chat

```bash
pip install aider-chat --upgrade

# Work with Claude 3.5 Sonnet on your repo
$ export ANTHROPIC_API_KEY=your-key-goes-here
$ aider

# Work with GPT-4o on your repo
$ export OPENAI_API_KEY=your-key-goes-here
$ aider 
```

# Docker

