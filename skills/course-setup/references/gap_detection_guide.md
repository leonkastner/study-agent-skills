# 🔍 Course Material Gap Detection Guide

During `course-setup`, the intake engine compares what is presented in the primary slides against available practice exams, student notes, and exercise sheets.

---

## 1. The 3-Tier Gap Classification Matrix

| Gap Tier | Condition | Diagnostic Prompt to Student | Recommended Remediation Action |
| :--- | :--- | :--- | :--- |
| **Tier 1: Complete Exercise Blindspot** | A lecture deck contains > 30 slides, but **zero past exam questions** and **zero student notes** cover this topic. | *"⚠️ Lecture X contains N slides on Concept Y, but has no practice tasks in your files. Do you have tutorial sheets for this lecture?"* | If student has no files, `mock-exam` automatically synthesizes authentic Bloom L2/L3 exam questions from the slide objectives. |
| **Tier 2: Formula / Calculation Disconnect** | A slide introduces a mathematical equation (e.g. Risk $P \times S$ or Disparate Impact), but no worked numerical examples exist. | *"⚠️ Slide Z introduces Formula F, but lacks worked calculation examples."* | Schedule dedicated active numerical calculation drills in `study-session`. |
| **Tier 3: Definition Ambiguity / Missing Terminology** | A slide mentions a key concept without giving a formal, explicit definition. | *"ℹ️ Term T is highlighted on slide S, but lacks an explicit professorial definition."* | Flag for student clarification or extract canonical definition from textbook/literature. |

---

## 2. Document Gap Report Formatting Standard

Always present gap analysis in a structured, actionable markdown block:

```markdown
### 🔍 Document Gap Report & Quality Audit
- ✅ **Complete Coverage:** Modules 1, 2, 4 have matching slides and past exam solutions.
- ⚠️ **Actionable Gaps Identified:**
  1. *Module 3 (Topic A):* 45 slides found; 0 practice exercises. (Engine will synthesize L2/L3 problems).
  2. *Module 5 (Formula B):* Mathematical metric present without worked example. (Active calculation drill scheduled).
```
