import pytest
from app.tools.transactions import TransactionSearchTool
from app.tools.customers import CustomerProfileTool
from app.tools.risk import RiskScoringTool
from app.tools.knowledge import CompliancePolicySearchTool
from app.tools.case_management import CaseManagementTool


@pytest.mark.asyncio
async def test_transaction_search_tool():
    tool = TransactionSearchTool()
    result = await tool.run(customer_id="CUST_1009")
    assert result.success is True
    assert result.tool_name == "transaction_search"
    assert len(result.data) > 0


@pytest.mark.asyncio
async def test_customer_profile_tool():
    tool = CustomerProfileTool()
    result = await tool.run(customer_id="CUST_1009")
    assert result.success is True
    assert result.tool_name == "customer_profile"
    assert result.data["customer_id"] == "CUST_1009"


@pytest.mark.asyncio
async def test_risk_scoring_tool():
    tool = RiskScoringTool()
    mock_txns = [
        {"amount": 60000, "country": "Cayman Islands", "flagged": True},
        {"amount": 12000, "country": "India", "flagged": True}
    ]
    result = await tool.run(transactions=mock_txns)
    assert result.success is True
    assert result.data["risk_level"] == "HIGH"
    assert result.data["risk_score"] > 0.8


@pytest.mark.asyncio
async def test_compliance_policy_search_tool():
    tool = CompliancePolicySearchTool()
    result = await tool.run(query="suspicious transactions")
    assert result.success is True
    assert len(result.data) > 0


@pytest.mark.asyncio
async def test_case_management_tool():
    tool = CaseManagementTool()
    result = await tool.run(customer_id="CUST_1009", risk_level="HIGH", summary="Flagged transactions detected")
    assert result.success is True
    assert "CASE-" in result.data["case_id"]
    assert result.data["risk_level"] == "HIGH"


@pytest.mark.asyncio
async def test_tool_invalid_arguments():
    tool = TransactionSearchTool()
    # Missing required argument customer_id
    result = await tool.run()
    assert result.success is False
    assert "validation" in result.error.lower() or "missing" in result.error.lower()
