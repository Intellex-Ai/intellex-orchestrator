"""Lightweight health check server for monitoring."""
import os
from aiohttp import web


async def health_handler(request: web.Request) -> web.Response:
    """Return basic health status."""
    return web.json_response({
        "status": "ok",
        "service": "intellex-orchestrator",
    })


async def create_health_server() -> web.AppRunner:
    """Create and return a health check server runner."""
    app = web.Application()
    app.router.add_get("/health", health_handler)
    app.router.add_get("/", health_handler)  # Root for Railway health checks
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    print(f"Health server listening on port {port}")
    return runner
