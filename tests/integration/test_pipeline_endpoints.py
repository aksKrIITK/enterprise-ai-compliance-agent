import pytest


@pytest.mark.asyncio
async def test_investigate_endpoint(async_client):
    payload = {
        "query": "Investigate whether customer CUST_1009 should be flagged for suspicious activity.",
        "customer_id": "CUST_1009"
    }
    response = await async_client.post("/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert data["customer_id"] == "CUST_1009"
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert "summary" in data


@pytest.mark.asyncio
async def test_document_ingest_endpoint(async_client):
    payload = {
        "document_id": "policy_test_99",
        "title": "Automated Test Compliance Directive",
        "content": "All offshore transactions above 10000 USD require immediate FinCEN escalation and enhanced identity verification.",
        "department": "compliance",
        "country": "India",
        "version": "2026",
        "sensitivity": "confidential"
    }
    response = await async_client.post("/documents/ingest", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["document_id"] == "policy_test_99"
    assert data["chunks_created"] >= 1
    assert data["status"] == "INGESTED"


@pytest.mark.asyncio
async def test_trace_observability_endpoints(async_client):
    # 1. Trigger an investigation to produce a trace
    payload = {
        "query": "Trace telemetry verification for CUST_1009",
        "customer_id": "CUST_1009"
    }
    inv_res = await async_client.post("/investigate", json=payload)
    assert inv_res.status_code == 200
    req_id = inv_res.json()["request_id"]

    # Retrieve detailed investigation to get trace_id
    detail_res = await async_client.get(f"/investigations/{req_id}")
    trace_id = detail_res.json()["trace_id"]

    # 2. Get trace by trace_id
    trace_res = await async_client.get(f"/traces/{trace_id}")
    assert trace_res.status_code == 200
    trace_data = trace_res.json()
    assert trace_data["trace_id"] == trace_id
    assert trace_data["request_id"] == req_id
    assert len(trace_data["spans"]) >= 3

    # 3. List all traces
    traces_list_res = await async_client.get("/traces")
    assert traces_list_res.status_code == 200
    traces = traces_list_res.json()
    assert isinstance(traces, list)
    assert any(t["trace_id"] == trace_id for t in traces)


@pytest.mark.asyncio
async def test_direct_human_review_task_id_route(async_client):
    # Retrieve pending tasks
    tasks_res = await async_client.get("/human-review/tasks")
    tasks = tasks_res.json()
    assert len(tasks) > 0
    target_id = tasks[0]["task_id"]

    # Submit decision to direct /human-review/{task_id}
    decision_payload = {
        "decision": "APPROVED",
        "notes": "Direct human review endpoint verification"
    }
    res = await async_client.post(f"/human-review/{target_id}", json=decision_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "APPROVED"
    assert data["decision_notes"] == "Direct human review endpoint verification"
