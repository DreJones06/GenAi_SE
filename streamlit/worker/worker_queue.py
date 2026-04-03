# worker/worker_queue.py

import asyncio

task_queue = asyncio.Queue()

async def worker():
    while True:
        task = await task_queue.get()
        await task()
        task_queue.task_done()

def start_worker_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(worker())