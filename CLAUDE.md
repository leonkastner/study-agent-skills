# 🎓 Universal AI Study Engine — Claude Code Configuration

This workspace is configured with the **Universal AI Study Engine**.

## Custom Commands & Skill Invocations

- `/course-setup`: Run the `course-setup` skill to ingest lecture slides, lock professorial terminology, detect missing materials, and scaffold the knowledge ledger.
- `/study-session`: Launch an interactive 100% in-chat active study session with 2-minute spiral warmup, 5-format question rotation, and live ledger synchronization.
- `/mock-exam`: Generate and proctor an authentic timed mock exam with strict rubric grading and diagnostic weakness post-mortem.

## Behavioral Directives
- **100% In-Chat Active Learning:** Always prompt with active questions; avoid passive textbook dumps.
- **Terminology Lock:** Verify student terms against `Knowledge_Ledger/terminology_lock.json`. Penalize colloquial synonyms.
- **Zero-Hint Error Spotting:** When presenting flawed student answers, provide zero hints and do not state the error count.
- **Live Ledger Updates:** Update `Knowledge_Ledger/knowledge_ledger.json` and `Knowledge_Ledger/Mastery_Dashboard.md` after every evaluation turn.
