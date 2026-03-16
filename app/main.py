import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag.index_schema import index_schema
from app.api.metadata_api import router as metadata_router
from app.metadata.schema_sync import start_sync_background
from app.services.query_queue import worker, query_queue

app = FastAPI()

app.include_router(metadata_router, prefix="/metadata")

class Query(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():

    index_schema()
    start_sync_background()

    asyncio.create_task(worker())

@app.post("/query")
async def query(q: Query):

    try:

        loop = asyncio.get_event_loop()

        future = loop.create_future()

        await query_queue.put((q.question, future))

        result = await future

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))