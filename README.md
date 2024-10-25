# RAG Pipeline with Haystack and OpenAI

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline using Haystack and OpenAI. It's designed to process and analyze tweet data, allowing users to ask questions about the content and receive AI-generated answers based on the relevant information retrieved from the tweet database.

## Features

- File upload functionality for tweet data
- RAG pipeline implementation using Haystack
- OpenAI integration for embeddings and text generation
- FastAPI backend for handling API requests
- Containerized application using Docker

## Project Structure

```
.
├── app
│   ├── apis
│   │   └── routers.py
│   ├── core
│   │   ├── app_factory.py
│   │   └── config.py
│   ├── haystack
│   │   └── haystack.py
│   ├── services
│   │   └── services.py
│   └── main.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a `.env` file in the root directory with the following content:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PROJECT_NAME=YourProjectName
   UPLOAD_DIR=path/to/upload/directory
   ```

3. Build and run the Docker container:
   ```
   docker build -t rag-pipeline .
   docker run -p 3000:3000 rag-pipeline
   ```

## Usage

The application exposes the following API endpoints:

1. File Upload:
   - Endpoint: `POST /upload`
   - Description: Upload a file containing tweet data

2. Ask Question:
   - Endpoint: `POST /ask`
   - Description: Ask a question about the uploaded tweet data

For detailed API documentation, visit `http://localhost:3000/docs` after starting the application.

## Core Components

### RAG Class

The RAG class (defined in `app/haystack/haystack.py`) is the core of the pipeline:

```python:app/haystack/haystack.py
startLine: 19
endLine: 70
```

This class handles document embedding, indexing, and query processing.

### Service Class

The Service class (defined in `app/services/services.py`) manages file uploads and question answering:

```python:app/services/services.py
startLine: 14
endLine: 40
```

### FastAPI Application

The FastAPI application is set up in `app/core/app_factory.py`:

```python:app/core/app_factory.py
startLine: 6
endLine: 33
```

## Configuration

The application configuration is managed using Pydantic's BaseSettings:

```python:app/core/config.py
startLine: 1
endLine: 8
```

## Logging

Logging is configured in `app/main.py`:

```python:app/main.py
startLine: 1
endLine: 10
```

## Docker Configuration

The application is containerized using Docker. The Dockerfile is located in the root directory:

```Dockerfile
# Use the official Python image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install the required system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Command to run the application  
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
```

## Contributing

Contributions to this project are welcome. Please ensure that you follow the existing code style and include appropriate tests for any new features.