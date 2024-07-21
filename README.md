# Azure Blob Containers Most Recent File Time

Displays the date time of the most recent file in a Azure Blob Container

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
```

# Docker

