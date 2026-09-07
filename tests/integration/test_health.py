import pytest


@pytest.mark.asyncio
async def test_health_check_healthy(async_client, mock_db_health_healthy, mock_redis_health_healthy):
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["database"] is True
    assert data["services"]["redis"] is True
    assert "version" in data


@pytest.mark.asyncio
async def test_health_check_degraded(async_client, mock_db_health_unhealthy, mock_redis_health_healthy):
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["services"]["database"] is False
    assert data["services"]["redis"] is True


@pytest.mark.asyncio
async def test_liveness_check(async_client):
    response = await async_client.get("/health/liveness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_readiness_check_healthy(async_client, mock_db_health_healthy, mock_redis_health_healthy):
    response = await async_client.get("/health/readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.asyncio
async def test_readiness_check_unhealthy(async_client, mock_db_health_unhealthy, mock_redis_health_healthy):
    response = await async_client.get("/health/readiness")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "unready"


@pytest.mark.asyncio
async def test_correlation_id_middleware(async_client, mock_db_health_healthy, mock_redis_health_healthy):
    custom_correlation_id = "test-corr-12345"
    response = await async_client.get("/health", headers={"X-Correlation-ID": custom_correlation_id})
    assert response.headers.get("X-Correlation-ID") == custom_correlation_id
