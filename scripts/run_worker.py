import asyncio
import signal
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
# Ensure project root is on path even if script is launched from elsewhere.
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.workers.queue import QueueWorker


async def main() -> None:
    worker = QueueWorker()
    loop = asyncio.get_event_loop()

    # Graceful shutdown
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, worker.stop)

    print("Starting orchestrator worker (in-memory queue)...")
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
