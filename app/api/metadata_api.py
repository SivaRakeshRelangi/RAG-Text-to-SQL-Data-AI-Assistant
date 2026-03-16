from fastapi import APIRouter
from app.metadata.schema_sync import sync_schema
from app.metadata.schema_loader import load_schema

router = APIRouter()

@router.get("/schema")
def get_schema():
    rows = load_schema()
    return {"schema": rows}

@router.post("/sync-schema")
def sync_metadata():
    sync_schema()
    return {"status": "metadata synced"}