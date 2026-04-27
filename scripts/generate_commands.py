#!/usr/bin/env python3
"""
Generate Claude Code command files from custom-slash-commands config.json
This creates actual slash command files in ~/.claude/commands/

Usage:
    python generate_commands.py          # Generate all commands
    python generate_commands.py --check # Check if regeneration is needed
    python generate_commands.py --force # Force regeneration even if up-to-date
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from datetime import datetime

COMMANDS_DIR = Path.home() / ".claude" / "commands"
SKILL_DIR = Path(__file__).parent.parent
STATE_FILE = SKILL_DIR / ".command_state"

def load_config():
    """Load configuration from config.json"""
    config_path = SKILL_DIR / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_config_hash():
    """Get hash of config.json for change detection"""
    config_path = SKILL_DIR / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return hashlib.md5(f.read().encode()).hexdigest()

def load_state():
    """Load previous generation state"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"config_hash": None, "generated_at": None}

def save_state(config_hash):
    """Save generation state"""
    state = {
        "config_hash": config_hash,
        "generated_at": datetime.now().isoformat(),
        "command_count": 49  # Will be updated during generation
    }
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def check_commands_exist(prefix_filter=None):
    """Check how many command files exist"""
    if not COMMANDS_DIR.exists():
        return 0

    pattern = "*-cmd-*.md" if prefix_filter is None else f"{prefix_filter}-cmd-*.md"
    files = list(COMMANDS_DIR.glob(pattern))
    return len(files)

def needs_regeneration():
    """Check if command files need to be regenerated"""
    state = load_state()
    current_hash = get_config_hash()

    # Check if config changed
    if state.get("config_hash") != current_hash:
        return True, "Config changed"

    # Check if command files exist
    count = check_commands_exist()
    if count < 49:  # Total expected commands
        return True, f"Only {count} commands found, expected 49"

    return False, "Up to date"

def generate_command_file(command, prefix, description, workflow):
    """Generate a command markdown file content."""
    # Command name is prefix-command or just command if no prefix
    if prefix:
        cmd_name = f"{prefix}-{command}"
    else:
        cmd_name = command

    # Build the command content
    content = f"""---
description: {description}
---

"""
    # Add workflow steps if available
    if workflow and len(workflow) > 0:
        content += "执行以下步骤：\n\n"
        for i, step in enumerate(workflow, 1):
            content += f"{i}. {step}\n"
    else:
        # Use description as the main instruction
        content += f"{description}\n"

    return content

def generate_all_commands():
    """Generate all command files from config"""
    config = load_config()
    commands = config.get("commands", [])

    # Ensure commands directory exists
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    for cmd in commands:
        command = cmd.get("command", "")
        prefix = cmd.get("prefix", "")
        description = cmd.get("description", "")
        workflow = cmd.get("workflow", [])

        if prefix:
            cmd_name = f"{prefix}-{command}"
        else:
            cmd_name = command

        # Generate content
        content = generate_command_file(command, prefix, description, workflow)

        # Write command file
        cmd_file = COMMANDS_DIR / f"{cmd_name}.md"
        with open(cmd_file, 'w', encoding='utf-8') as f:
            f.write(content)

        generated.append(f"/{cmd_name}")

    return generated

def main():
    parser = argparse.ArgumentParser(description="Generate Claude Code command files")
    parser.add_argument("--check", action="store_true", help="Check if regeneration is needed")
    parser.add_argument("--force", action="store_true", help="Force regeneration")
    args = parser.parse_args()

    # Check mode
    if args.check:
        needs_regen, reason = needs_regeneration()
        if needs_regen:
            print(f"NEEDS_REGENERATION: {reason}")
            sys.exit(0)
        else:
            print(f"UP_TO_DATE: {reason}")
            sys.exit(0)

    # Force mode or normal mode
    if args.force:
        print("FORCE: Regenerating all command files...")
    else:
        needs_regen, reason = needs_regeneration()
        if not needs_regen:
            state = load_state()
            print(f"Commands are up to date (generated at {state.get('generated_at', 'unknown')})")
            print("Use --force to regenerate anyway")
            sys.exit(0)
        print(f"REGENERATING: {reason}")

    # Generate commands
    config = load_config()
    commands = config.get("commands", [])
    generated = generate_all_commands()

    # Save state
    config_hash = get_config_hash()
    save_state(config_hash)

    print(f"\nGenerated {len(generated)} command files to {COMMANDS_DIR}")
    for cmd in sorted(generated)[:10]:
        print(f"  - {cmd}")
    if len(generated) > 10:
        print(f"  ... and {len(generated) - 10} more")

    print("\nPlease restart Claude Code to use the new commands")

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()