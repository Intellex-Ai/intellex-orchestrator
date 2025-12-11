import os
import uuid
from typing import Any, Optional

import httpx


COMMUNICATIONS_BASE_URL = os.getenv("COMMUNICATIONS_BASE_URL")
COMMUNICATIONS_SEND_PATH = os.getenv("COMMUNICATIONS_SEND_PATH", "/send")


async def send_email(
    to: str,
    template: str,
    data: dict[str, Any],
    subject: Optional[str] = None,
    metadata: Optional[dict[str, Any]] = None,
    callback_url: Optional[str] = None,
) -> None:
    if not COMMUNICATIONS_BASE_URL:
        return

    payload = {
        "id": f"send-{uuid.uuid4().hex[:8]}",
        "channel": "email",
        "template": template,
        "to": to,
        "subject": subject,
        "data": data,
        "metadata": metadata,
        "callbackUrl": callback_url,
    }

    try:
        url = f"{COMMUNICATIONS_BASE_URL.rstrip('/')}{COMMUNICATIONS_SEND_PATH}"
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(url, json=payload)
    except Exception as exc:  # pragma: no cover - best-effort
        print(f"Communications send failed: {exc}")

