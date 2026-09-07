import structlog
from app.core.logging import setup_logging, add_opentelemetry_context


def test_setup_logging_runs_without_error():
    setup_logging()
    logger = structlog.get_logger()
    assert logger is not None


def test_add_opentelemetry_context():
    event = {"event": "test_event"}
    processed_event = add_opentelemetry_context(None, "info", event.copy())
    assert "event" in processed_event
