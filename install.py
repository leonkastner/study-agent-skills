#!/usr/bin/env python3
"""
Universal AI Study Engine (study-agent-skills) — Python Multi-Harness Installer
Cross-platform installation tool for Antigravity, Claude Code, Cursor, Windsurf.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def print_banner():
    print("=" * 66)
    print(" 🎓 Universal AI Study Engine — Multi-Harness Skill Installer (Python)")
    print("=" * 66)


def link_or_copy(src: Path, dest: Path, mode: str = "symlink"):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()

    if mode == "copy":
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print(f"  [COPIED]  {dest}")
    else:
        try:
            os.symlink(src, dest, target_is_directory=src.is_dir())
            print(f"  [LINKED]  {dest} -> {src}")
        except OSError:
            # Fallback to copy on systems where symlinks fail (e.g. Windows without dev mode)
            if src.is_dir():
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
            print(f"  [COPIED]  {dest} (symlink fallback)")


def main():
    parser = argparse.ArgumentParser(description="Install study-agent-skills into course workspace.")
    parser.add_argument("-t", "--target", default=".", help="Target course directory (default: current directory)")
    parser.add_argument("-m", "--mode", choices=["symlink", "copy"], default="symlink", help="Install mode")
    parser.add_argument("--antigravity", action="store_true", help="Install for Google Antigravity")
    parser.add_argument("--claude", action="store_true", help="Install for Claude Code")
    parser.add_argument("--cursor", action="store_true", help="Install for Cursor")
    parser.add_argument("--windsurf", action="store_true", help="Install for Windsurf")
    parser.add_argument("--all", action="store_true", help="Install for all supported agent harnesses")

    args = parser.parse_args()

    source_dir = Path(__file__).resolve().parent
    target_dir = Path(args.target).resolve()

    print_banner()
    print(f"Source: {source_dir}")
    print(f"Target: {target_dir}")
    print(f"Mode:   {args.mode}\n")

    skills = ["course-setup", "study-session", "mock-exam"]

    def install_antigravity():
        print("📦 Installing for Google Antigravity...")
        dest_skills = target_dir / ".agents" / "skills"
        for s in skills:
            link_or_copy(source_dir / "skills" / s, dest_skills / s, args.mode)
        plugin_src = source_dir / "plugins" / "study-agent-kit"
        if plugin_src.exists():
            link_or_copy(plugin_src, target_dir / ".agents" / "plugins" / "study-agent-kit", args.mode)

    def install_claude():
        print("📦 Installing for Claude Code...")
        dest_skills = target_dir / ".claude" / "skills"
        for s in skills:
            link_or_copy(source_dir / "skills" / s, dest_skills / s, args.mode)
        claude_md = source_dir / "CLAUDE.md"
        if claude_md.exists() and not (target_dir / "CLAUDE.md").exists():
            shutil.copy2(claude_md, target_dir / "CLAUDE.md")
            print(f"  [CREATED] {target_dir / 'CLAUDE.md'}")

    def install_cursor():
        print("📦 Installing for Cursor...")
        dest_rules = target_dir / ".cursor" / "rules"
        dest_skills = target_dir / ".cursor" / "skills"
        for r in (source_dir / ".cursor" / "rules").glob("*.mdc"):
            link_or_copy(r, dest_rules / r.name, args.mode)
        for s in skills:
            link_or_copy(source_dir / "skills" / s, dest_skills / s, args.mode)
        cursorrules = source_dir / ".cursorrules"
        if cursorrules.exists() and not (target_dir / ".cursorrules").exists():
            shutil.copy2(cursorrules, target_dir / ".cursorrules")
            print(f"  [CREATED] {target_dir / '.cursorrules'}")

    def install_windsurf():
        print("📦 Installing for Windsurf...")
        dest_skills = target_dir / ".windsurf" / "skills"
        for s in skills:
            link_or_copy(source_dir / "skills" / s, dest_skills / s, args.mode)

    if args.all:
        install_antigravity()
        install_claude()
        install_cursor()
        install_windsurf()
    elif args.antigravity:
        install_antigravity()
    elif args.claude:
        install_claude()
    elif args.cursor:
        install_cursor()
    elif args.windsurf:
        install_windsurf()
    else:
        # Auto-detect or default to universal
        print("🔍 Auto-detecting harness environments in target workspace...")
        detected = False
        if (target_dir / ".agents").exists():
            install_antigravity()
            detected = True
        if (target_dir / ".claude").exists() or (target_dir / "CLAUDE.md").exists():
            install_claude()
            detected = True
        if (target_dir / ".cursor").exists() or (target_dir / ".cursorrules").exists():
            install_cursor()
            detected = True

        if not detected:
            print("ℹ️ No specific harness detected. Installing standard Antigravity, Claude Code & Cursor configurations...")
            install_antigravity()
            install_claude()
            install_cursor()

    # Scaffold course materials folder structure
    materials_dir = target_dir / "Course_Materials"
    for sub in ["01_Lecture_Slides", "02_Notes_and_Summaries", "03_Past_Exams_and_Solutions", "04_Syllabus_and_Admin"]:
        (materials_dir / sub).mkdir(parents=True, exist_ok=True)
    print("📁 Scaffolded clean Course_Materials/ directory structure.")

    print("\n✅ Installation complete!")
    print("👉 Next step: Drop your course lecture PDFs/notes into 'Course_Materials/' and tell your AI agent:")
    print("   \"Set up my study tutor for [Course Name]\"")
    print("=" * 66)


if __name__ == "__main__":
    main()
