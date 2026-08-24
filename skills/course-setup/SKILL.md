---
name: course-setup
description: >-
  Sets up and initializes a course workspace. Recursively audits all course materials (slides,
  notes, transcripts, past exams), spawns parallel subagents across lecture batches, extracts
  100% of slide topics and in-slide exercises, locks canonical professorial terminology, generates
  a document gap report, initializes knowledge_ledger.json and Mastery_Dashboard.md, and auto-scaffolds
  agent rules. Use whenever the user asks to set up, initialize, or re-index a course.
---

# 🛠️ Skill: `course-setup` (Course Ingestion, Slide Audit & Scaffolding)

Use this skill to onboard any new course or re-audit an existing course with updated materials.

---

## 1. Multi-Subagent Ingestion Architecture

When a course contains multiple slide decks, transcripts, or past exams, **DO NOT parse everything in a single prompt turn**. Doing so causes severe context bloat and degrades indexing accuracy.

### Orchestration Protocol:
1. **Scan Workspace:** Identify all files in `Course_Materials/` or workspace subdirectories.
2. **Spawn Parallel Research Subagents:**
   - Group lecture slide decks into batches (e.g. 3–4 decks per subagent).
   - Use the template in [subagent_intake_prompt.md](./references/subagent_intake_prompt.md).
   - Subagent Role: `Lecture Deck Auditor (L01-L04)`, `Lecture Deck Auditor (L05-L08)`, `Past Exam Auditor`.
3. **Collect & Synthesize:**
   - Each subagent returns a clean JSON summary of atomic knowledge units, extracted keywords, in-slide exercises, and syllabus exclusion flags.
   - The main agent merges these summaries into the central ledger.

---

## 2. Step-by-Step Execution Runbook

```mermaid
flowchart TD
    A[User: 'Set up my course for [Name]'] --> B[Step 1: Discover & Classify Materials]
    B --> C[Step 2: Spawn Parallel Subagents for Deep Audit]
    C --> D[Step 3: Run parse_slides.py / parse_materials.py]
    D --> E[Step 4: Build knowledge_ledger.json & terminology_lock.json]
    E --> F[Step 5: Run Gap Analysis & Generate Gap Report]
    F --> G[Step 6: Render Mastery_Dashboard.md & Scaffold AGENTS.md]
```

### Step 1: Discover & Classify Available Materials
Classify available files into the **Material Availability Matrix**:
- **Slides:** PDF/PPTX slide decks in `01_Lecture_Slides/`.
- **Notes:** Markdown, Word, or PDF notes in `02_Notes_and_Summaries/`.
- **Exams:** Past exam papers and official solutions in `03_Past_Exams_and_Solutions/`.
- **Transcripts/Admin:** Syllabus, exam briefing audio/video, or transcripts in `04_Syllabus_and_Admin/`.

### Step 2: Extract Atomic Knowledge Units & In-Slide Exercises
For every lecture deck:
- Extract all slide titles, conceptual subsections, and key definitions.
- **Extract all in-slide exercises, calculation problems, and scenarios** (Crucial: in-slide exercises often reveal the professor's exact exam question archetypes!).
- Identify explicit syllabus exclusions (e.g., topics marked *"not relevant for exam"* or *"excursion"*).
- Run `python3 scripts/parse_slides.py --input Course_Materials/01_Lecture_Slides/` or let subagents process them.

### Step 3: Lock Canonical Professorial Terminology
To prevent AI paraphrasing drift across study sessions:
- Identify exact technical terms, standard definitions, and formal distinctions directly from the slides.
- Save them into `Knowledge_Ledger/terminology_lock.json` matching [terminology_schema.json](./references/terminology_schema.json).
- Example:
  ```json
  {
    "term": "Inherent Complexity",
    "canonical_definition": "The structural difficulty of calculating optimal ethical decisions in multi-agent environments.",
    "required_keywords": ["NP-hard", "combinatorial state space", "multi-agent interactions"],
    "prohibited_colloquialisms": ["too slow", "hard to calculate", "takes long"]
  }
  ```

### Step 4: Perform Gap Analysis
Compare what exists in the slides vs. what is available in student notes and practice exams:
- Follow the heuristic in [gap_detection_guide.md](./references/gap_detection_guide.md).
- Identify slide topics that have **zero practice exercises** or **zero student notes**.
- Prepare the **Document Gap Report** to inform the student.

### Step 5: Initialize Knowledge Ledger & Dashboard
Run `python3 scripts/init_ledger.py` or write `Knowledge_Ledger/knowledge_ledger.json` conforming to [ledger_schema.json](./references/ledger_schema.json):
- Set all initial mastery scores to `0%` (`Untested`).
- Assign Bloom depth levels (`L1_Remember` to `L5_Develop`).
- Assign exam priorities (`Critical`, `High`, `Medium`, `Low`).
- Render `Knowledge_Ledger/Mastery_Dashboard.md` using [dashboard_template.md](./resources/dashboard_template.md).

### Step 6: Scaffold Lean Agent Rules
Write or update `AGENTS.md` and `GEMINI.md` in the project root with the specific course title, target exam date (if provided), total point weight, and pointers to `Knowledge_Ledger/`.

---

## 3. Output to the Student (Intake Report)

Always conclude the setup with a clear, inspiring kickoff report:

```markdown
# 🎓 Course Setup Complete: [Course Name]

### 📊 Ingestion Summary
- **Lecture Decks Audited:** X Decks (Y total slides parsed)
- **Atomic Knowledge Units Created:** Z Units across N Modules
- **Professorial Terms Locked:** K Canonical Terms
- **Baseline Exam Readiness:** 0.0% [░░░░░░░░░░]

### 🔍 Document Gap Report & Recommendations
- ✅ **Strong Coverage:** Module 1, 2, 3 have full slides and past exam tasks.
- ⚠️ **Identified Gaps:**
  - *Lecture 5 (Topic X):* 38 slides found, but no practice exercises or student notes.
  - *Recommendation:* Do you have exercise sheets for Lecture 5? If not, the engine will synthesize authentic Bloom L2/L3 exam questions for it.

### 🚀 Ready to Begin!
Whenever you want to start studying, simply say: **"Let's study"** or **"Start session"**.
```
