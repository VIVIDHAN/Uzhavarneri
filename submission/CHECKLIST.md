# Hackathon Submission Audit & Checklist

Project: **UzhavarNeri (உழவர்நெறி)**  
Track: Climate Resilience / Social Impact  
SDK: **Strands Agents SDK (v1.63.0)**  
License: **Apache-2.0**  

---

### Core Deliverables Checklist

- [x] **1. Working Strands Agent on AWS**
  - Uses official `strands-agents` SDK.
  - Multi-step agronomic tool orchestration (`get_block_weather`, `get_crop_guidelines`, `check_mandi_prices`, `validate_agrochemical_safety`).
  - Active `AgrochemicalSafetyGuard(InterventionHandler)` intercepting destructive chemical runoff and banned toxins.
  - Model backend: Amazon Bedrock (Nova / Claude) via `boto3` and OpenAI-compatible provider.

- [x] **2. Public Code Repository**
  - Public repository on GitHub.
  - Apache-2.0 Open Source License included (`LICENSE`).
  - Clean git commit history.
  - No secrets, API keys, or `.env` committed (`.gitignore` verified).
  - Clear `README.md` with installation, architecture diagram, and quickstart instructions.

- [x] **3. Builder Center Project Article**
  - Article written in [`submission/ARTICLE.md`](ARTICLE.md).
  - Explains the target community (Cauvery Delta smallholder farmers).
  - Describes the agentic architecture, tools, and Strands SDK features.
  - Documents the deterministic safety guardrail.
  - Includes measured benchmark comparisons against baseline LLM prompt.

- [x] **4. Under 3-Minute Demo Video**
  - Script ready in [`demo/demo_script.md`](../demo/demo_script.md) (2m 45s target).
  - Covers real-world community problem, architecture, live chemical runoff guardrail demo, banned pesticide interception, and measured benchmark results.
  - Free from copyrighted music and third-party trademarks.

- [x] **5. Reproducible Verification & Tests**
  - Complete automated test suite in `tests/` (`test_tools.py`, `test_guardrail.py`, `test_agent.py`).
  - All unit tests passing in <2 seconds.
  - Evaluation dataset in `eval/eval_cases.jsonl` with 25 realistic scenarios.
