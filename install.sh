#!/usr/bin/env bash
# ==============================================================================
# Universal AI Study Engine (study-agent-skills) — Multi-Harness Installer
# Compatible with Google Antigravity, Claude Code, Cursor, Windsurf
# ==============================================================================

set -e

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$(pwd)"
INSTALL_MODE="symlink"
HARNESS="auto"

print_banner() {
  echo "=================================================================="
  echo " 🎓 Universal AI Study Engine — Multi-Harness Skill Installer"
  echo "=================================================================="
}

show_help() {
  echo "Usage: ./install.sh [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  -t, --target <path>    Target course directory (default: current directory)"
  echo "  -m, --mode <mode>      Installation mode: 'symlink' (default) or 'copy'"
  echo "  --antigravity          Install specifically for Google Antigravity (.agents/skills)"
  echo "  --claude               Install specifically for Claude Code (.claude/skills)"
  echo "  --cursor               Install specifically for Cursor (.cursor/skills & .cursor/rules)"
  echo "  --windsurf             Install specifically for Windsurf (.windsurf/skills)"
  echo "  --all                  Install for all supported agent harnesses"
  echo "  -h, --help             Show this help message"
  echo ""
}

# Parse Arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -t|--target) TARGET_DIR="$2"; shift ;;
    -m|--mode) INSTALL_MODE="$2"; shift ;;
    --antigravity) HARNESS="antigravity" ;;
    --claude) HARNESS="claude" ;;
    --cursor) HARNESS="cursor" ;;
    --windsurf) HARNESS="windsurf" ;;
    --all) HARNESS="all" ;;
    -h|--help) show_help; exit 0 ;;
    *) echo "Unknown option: $1"; show_help; exit 1 ;;
  esac
  shift
done

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

link_or_copy() {
  local src="$1"
  local dest="$2"

  mkdir -p "$(dirname "$dest")"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    rm -rf "$dest"
  fi

  if [ "$INSTALL_MODE" == "copy" ]; then
    cp -r "$src" "$dest"
    echo "  [COPIED]  $dest"
  else
    ln -sf "$src" "$dest"
    echo "  [LINKED]  $dest -> $src"
  fi
}

install_antigravity() {
  echo "📦 Installing for Google Antigravity..."
  local dest_skills="$TARGET_DIR/.agents/skills"
  mkdir -p "$dest_skills"
  
  for skill in course-setup study-session mock-exam; do
    link_or_copy "$SOURCE_DIR/skills/$skill" "$dest_skills/$skill"
  done

  # Also install plugin bundle if directory exists
  mkdir -p "$TARGET_DIR/.agents/plugins"
  link_or_copy "$SOURCE_DIR/plugins/study-agent-kit" "$TARGET_DIR/.agents/plugins/study-agent-kit"
}

install_claude() {
  echo "📦 Installing for Claude Code..."
  local dest_skills="$TARGET_DIR/.claude/skills"
  mkdir -p "$dest_skills"

  for skill in course-setup study-session mock-exam; do
    link_or_copy "$SOURCE_DIR/skills/$skill" "$dest_skills/$skill"
  done

  if [ ! -f "$TARGET_DIR/CLAUDE.md" ]; then
    cp "$SOURCE_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
    echo "  [CREATED] $TARGET_DIR/CLAUDE.md"
  fi
}

install_cursor() {
  echo "📦 Installing for Cursor..."
  local dest_rules="$TARGET_DIR/.cursor/rules"
  local dest_skills="$TARGET_DIR/.cursor/skills"
  mkdir -p "$dest_rules" "$dest_skills"

  for rule in "$SOURCE_DIR/.cursor/rules"/*.mdc; do
    if [ -f "$rule" ]; then
      link_or_copy "$rule" "$dest_rules/$(basename "$rule")"
    fi
  done

  for skill in course-setup study-session mock-exam; do
    link_or_copy "$SOURCE_DIR/skills/$skill" "$dest_skills/$skill"
  done

  if [ ! -f "$TARGET_DIR/.cursorrules" ]; then
    cp "$SOURCE_DIR/.cursorrules" "$TARGET_DIR/.cursorrules"
    echo "  [CREATED] $TARGET_DIR/.cursorrules"
  fi
}

install_windsurf() {
  echo "📦 Installing for Windsurf..."
  local dest_skills="$TARGET_DIR/.windsurf/skills"
  mkdir -p "$dest_skills"

  for skill in course-setup study-session mock-exam; do
    link_or_copy "$SOURCE_DIR/skills/$skill" "$dest_skills/$skill"
  done
}

print_banner
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo "Mode:   $INSTALL_MODE"
echo ""

if [ "$HARNESS" == "all" ]; then
  install_antigravity
  install_claude
  install_cursor
  install_windsurf
elif [ "$HARNESS" == "antigravity" ]; then
  install_antigravity
elif [ "$HARNESS" == "claude" ]; then
  install_claude
elif [ "$HARNESS" == "cursor" ]; then
  install_cursor
elif [ "$HARNESS" == "windsurf" ]; then
  install_windsurf
else
  # Auto-detection: install to standard .agents / .claude / .cursor if found, or install universal .agents
  echo "🔍 Auto-detecting harness environments in target workspace..."
  detected=0

  if [ -d "$TARGET_DIR/.agents" ] || command -v agy &> /dev/null; then
    install_antigravity
    detected=1
  fi
  if [ -d "$TARGET_DIR/.claude" ] || [ -f "$TARGET_DIR/CLAUDE.md" ]; then
    install_claude
    detected=1
  fi
  if [ -d "$TARGET_DIR/.cursor" ] || [ -f "$TARGET_DIR/.cursorrules" ]; then
    install_cursor
    detected=1
  fi

  if [ $detected -eq 0 ]; then
    echo "ℹ️ No specific harness directory detected. Installing standard Antigravity & Universal .agents format..."
    install_antigravity
    install_claude
    install_cursor
  fi
fi

# Ensure workspace scaffold exists if directory is completely empty
if [ ! -d "$TARGET_DIR/Course_Materials" ]; then
  mkdir -p "$TARGET_DIR/Course_Materials/01_Lecture_Slides"
  mkdir -p "$TARGET_DIR/Course_Materials/02_Notes_and_Summaries"
  mkdir -p "$TARGET_DIR/Course_Materials/03_Past_Exams_and_Solutions"
  mkdir -p "$TARGET_DIR/Course_Materials/04_Syllabus_and_Admin"
  echo "📁 Scaffolded clean Course_Materials/ directory structure."
fi

echo ""
echo "✅ Installation complete!"
echo "👉 Next step: Drop your course lecture PDFs/notes into 'Course_Materials/' and tell your AI agent:"
echo "   \"Set up my study tutor for [Course Name]\""
echo "=================================================================="
