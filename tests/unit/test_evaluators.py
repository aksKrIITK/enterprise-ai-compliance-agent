import pytest
from app.evals.evaluators.tool_eval import ToolSelectionEvaluator
from app.evals.evaluators.correctness_eval import CorrectnessEvaluator
from app.evals.evaluators.groundedness_eval import GroundednessEvaluator
from app.evals.evaluators.policy_eval import PolicyComplianceEvaluator
from app.evals.evaluators.hallucination_eval import HallucinationEvaluator


def test_tool_selection_evaluator():
    evaluator = ToolSelectionEvaluator()
    score = evaluator.evaluate(["tool_a", "tool_b"], ["tool_a", "tool_b", "tool_c"])
    assert score == 1.0

    score_partial = evaluator.evaluate(["tool_a", "tool_b"], ["tool_a"])
    assert score_partial == 0.5


def test_correctness_evaluator():
    evaluator = CorrectnessEvaluator()
    assert evaluator.evaluate("HIGH", "HIGH") is True
    assert evaluator.evaluate("LOW", "HIGH") is False


def test_policy_evaluator():
    evaluator = PolicyComplianceEvaluator()
    assert evaluator.evaluate({"risk_level": "HIGH", "recommendation": "SAR Escalation required"}) is True
    assert evaluator.evaluate({"risk_level": "HIGH", "recommendation": "Ignore and take no action"}) is False



def test_groundedness_evaluator():
    evaluator = GroundednessEvaluator()
    evidence = {
        "transactions": [{"amount": 50000}],
        "rag_policy_citations": [{"doc_id": "P-1"}]
    }
    response = {
        "evidence": ["Customer transaction of 50000 flagged"]
    }
    score = evaluator.evaluate(evidence, response)
    assert score >= 0.8


def test_hallucination_evaluator():
    evaluator = HallucinationEvaluator()
    # Fully grounded
    evidence = {
        "transactions": [{"amount": 50000}],
        "rag_policy_citations": [{"doc_id": "P-1"}],
        "risk_scoring": {"risk_score": 0.9}
    }
    response = {
        "risk_level": "HIGH",
        "evidence": ["Transaction evidence supported"]
    }
    score = evaluator.evaluate(evidence, response)
    assert score <= 0.2

    # Hallucinated / missing evidence
    score_unsupported = evaluator.evaluate({}, response)
    assert score_unsupported > 0.5
