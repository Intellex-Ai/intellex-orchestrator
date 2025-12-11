import asyncio
import signal

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
