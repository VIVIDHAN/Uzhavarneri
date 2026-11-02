"""Integration tests for UzhavarNeriAgent."""

import os
import pytest
from uzhavarneri.agent import UzhavarNeriAgent


def test_agent_initialization():
    agent = UzhavarNeriAgent()
    assert agent.agent is not None
    assert len(agent.agent.tool_names) == 4
    assert "get_block_weather" in agent.agent.tool_names
    assert "validate_agrochemical_safety" in agent.agent.tool_names


@pytest.mark.skipif(os.environ.get("SKIP_NETWORK_TESTS") == "1", reason="Skip network LLM calls in fast test mode")
def test_agent_chat_execution():
    agent = UzhavarNeriAgent()
    res = agent.chat("Vanakkam! What is the optimal water depth for 20-day-old Samba paddy seedlings?")
    assert "reply" in res
    assert len(res["reply"]) > 20
    assert "latency_ms" in res
    assert res["latency_ms"] > 0
