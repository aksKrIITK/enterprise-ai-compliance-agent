import pytest


@pytest.mark.asyncio
async def test_run_evaluations_endpoint(async_client):
    response = await async_client.post("/evals/run")
    assert response.status_code == 200
    data = response.json()
    assert data["total_cases"] >= 3
    assert data["pass_rate"] >= 80.0
    assert data["tool_accuracy"] >= 80.0
    assert data["policy_compliance"] == 100.0


@pytest.mark.asyncio
async def test_get_evaluation_results_endpoint(async_client):
    response = await async_client.get("/evals/results")
    assert response.status_code == 200
    data = response.json()
    assert "total_cases" in data
    assert "tool_accuracy" in data
