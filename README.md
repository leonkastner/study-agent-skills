# Universal AI Study Engine (`study-agent-skills`)

A universal skill set that turns any AI coding assistant into an exam-calibrated personal study tutor. Compatible with **Google Antigravity**, **Claude Code / Desktop**, **Cursor**, **Windsurf**, and any harness supporting the open Agent Skills standard.

---

## 1. Quickstart (One Prompt Setup)

Open your course directory (containing your slides, notes, or PDFs) in your AI desktop app and paste:

```text
Install the study skill set from https://github.com/leonkastner/study-agent-skills into this workspace and set up my study tutor.
```

This single command:
1. Clones the skills into your workspace.
2. Automatically scans and classifies all documents in your directory (no manual folder organization required).
3. Audits all lecture slides and in-slide exercises.
4. Locks official professorial terminology into `Knowledge_Ledger/terminology_lock.json`.
5. Initializes your progress tracker in `Knowledge_Ledger/Mastery_Dashboard.md`.

---

## 2. How to Use It

Once initialized, use simple chat prompts or slash commands to run your study workflow:

### Step 1: Active Daily Study
Start an active, interleaved study session with 2-minute spiral warmups, applied scenario diagnosis, metric calculations, and unguided error-spotting:
```text
Let's study
```
*(Or use `/study-session`)*

Your tutor asks one focused question at a time, evaluates against the locked terminology, and updates your mastery dashboard live after every answer.

### Step 2: Timed Mock Exams
Simulate a full exam covering 100% of the course syllabus under realistic timing and point weights:
```text
Run a full mock exam
```
*(Or use `/mock-exam`)*

The tutor delivers the exam, grades each answer point-by-point against professorial rubrics, and outputs a diagnostic report with immediate remediation targets.

### Step 3: Material Re-Auditing (Optional)
If you add new lecture slides or notes later in the semester, re-index your workspace:
```text
Audit my course materials
```
*(Or use `/course-setup`)*

---

## 3. Recommended Environment

### Interface: Desktop App (Avoid Raw Terminal)
Studying in a raw terminal makes reading tables, math formulas, and scorecards inconvenient. We recommend using a desktop app with a clean graphical chat interface:
- **Google Antigravity** (Desktop App / Agent Manager) — Recommended
- **Claude Desktop**
- **Cursor** / **Windsurf** / **ChatGPT Desktop**

### Model: Fast Low-Latency Models
Active tutoring requires fast turnarounds to keep study sessions engaging:
- Recommended: **Gemini Flash**, **Claude Sonnet**, or **GPT-5.6 / Luna**.
- Fast models offer near-instant responses while accurately enforcing strict grading rubrics.

---

## 4. Skills Reference

| Skill | Purpose | Chat Trigger | Slash Command |
| :--- | :--- | :--- | :--- |
| **`course-setup`** | Scans documents, extracts slide topics, locks technical terminology, and builds the knowledge ledger. | *"Audit my materials"* | `/course-setup` |
| **`study-session`** | Conducts active interleaved drills (scenarios, calculations, unguided error-spotting, taxonomy) and syncs dashboard. | *"Let's study"* | `/study-session` |
| **`mock-exam`** | Assembles balanced full-syllabus exam papers, proctors timed tests, and produces diagnostic post-mortems. | *"Run mock exam"* | `/mock-exam` |

---

## License

Distributed under the MIT License. See `LICENSE` for details.
