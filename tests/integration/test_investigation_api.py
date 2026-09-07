import pytest


@pytest.mark.asyncio
async def test_investigation_endpoint(async_client):
    payload = {
        "query": "Investigate whether transaction for CUST_1009 should be flagged for suspicious activity and provide evidence.",
        "customer_id": "CUST_1009"
    }
    response = await async_client.post("/investigations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert data["customer_id"] == "CUST_1009"
    assert data["risk_level"] == "HIGH"
    assert data["human_review_task_id"] is not None


@pytest.mark.asyncio
async def test_get_investigation_details(async_client):
    payload = {
        "query": "Investigate customer CUST_1009",
        "customer_id": "CUST_1009"
    }
    create_res = await async_client.post("/investigations", json=payload)
    req_id = create_res.json()["request_id"]

    details_res = await async_client.get(f"/investigations/{req_id}")
    assert details_res.status_code == 200
    details_data = details_res.json()
    assert details_data["request_id"] == req_id


@pytest.mark.asyncio
async def test_human_review_workflow(async_client):
    # 1. List pending tasks
    tasks_res = await async_client.get("/human-review/tasks")
    assert tasks_res.status_code == 200
    tasks = tasks_res.json()
    assert len(tasks) > 0

    target_task_id = tasks[0]["task_id"]

    # 2. Submit decision
    decision_payload = {
        "decision": "APPROVED",
        "notes": "Verified evidence and offshore SWIFT transfer. Approved for SAR filing."
    }
    decision_res = await async_client.post(f"/human-review/{target_task_id}/decision", json=decision_payload)
    assert decision_res.status_code == 200
    updated_task = decision_res.json()
    assert updated_task["status"] == "APPROVED"
    assert updated_task["decision_notes"] == decision_payload["notes"]
