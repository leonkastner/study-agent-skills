# 📈 Bloom Cognitive Depth & Mastery Curve Matrix

Every Knowledge Unit in `knowledge_ledger.json` is calibrated against Bloom's Revised Cognitive Taxonomy to ensure the student reaches the exact required exam depth.

---

## 1. The 5 Cognitive Levels

| Level | Bloom Tag | Cognitive Action | Exam Point Weight | Example Question Phrasing |
| :--- | :--- | :--- | :---: | :--- |
| **L1** | `L1_Remember` | Recall exact facts, list taxonomy items, define standard terms. | 1.0 – 2.5 pts | *"List the 5 levels of...", "Name 3 types of..."* |
| **L2** | `L2_Understand` | Explain underlying mechanisms, compare and contrast approaches, illustrate trade-offs. | 2.0 – 4.0 pts | *"Explain why approach A fails in context B...", "Compare Top-Down vs Bottom-Up across..."* |
| **L3** | `L3_Apply` | Execute formulas, apply rules to novel cases, calculate metrics. | 3.0 – 6.0 pts | *"Calculate the Disparate Impact Ratio...", "Apply the Blanchard & Peale filter to..."* |
| **L4** | `L4_Evaluate` | Spot subtle flaws in systems/claims, criticize ethical/technical tradeoffs, justify decisions. | 3.0 – 6.0 pts | *"Evaluate the following passage and identify all errors...", "Which metric is appropriate here and why?"* |
| **L5** | `L5_Develop` | Synthesize hybrid architectures, design end-to-end pipelines under constraints. | 4.0 – 8.0 pts | *"Design a multi-agent ethical coordination pipeline...", "Synthesize a mitigation strategy for..."* |

---

## 2. Multi-Session Mastery Progression (No Instant 100%)

Real mastery requires multi-session spaced retrieval across varied angles of attack. Scores advance gradually:

- **Exposure 1 (Initial Test):**
  - Flawless recall $\rightarrow$ `50%` (`Basic Recall`)
  - Partial recall / minor errors $\rightarrow$ `25%` (`Fragile`)
- **Exposure 2–3 (Interleaved / Varied Angle):**
  - Successful scenario application or calculation $\rightarrow$ `75%` (`Solid Understanding`)
- **Exposure 4+ (Delayed Recall & Mock Exam):**
  - Flawless recall during timed mock exam or unguided forensic error-spotting $\rightarrow$ `90% – 100%` (`Exam Ready`)
