import pytest
import uuid
from app.graph.workflow import investigation_graph
from app.graph.state import InvestigationState


@pytest.mark.asyncio
async def test_langgraph_happy_path_workflow():
    initial_state: InvestigationState = {
        "request_id": f"REQ-{uuid.uuid4().hex[:8]}",
        "user_query": "Investigate whether transaction for CUST_1009 should be flagged for suspicious activity and provide evidence.",
        "customer_id": "CUST_1009",
        "investigation_plan": [],
        "tool_calls": [],
        "retrieved_documents": [],
        "evidence": {},
        "agent_response": None,
        "critic_feedback": None,
        "confidence_score": 0.0,
        "retry_count": 0,
        "max_retries": 2,
        "trace_id": "TRC-TEST-001",
        "final_status": "PENDING"
    }

    final_state = await investigation_graph.ainvoke(initial_state)

    assert final_state["customer_id"] == "CUST_1009"
    assert len(final_state["investigation_plan"]) > 0
    assert len(final_state["tool_calls"]) >= 2
    assert final_state["critic_feedback"]["passed"] is True
    assert final_state["agent_response"]["risk_level"] == "HIGH"
    assert "case_id" in final_state["agent_response"]
