import asyncio
from app.services.query_service import process_query

query_queue = asyncio.Queue()

async def worker():

    while True:

        question, future = await query_queue.get()

        try:
            result = process_query(question)
            future.set_result(result)

        except Exception as e:
            future.set_exception(e)

        finally:
            query_queue.task_done()