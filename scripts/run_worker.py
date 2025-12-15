import asyncio
import os
import signal
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
# Load local env defaults without overriding hosted env vars.
load_dotenv(ROOT_DIR / ".env")
# Ensure project root is on path even if script is launched from elsewhere.
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.workers.queue import QueueWorker
from app.workers.redis_queue import RedisQueueWorker
from app.health import create_health_server


async def main() -> None:
    # Start health server for Railway monitoring
    health_runner = await create_health_server()

    if os.getenv("REDIS_URL"):
        worker = RedisQueueWorker()
        print("Starting orchestrator worker (Redis queue)...")
    else:
        worker = QueueWorker()
        print("Starting orchestrator worker (in-memory queue)...")
    loop = asyncio.get_event_loop()

    # Graceful shutdown
    async def shutdown():
        worker.stop()
        await health_runner.cleanup()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())

