#!/usr/bin/env python3
"""
Generate Claude Code command files from custom-slash-commands config.json
This creates actual slash command files in ~/.claude/commands/

Usage:
    python generate_commands.py          # Sync commands (create/update only if needed)
    python generate_commands.py --check # Check if any sync is needed
    python generate_commands.py --force # Force sync all commands
"""

import argparse
import hashlib
import json
import os
import sys
import tempfile
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
    return {"config_hash": None, "generated_at": None, "commands": {}}

def save_state(config_hash, commands_state):
    """Save generation state with per-command hashes"""
    state = {
        "config_hash": config_hash,
        "generated_at": datetime.now().isoformat(),
        "command_count": len(commands_state),
        "commands": commands_state
    }
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_command_file_path(cmd_name):
    """Return Path object for command file"""
    return COMMANDS_DIR / f"{cmd_name}.md"

def compute_command_content(command, prefix, description, workflow):
    """Generate expected file content."""
    if prefix:
        cmd_name = f"{prefix}-{command}"
    else:
        cmd_name = command

    content = f"""---
description: {description}
---

"""
    if workflow and len(workflow) > 0:
        content += "执行以下步骤：\n\n"
        for i, step in enumerate(workflow, 1):
            content += f"{i}. {step}\n"
    else:
        content += f"{description}\n"

    return cmd_name, content

def get_file_content_hash(file_path):
    """Get MD5 hash of existing file content, None if doesn't exist"""
    if not file_path.exists():
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return hashlib.md5(f.read().encode()).hexdigest()
    except (IOError, UnicodeDecodeError):
        return None

def sync_commands(dry_run=False, force=False):
    """
    Sync commands with smart update logic.

    Returns: {
        "created": [cmd_names],
        "updated": [cmd_names],
        "skipped": [cmd_names],
        "errors": [(cmd_name, error)]
    }
    """
    config = load_config()
    commands = config.get("commands", [])

    # Ensure commands directory exists
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    result = {
        "created": [],
        "updated": [],
        "skipped": [],
        "errors": []
    }
    commands_state = {}

    for cmd in commands:
        command = cmd.get("command", "")
        prefix = cmd.get("prefix", "")
        description = cmd.get("description", "")
        workflow = cmd.get("workflow", [])

        cmd_name, expected_content = compute_command_content(command, prefix, description, workflow)
        file_path = get_command_file_path(cmd_name)
        expected_hash = hashlib.md5(expected_content.encode()).hexdigest()

        try:
            existing_hash = get_file_content_hash(file_path)

            if existing_hash is None:
                # File doesn't exist - create it
                if not dry_run:
                    write_file_atomically(file_path, expected_content)
                result["created"].append(cmd_name)
            elif existing_hash != expected_hash:
                # File exists but content differs - update it
                if not dry_run:
                    write_file_atomically(file_path, expected_content)
                result["updated"].append(cmd_name)
            else:
                # Content same - skip
                result["skipped"].append(cmd_name)
        except Exception as e:
            result["errors"].append((cmd_name, str(e)))

        commands_state[cmd_name] = {
            "hash": expected_hash,
            "prefix": prefix,
            "command": command
        }

    return result

def write_file_atomically(file_path, content):
    """Write content to temp file then rename (atomic operation)"""
    dir_name = file_path.parent
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=dir_name, delete=False) as tmp:
        tmp.write(content)
        tmp_name = tmp.name
    # Atomic rename - won't leave partial file on crash
    os.replace(tmp_name, file_path)

def needs_sync():
    """Check if any command needs sync (create or update)"""
    config = load_config()
    commands = config.get("commands", [])

    for cmd in commands:
        command = cmd.get("command", "")
        prefix = cmd.get("prefix", "")
        description = cmd.get("description", "")
        workflow = cmd.get("workflow", [])

        cmd_name, expected_content = compute_command_content(command, prefix, description, workflow)
        file_path = get_command_file_path(cmd_name)
        expected_hash = hashlib.md5(expected_content.encode()).hexdigest()

        existing_hash = get_file_content_hash(file_path)

        if existing_hash is None:
            return True, f"Command '{cmd_name}' is missing"
        if existing_hash != expected_hash:
            return True, f"Command '{cmd_name}' has outdated content"

    return False, "All commands are up to date"

def main():
    parser = argparse.ArgumentParser(description="Sync Claude Code command files")
    parser.add_argument("--check", action="store_true", help="Check if sync is needed")
    parser.add_argument("--force", action="store_true", help="Force sync all commands")
    args = parser.parse_args()

    # Check mode
    if args.check:
        needs_regen, reason = needs_sync()
        if needs_regen:
            print(f"NEEDS_SYNC: {reason}")
            sys.exit(0)
        else:
            print(f"UP_TO_DATE: {reason}")
            sys.exit(0)

    # Force mode or normal mode
    if args.force:
        print("FORCE: Syncing all command files...")
    else:
        needs_regen, reason = needs_sync()
        if not needs_regen:
            state = load_state()
            print(f"Commands are up to date (generated at {state.get('generated_at', 'unknown')})")
            print("Use --force to sync anyway")
            sys.exit(0)
        print(f"SYNCING: {reason}")

    # Sync commands
    result = sync_commands()

    # Save state
    config_hash = get_config_hash()
    commands_state = {}
    for cmd_list, status in [
        (result["created"], "created"),
        (result["updated"], "updated"),
        (result["skipped"], "skipped")
    ]:
        for cmd_name in cmd_list:
            commands_state[cmd_name] = {"status": status}
    save_state(config_hash, commands_state)

    # Output results
    print(f"\nSync complete:")
    print(f"  Created: {len(result['created'])}")
    print(f"  Updated: {len(result['updated'])}")
    print(f"  Skipped: {len(result['skipped'])}")
    if result["errors"]:
        print(f"  Errors: {len(result['errors'])}")
        for cmd_name, err in result["errors"]:
            print(f"    - {cmd_name}: {err}")

    if result["created"]:
        print("\nNew commands created:")
        for cmd in sorted(result["created"])[:10]:
            print(f"  - /{cmd}")
        if len(result["created"]) > 10:
            print(f"  ... and {len(result['created']) - 10} more")

    if result["updated"]:
        print("\nCommands updated:")
        for cmd in sorted(result["updated"])[:10]:
            print(f"  - /{cmd}")
        if len(result["updated"]) > 10:
            print(f"  ... and {len(result['updated']) - 10} more")

    print("\nPlease restart Claude Code to use the updated commands")

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()