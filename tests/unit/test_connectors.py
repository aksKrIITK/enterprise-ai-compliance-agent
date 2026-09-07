import pytest
from app.connectors.postgres import PostgresConnector
from app.connectors.api import APIConnector
from app.connectors.documents import DocumentConnector


@pytest.mark.asyncio
async def test_postgres_connector():
    connector = PostgresConnector()
    res = await connector.fetch_data({"customer_id": "CUST_1009"})
    assert res.success is True
    assert res.source == "PostgresTransactionConnector"
    assert len(res.data) >= 1
    assert res.data[0]["customer_id"] == "CUST_1009"


@pytest.mark.asyncio
async def test_api_connector():
    connector = APIConnector()
    res = await connector.fetch_data({"customer_id": "CUST_1009"})
    assert res.success is True
    assert res.data["risk_rating"] == "HIGH"
    assert res.data["kyc_verified"] is True


@pytest.mark.asyncio
async def test_document_connector():
    connector = DocumentConnector()
    res = await connector.fetch_data({"query": "AML policy"})
    assert res.success is True
    assert len(res.data) >= 1
    assert "POLICY_AML_2026_V2" in res.data[0]["document_id"]
