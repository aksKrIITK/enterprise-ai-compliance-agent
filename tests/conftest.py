import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_db_health_healthy():
    with patch("app.api.routes.check_database_health", new_callable=AsyncMock) as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_db_health_unhealthy():
    with patch("app.api.routes.check_database_health", new_callable=AsyncMock) as mock:
        mock.return_value = False
        yield mock


@pytest.fixture
def mock_redis_health_healthy():
    with patch("app.api.routes.check_redis_health", new_callable=AsyncMock) as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_redis_health_unhealthy():
    with patch("app.api.routes.check_redis_health", new_callable=AsyncMock) as mock:
        mock.return_value = False
        yield mock
