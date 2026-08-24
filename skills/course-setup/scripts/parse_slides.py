#!/usr/bin/env python3
"""
Slide Deck Parser for Course Setup
Extracts slide titles, bullet points, in-slide exercises, equations, and figures from lecture PDFs.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF using pdftotext CLI, pypdf, or pdfplumber if available."""
    # 1. Try pdftotext CLI (fastest & cleanest layout)
    try:
        res = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if res.stdout.strip():
            return res.stdout
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # 2. Try pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        text = "\n--- SLIDE ---\n".join([page.extract_text() or "" for page in reader.pages])
        if text.strip():
            return text
    except ImportError:
        pass

    # 3. Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            text = "\n--- SLIDE ---\n".join([page.extract_text() or "" for page in pdf.pages])
            if text.strip():
                return text
    except ImportError:
        pass

    return ""


def parse_slides_text(raw_text: str, filename: str) -> dict:
    """Parses raw extracted text into structured slide objects."""
    # Split by form-feed or slide markers
    raw_slides = re.split(r'\x0c|(?:\n--- SLIDE ---\n)', raw_text)
    slides_data = []

    exercise_keywords = [
        r'\bexercise\b', r'\bscenario\b', r'\bquestion\b', r'\bcase study\b',
        r'\bdiscussion\b', r'\bproblem\b', r'\btask\b', r'\bdilemma\b',
        r'\bcalculate\b', r'\bcompute\b', r'\bexample problem\b'
    ]
    exercise_pattern = re.compile('|'.join(exercise_keywords), re.IGNORECASE)

    for idx, slide_content in enumerate(raw_slides, start=1):
        lines = [line.strip() for line in slide_content.split('\n') if line.strip()]
        if not lines:
            continue

        title = lines[0] if lines else f"Slide {idx}"
        body = lines[1:] if len(lines) > 1 else []
        full_slide_str = " ".join(lines)

        is_exercise = bool(exercise_pattern.search(full_slide_str))
        
        # Check for formulas / math symbols
        has_formulas = bool(re.search(r'[=<>+\-*/∑∫√±]|(?:\bR\s*=\s*)|(?:\bP\s*\*\s*S\b)', full_slide_str))

        slides_data.append({
            "slide_number": idx,
            "title": title,
            "content": lines,
            "is_exercise": is_exercise,
            "has_formulas": has_formulas
        })

    return {
        "filename": filename,
        "total_slides": len(slides_data),
        "exercises_found": sum(1 for s in slides_data if s["is_exercise"]),
        "slides": slides_data
    }


def process_directory(slides_dir: Path, output_json: Path = None) -> dict:
    """Processes all PDF files in directory."""
    results = {}
    pdf_files = sorted(list(slides_dir.glob("*.pdf")) + list(slides_dir.glob("**/*.pdf")))

    print(f"📄 Found {len(pdf_files)} PDF slide deck(s) in {slides_dir}")

    for pdf in pdf_files:
        print(f"  Parsing: {pdf.name} ...")
        text = extract_text_from_pdf(pdf)
        if text:
            parsed = parse_slides_text(text, pdf.name)
            results[pdf.name] = parsed
            print(f"    -> {parsed['total_slides']} slides, {parsed['exercises_found']} exercise/scenario slides found.")
        else:
            print(f"    [WARN] Could not extract text from {pdf.name}")

    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Saved structured slide audit to: {output_json}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Parse lecture slide PDFs into structured audit data.")
    parser.add_argument("-i", "--input", default="Course_Materials/01_Lecture_Slides", help="Directory containing slide PDFs")
    parser.add_argument("-o", "--output", default="Knowledge_Ledger/slides_audit.json", help="Output JSON path")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    if not input_path.exists():
        print(f"Directory {input_path} does not exist. Creating it.")
        input_path.mkdir(parents=True, exist_ok=True)
        sys.exit(0)

    process_directory(input_path, output_path)


if __name__ == "__main__":
    main()
