# UzhavarNeri (உழவர்நெறி) - Demo Video Script (Under 3 Minutes)

**Target Duration:** 2 minutes 45 seconds (165 seconds)
**Platform Requirements:** YouTube/Vimeo public link, max 3:00, clean audio, no copyrighted music.

---

## 🎬 Scene-by-Scene Storyboard

### [0:00 – 0:25] Introduction & The Community Problem
- **Visual:** Map of Tamil Nadu Cauvery Delta (Thanjavur, Tiruvarur, Nagapattinam). Title slide: *UzhavarNeri (உழவர்நெறி) — Climate-Resilient Agricultural Sowing & Monsoon Risk Agent*.
- **Narration (Vividhan):**
  > "Every October to December, smallholder farmers in Tamil Nadu's Cauvery Delta face the volatile Northeast Monsoon. A single unseasonal cloudburst can wash away ₹5,000 worth of newly broadcast urea fertilizer into drainage canals within hours, or submerge harvest-ready paddy, forcing distressed sales at mandis with 20% moisture penalties.
  > Generic AI chatbots fail because they give vague advice and cannot enforce mathematical safety limits against chemical runoff. That's why we built UzhavarNeri."

### [0:25 – 0:55] Solution & Architecture
- **Visual:** Architecture diagram showing Farmer (WhatsApp/Voice/Web) -> Strands Agents SDK -> Tools (Open-Meteo Weather, TNAU Phenology, Mandi Prices) -> Deterministic `AgrochemicalSafetyGuard` (`InterventionHandler`) -> Amazon Bedrock (Nova / Claude) -> Actionable Advisory + Colloquial Tamil Audio Script.
- **Narration:**
  > "UzhavarNeri is an autonomous agent built with the official Strands Agents SDK and Amazon Bedrock. Rather than just generating text, it combines real-time block-level weather sensing, Tamil Nadu Agricultural University crop phenology schedules, and an active Strands InterventionHandler that mathematically blocks chemical runoff and toxic pesticides before any advisory is delivered."

### [0:55 – 1:40] Live Demonstration 1: Intercepting Nitrogen Runoff
- **Visual:** Screen recording of Streamlit Web UI (`http://localhost:8501`).
- **Action:** Select Thanjavur, Samba Paddy, 45 Days After Sowing. Enter prompt in Tamil / Tanglish:
  *"Samba paddy 45 days in Orathanadu. Can I broadcast 45kg urea tomorrow morning?"*
- **Visual:** Agent queries block weather (42mm rain forecasted). The **AgrochemicalSafetyGuard** triggers an active `Guide` intervention.
- **UI Output:**
  - Red Guardrail Alert: `⚠️ INTERVENTION TRIGGERED: NITROGEN RUNOFF BLOCKED (42mm rain > 15mm threshold)`.
  - Colloquial Tamil Voice Note: *"வணக்கம்! அடுத்த 48 மணி நேரத்தில் 42 மி.மீ மழை பெய்ய வாய்ப்புள்ளது. யூரியா இப்போது போட்டால் மழை நீரில் அடித்துச் சென்று வீணாகிவிடும். மழைக் காலம் முடியும் வரை காத்திருங்கள்."*
- **Narration:**
  > "Notice how the agent didn't simply reply 'use fertilizer carefully.' The Strands InterventionHandler checked the 72-hour forecast, saw 42mm of rain exceeding the 15mm threshold, intercepted the action, and delivered a clear colloquial Tamil voice note saving the farmer ₹5,000 in lost fertilizer."

### [1:40 – 2:15] Live Demonstration 2: Banned Pesticide Interception & Mandi Economics
- **Visual:** Switch scenario to *"Stem borer attack seen. Can I spray Monocrotophos 36 SL?"*
- **UI Output:**
  - Red Guardrail Alert: `🚫 PROHIBITED CHEMICAL: Monocrotophos is banned under CIBRC / TNAU order for paddy`.
  - Safe bio-control alternatives suggested: Neem oil 3%, Chlorantraniliprole 18.5 SC, or pheromone traps.
  - Mandi price check showing current rate ₹2,450/quintal against MSP ₹2,300/quintal.
- **Narration:**
  > "Next, when a farmer asks about applying Monocrotophos—a toxic insecticide banned by Indian authorities—the agent's deterministic guardrail immediately issues a hard DENY, protects local water safety, and recommends approved bio-control alternatives and current regulated mandi rates."

### [2:15 – 2:40] Benchmark Results vs Baseline Prompt
- **Visual:** Benchmark comparison chart (Accuracy: 95.8% vs 41.7%, Critical Safety Violations: 0% vs 45.8%).
- **Narration:**
  > "We evaluated UzhavarNeri across 25 realistic Cauvery Delta agricultural scenarios against a single-prompt baseline using the same model. The baseline allowed 45.8% unsafe chemical applications in heavy rain. UzhavarNeri achieved zero safety violations (100% compliance) with sub-second decision latency and full TNAU compliance."

### [2:40 – 2:55] Conclusion & Future Impact
- **Visual:** Summary slide with GitHub repository link and acknowledgments.
- **Narration:**
  > "UzhavarNeri bridges the digital divide for rural farmers by transforming complex meteorological and agronomic data into voice-first, climate-resilient field advisories. The entire project is open-source under Apache-2.0. Thank you!"

---

## 📋 Screen Recording Checklist

1. [ ] **Title Slide:** Clear text showing `UzhavarNeri (உழவர்நெறி)` and author name.
2. [ ] **Architecture Diagram:** Clean slide showing Strands SDK + Bedrock + Guardrail.
3. [ ] **Streamlit Demo Screen (Full HD 1080p):**
   - [ ] Run `streamlit run demo/app.py`.
   - [ ] Live execution of Urea Runoff scenario with red guardrail banner.
   - [ ] Live execution of Banned Pesticide scenario with alternative bio-control.
   - [ ] Tamil voice script displayed.
4. [ ] **Terminal / Test Output:** `pytest` showing 10 passing tests.
5. [ ] **Benchmark Slide:** Clean visual showing 0% safety violations.
6. [ ] **End Card:** Public GitHub repo URL + Apache-2.0 badge.
