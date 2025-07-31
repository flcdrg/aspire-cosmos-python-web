import os
import asyncio
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError
import uvicorn


# Configuration - these will be provided by Aspire
COSMOS_ENDPOINT = os.getenv("ConnectionStrings__cosmos-db__AccountEndpoint", "https://localhost:8081")
COSMOS_KEY = os.getenv("ConnectionStrings__cosmos-db__AccountKey", "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==")
DATABASE_NAME = "SampleDB"
CONTAINER_NAME = "Items"

app = FastAPI(title="Cosmos DB API", description="Simple REST API for Azure Cosmos DB")

# Global variables
cosmos_client = None
database = None
container = None


async def init_cosmos_db():
    """Initialize Cosmos DB connection and create database/container if they don't exist"""
    global cosmos_client, database, container
    
    try:
        print(f"Connecting to Cosmos DB at: {COSMOS_ENDPOINT}")
        
        # Create Cosmos client
        cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
        
        # Create database if it doesn't exist
        database = cosmos_client.create_database_if_not_exists(id=DATABASE_NAME)
        print(f"Database '{DATABASE_NAME}' created or already exists")
        
        # Create container if it doesn't exist
        container = database.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )
        print(f"Container '{CONTAINER_NAME}' created or already exists")
        
        # Add sample entity if container is empty
        await add_sample_entity()
        
    except Exception as e:
        print(f"Error initializing Cosmos DB: {e}")
        raise


async def add_sample_entity():
    """Add a sample entity to the container if it's empty"""
    try:
        # Check if container has any items
        query = "SELECT VALUE COUNT(1) FROM c"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        count = items[0] if items else 0
        
        if count == 0:
            sample_entity = {
                "id": "sample-1",
                "name": "Sample Item",
                "description": "This is a sample entity created on startup",
                "category": "demo",
                "created_at": "2025-07-31T00:00:00Z"
            }
            
            container.create_item(body=sample_entity)
            print("Sample entity added to container")
        else:
            print(f"Container already contains {count} item(s)")
            
    except Exception as e:
        print(f"Error adding sample entity: {e}")


@app.on_event("startup")
async def startup_event():
    """Initialize Cosmos DB on application startup"""
    print("Starting up Python API...")
    print(f"Environment variables:")
    for key, value in os.environ.items():
        if "cosmos" in key.lower() or "connection" in key.lower():
            print(f"  {key}={value}")
    await init_cosmos_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Cosmos DB API is running", "database": DATABASE_NAME, "container": CONTAINER_NAME}


@app.get("/items", response_model=List[Dict[str, Any]])
async def get_all_items():
    """Get all items from the Cosmos DB container"""
    try:
        if not container:
            raise HTTPException(status_code=500, detail="Cosmos DB not initialized")
        
        query = "SELECT * FROM c"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        return items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving items: {str(e)}")


@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """Get a specific item by ID"""
    try:
        if not container:
            raise HTTPException(status_code=500, detail="Cosmos DB not initialized")
        
        item = container.read_item(item=item_id, partition_key=item_id)
        return item
        
    except CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail=f"Item with id '{item_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving item: {str(e)}")


@app.post("/items")
async def create_item(item: Dict[str, Any]):
    """Create a new item in the container"""
    try:
        if not container:
            raise HTTPException(status_code=500, detail="Cosmos DB not initialized")
        
        # Ensure the item has an id
        if "id" not in item:
            raise HTTPException(status_code=400, detail="Item must have an 'id' field")
        
        created_item = container.create_item(body=item)
        return created_item
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating item: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        if not cosmos_client or not database or not container:
            return {"status": "unhealthy", "reason": "Cosmos DB not properly initialized"}
        
        # Simple query to test connection
        query = "SELECT VALUE COUNT(1) FROM c"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        count = items[0] if items else 0
        
        return {
            "status": "healthy",
            "database": DATABASE_NAME,
            "container": CONTAINER_NAME,
            "item_count": count
        }
    except Exception as e:
        return {"status": "unhealthy", "reason": str(e)}


def main():
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting Cosmos DB Python API on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
