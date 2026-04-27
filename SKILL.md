---
name: custom-slash-commands
description: Custom slash command framework for Claude Code. Use when users want to create, manage, or execute their own slash commands like /dev-cmd-code-review, /stock-cmd-query, or any custom command with prefix grouping. Manages a configuration file that defines command name, prefix, description, and optional workflow steps. This skill reads the config file and executes the appropriate command workflow based on the user's slash command invocation.
---

# Custom Slash Commands Framework

A flexible framework that lets you define and execute custom slash commands for Claude Code. Define your own commands with simple JSON configuration.

## How It Works

1. **You invoke a custom slash command** (e.g., `/dev-cmd-code-review`)
2. **Skill loads your config** from `config.json`
3. **Skill finds the matching command** by command name or alias
4. **Skill executes the workflow** described in the command definition
5. **Results are returned** based on the command type

## Command Execution

When a custom slash command is invoked:

### Step 1: Load Configuration
Read `config.json` from the skill directory to get all command definitions.

### Step 2: Match Command
Find the command entry where `command` matches the invoked slash command name (without the `/` prefix).

### Step 3: Execute
For the matched command:
- If `workflow` array has steps, execute them in order
- If `workflow` is empty, use the `description` as instructions for an LLM-native approach
- Return execution results or status

## Configuration File Format

`config.json` should contain:

```json
{
  "commands": [
    {
      "command": "code-review",
      "prefix": "dev-cmd",
      "description": "执行代码审查，检查质量、安全、最佳实践",
      "workflow": [
        "执行git diff查看当前变更",
        "进行全面代码审查，检查安全漏洞",
        "检查代码质量、一致性、错误处理",
        "输出审查报告"
      ]
    },
    {
      "command": "commit",
      "prefix": "dev-cmd",
      "description": "提交代码到远程仓库，自动生成提交信息",
      "workflow": []
    }
  ]
}
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Command name (e.g., "code-review") |
| `prefix` | No | Prefix for grouping (e.g., "dev-cmd") |
| `description` | Yes | What this command does (used when workflow is empty) |
| `workflow` | No | Array of workflow steps to execute in order |

## Design Principles

1. **Simplicity**: Configuration over code. Most commands need only a description.
2. **Flexibility**: Workflow steps are optional — the LLM can handle complex tasks from descriptions alone.
3. **Organization**: Commands are grouped by prefix for easy management.
4. **Portability**: Fork the project, modify config.json, share with others.

## Example Commands

### Development Commands
- `/dev-cmd-code-review` — 执行代码审查
- `/dev-cmd-commit` — 提交代码到远程仓库
- `/dev-cmd-update-docs` — 更新项目文档

### Stock Commands
- `/stock-cmd-query` — 查询股票数据
- `/stock-cmd-buy` — 买入股票
- `/stock-cmd-sell` — 卖出股票

### Custom Commands
- `/my-cmd-backup` — 备份项目文件
- `/my-cmd-deploy` — 部署应用到服务器

## Workflow Execution

When executing a workflow:
1. **Parse steps** from the workflow array
2. **Execute each step** using appropriate tools
3. **Collect results** from each step
4. **Return summary** of what was accomplished

Steps can be:
- Shell commands (bash commands)
- File operations (read, write, edit)
- API calls (if needed)
- Or any task the LLM can perform from text description

## Notes

- Commands are invoked by their full name (prefix + command)
- If no workflow is defined, the skill uses the description to guide execution
- Config file supports Chinese and English descriptions
- Workflow steps can reference each other or be independent
