#!/usr/bin/env python3
"""
Mock Exam Generator
Reads knowledge_ledger.json and generates an authentic, balanced mock exam markdown sheet.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path


def generate_mock_exam(ledger_path: Path, output_file: Path = None) -> str:
    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    meta = ledger.get("metadata", {})
    course = meta.get("course", "Course")
    total_pts = meta.get("total_points", 120)
    duration = meta.get("exam_duration_minutes", 90)
    modules = ledger.get("modules", [])

    pts_per_mod = round(total_pts / max(1, len(modules)))

    md = f"""# 📝 Mock Examination: {course}

**Course:** {course}  
**Exam Duration:** {duration} Minutes  
**Total Points:** {total_pts} Points  
**Structure:** {len(modules)} Main Questions ({pts_per_mod} Points each)  
**Date:** {datetime.date.today().strftime('%B %d, %Y')}  

---

### Instructions for the Candidate:
1. All questions must be answered using **precise professorial terminology**.
2. For calculation questions, show the full formula and step-by-step arithmetic.
3. For forensic error-spotting tasks, evaluate the entire passage unguided.
4. Maintain academic rigor; colloquial approximations will be penalized.

---

"""

    for idx, mod in enumerate(modules, start=1):
        mod_title = mod.get("title", f"Module {idx}")
        md += f"## Problem {idx}: {mod_title} ({pts_per_mod} Points)\n\n"

        units = mod.get("units", [])
        if not units:
            md += f"*Question {idx}.1:* State the core definitions and operational principles of {mod_title}. (4.0 Points)\n\n"
            md += f"*Question {idx}.2:* Analyze the primary trade-offs and mechanisms governing this module. (4.0 Points)\n\n"
            md += f"*Question {idx}.3:* Evaluate a real-world scenario applying these concepts. (4.0 Points)\n\n"
        else:
            pts_per_sub = round(pts_per_mod / max(1, min(len(units), 3)), 1)
            for u_idx, unit in enumerate(units[:3], start=1):
                depth = unit.get("target_depth", "L2_Understand")
                u_title = unit.get("title", "Concept")

                if depth == "L1_Remember":
                    md += f"**Part {idx}.{u_idx} (Taxonomy & Recall — {pts_per_sub} Pts):**\n"
                    md += f"State the formal definition of **{u_title}** and list all its primary constituent elements or levels.\n\n"
                elif depth == "L3_Apply":
                    md += f"**Part {idx}.{u_idx} (Applied Application / Calculation — {pts_per_sub} Pts):**\n"
                    md += f"Suppose a system operates under the constraints of **{u_title}**. Execute the necessary step-by-step calculations/decisions and justify the optimal action.\n\n"
                elif depth == "L4_Evaluate":
                    md += f"**Part {idx}.{u_idx} (Forensic Evaluation & Diagnosis — {pts_per_sub} Pts):**\n"
                    md += f"A candidate asserts a system implementation for **{u_title}**. Identify all technical flaws, boundary violations, and provide the correct professorial formulation.\n\n"
                else:
                    md += f"**Part {idx}.{u_idx} (Mechanism & Trade-Off Analysis — {pts_per_sub} Pts):**\n"
                    md += f"Explain the underlying mechanism of **{u_title}**. Contrast its strengths and limitations against alternative approaches.\n\n"

        md += "---\n\n"

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Generated mock exam paper: {output_file}")

    return md


def main():
    parser = argparse.ArgumentParser(description="Generate mock exam markdown paper.")
    parser.add_argument("-l", "--ledger", default="Knowledge_Ledger/knowledge_ledger.json", help="Path to knowledge ledger")
    parser.add_argument("-o", "--output", default="Exam_Preparation/Simulated_Mock_Exam.md", help="Output mock exam file")

    args = parser.parse_args()
    ledger_path = Path(args.ledger)
    output_path = Path(args.output) if args.output else None

    if not ledger_path.exists():
        print(f"Error: Ledger file {ledger_path} not found.")
        sys.exit(1)

    generate_mock_exam(ledger_path, output_path)


if __name__ == "__main__":
    main()
