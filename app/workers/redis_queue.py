import json
import os
from typing import Optional

from redis.asyncio import Redis

from app.models import ResearchProject
from app.workers.jobs import MessageJob, handle_message


QUEUE_KEY = os.getenv("ORCHESTRATOR_QUEUE_KEY", "intellex:message_jobs")


class RedisQueueWorker:
    def __init__(self, redis_url: Optional[str] = None, queue_key: str = QUEUE_KEY):
        redis_url = redis_url or os.getenv("REDIS_URL")
        if not redis_url:
            raise ValueError("REDIS_URL is required for RedisQueueWorker")
        self.queue_key = queue_key
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self._running = False

    async def start(self) -> None:
        self._running = True
        while self._running:
            item = await self.redis.blpop(self.queue_key, timeout=1)
            if not item:
                continue
            _, raw = item
            try:
                data = json.loads(raw)
                project = ResearchProject(**(data.get("project") or {}))
                job = MessageJob(
                    job_id=data.get("jobId") or data.get("job_id"),
                    project=project,
                    user_content=data.get("userContent") or data.get("user_content") or "",
                    callback_path=data.get("callbackPath") or data.get("callback_path"),
                    agent_message_id=data.get("agentMessageId") or data.get("agent_message_id"),
                )
                await handle_message(job)
            except Exception as exc:  # pragma: no cover - runtime guard
                print(f"Failed to process redis job: {exc}")

        await self.redis.aclose()

    def stop(self) -> None:
        self._running = False

