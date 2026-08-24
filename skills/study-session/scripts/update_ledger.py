#!/usr/bin/env python3
"""
Knowledge Ledger Atomic Updater & Dashboard Re-Renderer
Atomically updates unit scores, appends to weaknesses_log, recalculates mastery %, and re-renders Mastery_Dashboard.md.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path


def update_unit_score(ledger_path: Path, unit_id: str, new_score: float, weakness_entry: str = None) -> dict:
    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    unit_found = False
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for module in ledger.get("modules", []):
        for unit in module.get("units", []):
            if unit.get("id") == unit_id:
                unit_found = True
                unit["mastery_score"] = max(0, min(100, new_score))
                unit["last_reviewed"] = now_iso
                unit["review_urgency"] = 1.0

                # Status mapping
                if new_score >= 80:
                    unit["status"] = "Exam Ready"
                elif new_score >= 60:
                    unit["status"] = "Solid Understanding"
                elif new_score >= 25:
                    unit["status"] = "Basic Recall"
                elif new_score > 0:
                    unit["status"] = "Fragile"
                else:
                    unit["status"] = "Untested"

                if weakness_entry:
                    today_str = datetime.date.today().isoformat()
                    unit.setdefault("weaknesses_log", []).append(f"{today_str}: {weakness_entry}")
                break
        if unit_found:
            break

    if not unit_found:
        print(f"[WARN] Unit ID '{unit_id}' not found in ledger.")
        return ledger

    # Recalculate module averages and overall average
    all_scores = []
    for module in ledger.get("modules", []):
        units = module.get("units", [])
        if units:
            mod_avg = sum(u.get("mastery_score", 0) for u in units) / len(units)
            module["module_mastery_pct"] = round(mod_avg, 1)
            all_scores.extend(u.get("mastery_score", 0) for u in units)

            if mod_avg >= 80:
                module["status"] = "Exam Ready"
            elif mod_avg >= 60:
                module["status"] = "Solid Understanding"
            elif mod_avg > 0:
                module["status"] = "In Progress"
            else:
                module["status"] = "Untested"

    if all_scores:
        overall_avg = sum(all_scores) / len(all_scores)
        ledger["metadata"]["overall_mastery_pct"] = round(overall_avg, 1)

    ledger["metadata"]["last_updated"] = now_iso

    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

    return ledger


def re_render_dashboard(ledger: dict, dashboard_path: Path):
    meta = ledger["metadata"]
    total_units = meta["total_knowledge_units"]
    overall_pct = meta["overall_mastery_pct"]

    counts = {"Exam Ready": 0, "Solid Understanding": 0, "Basic Recall": 0, "Fragile": 0, "Untested": 0}
    for m in ledger.get("modules", []):
        for u in m.get("units", []):
            st = u.get("status", "Untested")
            counts[st] = counts.get(st, 0) + 1

    bar_len = 10
    filled = int(round(overall_pct / 10))
    progress_bar = "█" * filled + "░" * (bar_len - filled)

    md = f"""# 📊 {meta['course']} — Personal Mastery Dashboard

**Course:** {meta['course']}  
**Target Exam Date:** {meta.get('exam_date', 'TBD')}  
**Total Points:** {meta.get('total_points', 120)} Points across {meta.get('number_of_main_questions', 10)} Main Questions  
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

    for m in ledger.get("modules", []):
        mod_pct = m.get("module_mastery_pct", 0.0)
        status_tag = m.get("status", "Untested")
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

    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(md)


def main():
    parser = argparse.ArgumentParser(description="Update knowledge ledger unit and re-render dashboard.")
    parser.add_argument("-l", "--ledger", default="Knowledge_Ledger/knowledge_ledger.json", help="Path to knowledge_ledger.json")
    parser.add_argument("-d", "--dashboard", default="Knowledge_Ledger/Mastery_Dashboard.md", help="Path to Mastery_Dashboard.md")
    parser.add_argument("-u", "--unit", required=True, help="Unit ID (e.g. M01_KU01)")
    parser.add_argument("-s", "--score", type=float, required=True, help="New mastery score (0-100)")
    parser.add_argument("-w", "--weakness", default=None, help="Optional weakness log message")

    args = parser.parse_args()
    ledger_path = Path(args.ledger)
    dashboard_path = Path(args.dashboard)

    if not ledger_path.exists():
        print(f"Error: Ledger file {ledger_path} not found.")
        sys.exit(1)

    updated_ledger = update_unit_score(ledger_path, args.unit, args.score, args.weakness)
    re_render_dashboard(updated_ledger, dashboard_path)
    print(f"✅ Updated `{args.unit}` -> {args.score}%. Overall readiness: {updated_ledger['metadata']['overall_mastery_pct']}%.")


if __name__ == "__main__":
    main()
