"""Eureka client configuration (py-eureka-client).

The service registers itself under the name NOTIFICATION when FastAPI starts
(lifespan startup) and is removed from Eureka when FastAPI stops (lifespan shutdown).

Environment variables (all optional):
    PORT           port of this instance                    (default 8084)
    EUREKA_SERVER  URL of the Eureka server                 (default http://localhost:8761/eureka)
    INSTANCE_HOST  host name published in Eureka            (default localhost)
    INSTANCE_IP    IP address published in Eureka           (default 127.0.0.1)
    EUREKA_ENABLED set to "false" to disable registration   (default true)
"""
import logging
import os

import py_eureka_client.eureka_client as eureka_client

logger = logging.getLogger("uvicorn.error")

APP_NAME = "NOTIFICATION"


def get_port() -> int:
    return int(os.getenv("PORT", "8084"))


def get_eureka_server() -> str:
    return os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")


def is_enabled() -> bool:
    return os.getenv("EUREKA_ENABLED", "true").lower() != "false"


async def register() -> None:
    """Register this instance in Eureka (called at application startup)."""
    if not is_enabled():
        logger.info("Eureka registration disabled (EUREKA_ENABLED=false)")
        return

    host = os.getenv("INSTANCE_HOST", "localhost")
    port = get_port()
    try:
        await eureka_client.init_async(
            eureka_server=get_eureka_server(),
            app_name=APP_NAME,
            instance_id=f"{host}:{APP_NAME.lower()}:{port}",
            instance_host=host,
            instance_ip=os.getenv("INSTANCE_IP", "127.0.0.1"),
            instance_port=port,
            status_page_url=f"http://{host}:{port}/api/notifications/hello",
            health_check_url=f"http://{host}:{port}/api/notifications/hello",
            home_page_url=f"http://{host}:{port}/",
            # keep the service running even if Eureka is not started yet
            should_discover=True,
        )
        logger.info("Registered in Eureka as %s on port %s", APP_NAME, port)
    except Exception as exc:  # the service must still answer if Eureka is down
        logger.error("Eureka registration failed: %s", exc)


async def unregister() -> None:
    """Stop the Eureka client (deregisters the instance) at application shutdown."""
    if not is_enabled():
        return
    try:
        await eureka_client.stop_async()
        logger.info("Eureka client stopped")
    except Exception as exc:
        logger.error("Eureka client stop failed: %s", exc)
