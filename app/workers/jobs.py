import asyncio
import uuid
from dataclasses import dataclass
from typing import Optional

from app.clients.api import api_client
from app.services.orchestrator import orchestrator
from app.models import ResearchProject


@dataclass
class MessageJob:
    job_id: str
    project: ResearchProject
    user_content: str
    callback_path: Optional[str] = None


async def handle_message(job: MessageJob) -> None:
    """
    Process a message with the orchestrator and optionally send a callback to the API.
    """
    response_content, thoughts = await orchestrator.process_message(job.project, job.user_content)
    payload = {
        "jobId": job.job_id,
        "projectId": job.project.id,
        "response": response_content,
        "thoughts": [thought.model_dump() for thought in thoughts],
    }
    if job.callback_path:
        await api_client.send_callback(job.callback_path, payload)


async def enqueue_message(queue: asyncio.Queue, project: ResearchProject, user_content: str, callback_path: Optional[str] = None) -> str:
    """
    Enqueue a message job into the in-memory queue. Returns job id.
    """
    job_id = f"job-{uuid.uuid4().hex[:10]}"
    job = MessageJob(job_id=job_id, project=project, user_content=user_content, callback_path=callback_path)
    await queue.put(job)
    return job_id
