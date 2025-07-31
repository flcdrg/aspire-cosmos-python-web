# Python App - Cosmos DB API

This is a FastAPI application that connects to Azure Cosmos DB and provides a REST API for managing items.

## Features

- Connects to Azure Cosmos DB (or emulator)
- Creates database and container automatically on startup
- Adds a sample entity if the container is empty
- REST API endpoints for managing items
- Health check endpoint

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Azure Cosmos DB or Cosmos DB Emulator

## Getting Started

### Install dependencies

```bash
uv sync
```

### Run the application

```bash
uv run python main.py
```

Or using the script:

```bash
uv run start
```

### Run with Aspire

This application is designed to work with .NET Aspire. Run the entire application stack:

```bash
cd ../AspireCosmosPythonWeb.AppHost
dotnet run
```

## API Endpoints

- `GET /` - Root endpoint with basic information
- `GET /items` - Get all items from the container
- `GET /items/{item_id}` - Get a specific item by ID
- `POST /items` - Create a new item
- `GET /health` - Health check endpoint

## Environment Variables

When running with Aspire, the following environment variables are automatically configured:

- `ConnectionStrings__cosmos-db__AccountEndpoint` - Cosmos DB endpoint
- `ConnectionStrings__cosmos-db__AccountKey` - Cosmos DB key
- `PORT` - Port number for the application

## Development

The application uses the following Python packages:

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `azure-cosmos` - Azure Cosmos DB client
- `opentelemetry-*` - Observability and telemetry (for Aspire integration)