#!/usr/bin/env python3
"""
Knowledge Ledger & Terminology Lock Initializer
Builds knowledge_ledger.json, terminology_lock.json, and Mastery_Dashboard.md.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path


def create_initial_ledger(course_name: str, modules_data: list, exam_date: str = None, total_points: int = 120, exam_duration: int = 90) -> dict:
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    total_units = sum(len(m.get("units", [])) for m in modules_data)

    ledger = {
        "metadata": {
            "course": course_name,
            "credits": "5 ECTS",
            "exam_date": exam_date or "TBD",
            "exam_duration_minutes": exam_duration,
            "total_points": total_points,
            "number_of_main_questions": len(modules_data),
            "points_per_question": round(total_points / max(1, len(modules_data))),
            "created_at": now_iso,
            "last_updated": now_iso,
            "total_knowledge_units": total_units,
            "overall_mastery_pct": 0.0
        },
        "cognitive_levels": {
            "L1_Remember": "Recall facts, list items, state definitions without deep commentary.",
            "L2_Understand": "Explain concepts, translate meaning, compare mechanisms, contrast trade-offs.",
            "L3_Apply": "Use rules, methods, or models to solve concrete problems, execute calculations.",
            "L4_Evaluate": "Make judgments, assess bias/fairness, criticize systems based on criteria.",
            "L5_Develop": "Synthesize solutions, combine top-down/bottom-up architectures."
        },
        "modules": modules_data
    }

    return ledger


def render_dashboard(ledger: dict) -> str:
    meta = ledger["metadata"]
    total_units = meta["total_knowledge_units"]
    overall_pct = meta["overall_mastery_pct"]

    # Count statuses
    counts = {"Exam Ready": 0, "Solid Understanding": 0, "Basic Recall": 0, "Fragile": 0, "Untested": 0}
    for m in ledger["modules"]:
        for u in m.get("units", []):
            st = u.get("status", "Untested")
            counts[st] = counts.get(st, 0) + 1

    bar_len = 10
    filled = int(round(overall_pct / 10))
    progress_bar = "█" * filled + "░" * (bar_len - filled)

    md = f"""# 📊 {meta['course']} — Personal Mastery Dashboard

**Course:** {meta['course']}  
**Target Exam Date:** {meta['exam_date']}  
**Total Points:** {meta['total_points']} Points across {meta['number_of_main_questions']} Main Questions  
**Overall Exam Readiness:** **{overall_pct:.1f}%** [{progress_bar}]  
**Last Updated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  

---

## 1. Executive Summary & Readiness Status

| Metric | Value |
| :--- | :--- |
| **Total Knowledge Units** | **{total_units} Atomic Units** |
| **Overall Exam Readiness** | **{overall_pct:.1f}%** |
| **Exam Ready Units (80–100%)** | **{counts['Exam Ready']} Units** |
| **Solid Understanding (60–79%)** | **{counts['Solid Understanding']} Units** |
| **Basic Recall (25–59%)** | **{counts['Basic Recall']} Units** |
| **Fragile / Untested (0–24%)** | **{counts['Fragile'] + counts['Untested']} Units** |

---

## 2. Module-by-Module Progress & Exam Coverage

"""

    for m in ledger["modules"]:
        mod_pct = m.get("module_mastery_pct", 0.0)
        status_tag = "Exam Ready" if mod_pct >= 80 else ("In Progress" if mod_pct > 0 else "Untested")
        sources_str = ", ".join(m.get("source_lectures", []))

        md += f"### 🔹 {m['module_id']}: {m['title']} ({mod_pct:.1f}% Mastery — {status_tag})\n"
        md += f"**Exam Scope:** {m.get('exam_question', 'N/A')} | **Sources:** {sources_str}\n\n"
        md += "| Unit ID | Title | Depth | Priority | Mastery | Status | Last Reviewed |\n"
        md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

        for u in m.get("units", []):
            last_rev = u.get("last_reviewed") or "Never"
            if "T" in str(last_rev):
                last_rev = str(last_rev).split("T")[0]
            md += f"| `{u['id']}` | **{u['title']}** | `{u.get('target_depth', 'L2_Understand')}` | {u.get('exam_priority', 'High')} | **{u.get('mastery_score', 0)}%** | `{u.get('status', 'Untested')}` | {last_rev} |\n"

        md += "\n"

    return md


def scaffold_course_rules(target_dir: Path, course_name: str, exam_date: str = None):
    """Scaffolds lean AGENTS.md and GEMINI.md in target course workspace."""
    agents_md = target_dir / "AGENTS.md"
    gemini_md = target_dir / "GEMINI.md"

    content = f"""# 🎓 {course_name} — Personal Study Tutor Instructions

**Course:** {course_name}  
**Target Exam Date:** {exam_date or 'TBD'}  
**Primary Database:** `Knowledge_Ledger/knowledge_ledger.json`  
**Mastery Dashboard:** `Knowledge_Ledger/Mastery_Dashboard.md`  
**Terminology Lock:** `Knowledge_Ledger/terminology_lock.json`  

---

## Operating Protocol for Every Study Session

1. **Kickoff Card:** Load `Knowledge_Ledger/knowledge_ledger.json` and display overall exam readiness %.
2. **2-Minute Spiral Warmup:** Launch 1–2 rapid questions from decayed/fragile units before new concepts.
3. **100% In-Chat Active Learning:** Rotate dynamically across the 5 formats (Scenarios, Math Calculations, Unguided Forensic Error-Spotting, Priority Triage, Taxonomy Matrices).
4. **Strict Terminology & Rubric Grading:** Enforce exact terms from `Knowledge_Ledger/terminology_lock.json`. Penalize colloquialisms with explicit 4-part feedback.
5. **Continuous Live Updates:** Update `knowledge_ledger.json` and `Mastery_Dashboard.md` after every answered task.
"""

    if not agents_md.exists():
        with open(agents_md, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [CREATED] {agents_md}")

    if not gemini_md.exists():
        with open(gemini_md, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [CREATED] {gemini_md}")


def main():
    parser = argparse.ArgumentParser(description="Initialize knowledge ledger and terminology lock.")
    parser.add_argument("-n", "--name", default="University Course", help="Course Name")
    parser.add_argument("-d", "--date", default="TBD", help="Target Exam Date")
    parser.add_argument("-t", "--target", default=".", help="Target workspace root")

    args = parser.parse_args()
    target_root = Path(args.target).resolve()
    kl_dir = target_root / "Knowledge_Ledger"
    kl_dir.mkdir(parents=True, exist_ok=True)

    ledger_path = kl_dir / "knowledge_ledger.json"
    glossary_path = kl_dir / "terminology_lock.json"
    dashboard_path = kl_dir / "Mastery_Dashboard.md"

    # Default skeleton modules if no parsed data is provided
    default_modules = [
        {
            "module_id": "M01",
            "exam_question": "Question 1",
            "title": "Course Foundations & Core Concepts",
            "source_lectures": ["Lecture 1", "Lecture 2"],
            "status": "Untested",
            "module_mastery_pct": 0.0,
            "units": [
                {
                    "id": "M01_KU01",
                    "title": "Foundational Definitions & Scope",
                    "target_depth": "L1_Remember",
                    "bloom_level": 1,
                    "exam_priority": "High",
                    "mastery_score": 0,
                    "status": "Untested",
                    "last_reviewed": None,
                    "review_urgency": 1.0,
                    "key_points": ["Core definitions", "Boundary conditions"],
                    "common_misconceptions": ["Over-generalizing definitions"],
                    "weaknesses_log": []
                },
                {
                    "id": "M01_KU02",
                    "title": "Primary Frameworks & Models",
                    "target_depth": "L2_Understand",
                    "bloom_level": 2,
                    "exam_priority": "Critical",
                    "mastery_score": 0,
                    "status": "Untested",
                    "last_reviewed": None,
                    "review_urgency": 1.0,
                    "key_points": ["Core model architecture", "Trade-offs"],
                    "common_misconceptions": [],
                    "weaknesses_log": []
                }
            ]
        }
    ]

    ledger = create_initial_ledger(args.name, default_modules, args.date)

    if not ledger_path.exists():
        with open(ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2, ensure_ascii=False)
        print(f"  [CREATED] {ledger_path}")

    if not glossary_path.exists():
        skeleton_glossary = {
            "metadata": {
                "course": args.name,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "total_locked_terms": 2
            },
            "terms": [
                {
                    "term": "Foundational Principle",
                    "canonical_definition": "Primary axiom governing system operations.",
                    "required_keywords": ["axiom", "system operation", "invariant"],
                    "prohibited_colloquialisms": ["rule of thumb", "general idea"]
                }
            ]
        }
        with open(glossary_path, "w", encoding="utf-8") as f:
            json.dump(skeleton_glossary, f, indent=2, ensure_ascii=False)
        print(f"  [CREATED] {glossary_path}")

    dashboard_md = render_dashboard(ledger)
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_md)
    print(f"  [RENDERED] {dashboard_path}")

    scaffold_course_rules(target_root, args.name, args.date)


if __name__ == "__main__":
    main()
