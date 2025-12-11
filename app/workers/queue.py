import asyncio
from typing import Optional

from app.workers.jobs import MessageJob, handle_message


class QueueWorker:
    def __init__(self, queue: Optional[asyncio.Queue] = None):
        self.queue: asyncio.Queue = queue or asyncio.Queue()
        self._running = False

    async def start(self) -> None:
        self._running = True
        while self._running:
            job = await self.queue.get()
            try:
                await self._dispatch(job)
            except Exception as exc:  # pragma: no cover - runtime guard
                print(f"Job failed: {exc}")
            finally:
                self.queue.task_done()

    async def _dispatch(self, job: MessageJob) -> None:
        await handle_message(job)

    def stop(self) -> None:
        self._running = False
