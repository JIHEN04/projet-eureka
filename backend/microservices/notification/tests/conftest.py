"""Tests never talk to a real Eureka server."""
import os

os.environ.setdefault("EUREKA_ENABLED", "false")
