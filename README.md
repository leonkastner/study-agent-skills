# Universal AI Study Engine (`study-agent-skills`)

A universal skill set that turns any AI coding assistant into an exam-calibrated personal study tutor. Compatible with **Google Antigravity**, **Claude Code / Desktop**, **Cursor**, **Windsurf**, and any harness supporting the open Agent Skills standard.

---

## Instant Setup (1 Prompt)

Open your course folder in your AI desktop app and paste this prompt into the chat:

```text
Install the study skill set from https://github.com/leonkastner/study-agent-skills into this workspace and set up my study tutor for [Course Name].
```

The agent will clone the skills, audit all slide decks, lock official professorial terminology, and initialize your personal progress ledger.

---

## Recommended Setup

### 1. Interface: Use a Desktop App (Avoid Raw Terminal)
While command-line terminals work, studying in a raw terminal is visually inconvenient for reading tables, math formulas, and scorecards. We recommend using a desktop app with a clean graphical chat interface:
- **Google Antigravity** (Desktop App / Agent Manager) — Recommended
- **Claude Desktop**
- **Cursor** / **Windsurf** / **ChatGPT Desktop**

### 2. Model Selection: Fast Models Win
For interactive study sessions, **response latency is critical**. Slow models break cognitive momentum during active retrieval.
- Choose a **fast, low-latency model** (e.g., Gemini Flash, Claude Haiku, or GPT-4o-mini).
- Fast models provide near-instant responses, follow grading rubrics accurately, and keep study sessions engaging.

---

## How to Organize Your Course Folder

```text
My_Course_Name/
└── Course_Materials/
    ├── 01_Lecture_Slides/             # Drop your lecture PDFs here (L01.pdf, L02.pdf...)
    ├── 02_Notes_and_Summaries/        # Notes, summaries, or reading materials
    ├── 03_Past_Exams_and_Solutions/   # Past exam papers and solution keys (optional)
    └── 04_Syllabus_and_Admin/         # Syllabus, exam guidelines, or transcripts
```

---

## Core Skills & Workflow

The system consists of 3 focused skills:

| Skill | Purpose | How to Trigger |
| :--- | :--- | :--- |
| **`course-setup`** | Audits 100% of lecture slides, locks professorial terminology into `terminology_lock.json`, detects missing material gaps, and initializes `knowledge_ledger.json`. | Run automatically during initial setup, or prompt: *"Audit my course materials"*. |
| **`study-session`** | Conducts 100% in-chat active study drills. Runs 2-minute spiral warmups, rotates across 5 active formats (scenarios, calculations, error-spotting, triage, taxonomy), and updates mastery live. | Prompt: *"Let's study"* or *"Quiz me on Module 2"*. |
| **`mock-exam`** | Assembles and proctors a balanced, full-scope mock exam paper covering the entire syllabus. Grades point-by-point and generates diagnostic weakness reports. | Prompt: *"Run a full mock exam"*. |

---

## Why This Works

1. **Zero Slide Blindspots:** Audits all lecture slides and in-slide exercises, preventing tutors from fixating only on old exams.
2. **Canonical Terminology Lock:** Locks official academic terms from your slides into `Knowledge_Ledger/terminology_lock.json`, eliminating confusing paraphrasing and enforcing precise keyword grading.
3. **Active Retrieval:** Replaces passive reading with interactive scenario diagnosis, metric calculations, and unguided forensic error-spotting.
4. **Live Mastery Ledger:** Tracks atomic knowledge units and renders `Knowledge_Ledger/Mastery_Dashboard.md` after every drill.

---

## License

Distributed under the MIT License. See `LICENSE` for details.
