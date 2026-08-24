#!/usr/bin/env python3
"""
Multi-Modal Material Parser for Course Setup
Parses transcripts, markdown notes, syllabus documents, and exercise problem sheets.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def parse_text_or_markdown(file_path: Path) -> dict:
    """Parses markdown or plain text notes into sections."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Split by markdown headers
    headers = re.findall(r'^(#{1,4}\s+.+)$', content, flags=re.MULTILINE)
    word_count = len(content.split())

    # Check for exam hints
    exam_hints = re.findall(r'(?:exam|klausur|important|wichtig|prof|betz|excluded|skip)[^\.\n]*[\.\n]', content, re.IGNORECASE)

    return {
        "filename": file_path.name,
        "type": "notes_markdown" if file_path.suffix == ".md" else "notes_text",
        "word_count": word_count,
        "headers_found": headers,
        "exam_hints_detected": exam_hints[:10]  # top 10 hints
    }


def parse_transcript(file_path: Path) -> dict:
    """Parses spoken audio/video transcripts (VTT, SRT, or TXT)."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    # Clean SRT / VTT timestamps if present
    cleaned = re.sub(r'\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[\.,]\d{3}', '', raw)
    cleaned = re.sub(r'^\d+$', '', cleaned, flags=re.MULTILINE)
    
    # Search for professor emphasis keywords
    emphases = re.findall(r'(?:guaranteed|crucial|make sure you know|exam question|points for|focus on)[^\.\n]*[\.\n]', cleaned, re.IGNORECASE)
    exclusions = re.findall(r'(?:not in the exam|excluded|dont worry about|skip this|no need to learn)[^\.\n]*[\.\n]', cleaned, re.IGNORECASE)

    return {
        "filename": file_path.name,
        "type": "audio_transcript",
        "word_count": len(cleaned.split()),
        "professor_emphases": emphases[:15],
        "professor_exclusions": exclusions[:10]
    }


def scan_materials_root(root_dir: Path, output_json: Path = None) -> dict:
    """Scans all non-slide course material folders."""
    manifest = {
        "notes": [],
        "transcripts": [],
        "past_exams": [],
        "syllabus": []
    }

    for file_path in root_dir.glob("**/*"):
        if file_path.is_dir() or file_path.name.startswith("."):
            continue

        ext = file_path.suffix.lower()
        rel = file_path.relative_to(root_dir)

        if "exam" in str(rel).lower():
            manifest["past_exams"].append({
                "filename": file_path.name,
                "path": str(rel),
                "is_solution": "solution" in file_path.name.lower()
            })
        elif "syllabus" in str(rel).lower() or "overview" in str(rel).lower() or "admin" in str(rel).lower():
            manifest["syllabus"].append({
                "filename": file_path.name,
                "path": str(rel)
            })
        elif ext in [".vtt", ".srt"] or "recording" in str(rel).lower() or "transcript" in str(rel).lower():
            if ext in [".txt", ".vtt", ".srt", ".md"]:
                manifest["transcripts"].append(parse_transcript(file_path))
            else:
                manifest["transcripts"].append({"filename": file_path.name, "path": str(rel), "type": "media_file"})
        elif ext in [".md", ".txt", ".docx"]:
            manifest["notes"].append(parse_text_or_markdown(file_path))

    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved multi-modal materials manifest to: {output_json}")

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Parse non-slide course materials (transcripts, notes, past exams).")
    parser.add_argument("-i", "--input", default="Course_Materials", help="Root materials directory")
    parser.add_argument("-o", "--output", default="Knowledge_Ledger/materials_manifest.json", help="Output JSON path")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    if not input_path.exists():
        input_path.mkdir(parents=True, exist_ok=True)

    scan_materials_root(input_path, output_path)


if __name__ == "__main__":
    main()
