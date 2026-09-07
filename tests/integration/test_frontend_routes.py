import pytest


@pytest.mark.asyncio
async def test_static_root_endpoint(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    # Checks that HTML content or message is served
    assert "EnterpriseOps" in response.text or "text/html" in response.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_list_investigations_endpoint(async_client):
    # Ensure at least one investigation is posted
    payload = {
        "query": "Investigate compliance status for customer CUST_1009",
        "customer_id": "CUST_1009"
    }
    create_res = await async_client.post("/investigations", json=payload)
    assert create_res.status_code == 200

    # Retrieve list
    list_res = await async_client.get("/investigations")
    assert list_res.status_code == 200
    data = list_res.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(inv["customer_id"] == "CUST_1009" for inv in data)


@pytest.mark.asyncio
async def test_static_files_accessible(async_client):
    css_res = await async_client.get("/static/css/style.css")
    assert css_res.status_code == 200
    assert "--bg-primary" in css_res.text

    js_res = await async_client.get("/static/js/app.js")
    assert js_res.status_code == 200
    assert "DOMContentLoaded" in js_res.text
