# controller/task_controller.py

import asyncio
from engine.playwright_engine import run_search
from storage.file_store import save_result
from config.settings import RESULT_PATH

async def process_task(query, callback):
    result = await run_search(query)
    save_result(result, RESULT_PATH)
    callback(result)

def submit_task(query, callback):
    async def task():
        await process_task(query, callback)

    asyncio.create_task(task())