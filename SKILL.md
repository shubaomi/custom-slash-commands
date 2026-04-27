---
name: custom-slash-commands
description: Custom slash commands framework. Use /custom-slash-commands to activate, or directly use commands like /dev-cmd-code-review, /stock-cmd-query after installation.
---

# Custom Slash Commands Framework

This skill provides a comprehensive set of slash commands for development, stock trading, design, operations, data analysis, project management, security, and API work.

## Initial Setup (Auto-Activate on First Use)

When this skill is first invoked, it will automatically:

1. **Check command files**: Verify that slash command files exist in `~/.claude/commands/`
2. **Auto-generate if missing**: If commands are not found, run the generation script to create them
3. **Show ready status**: Display available commands and usage information

## Commands Overview

### Development Commands (dev-cmd)
- `/dev-cmd-code-review` - 执行代码审查，检查代码质量、安全漏洞、最佳实践和错误处理
- `/dev-cmd-commit` - 提交代码到远程仓库，自动生成规范的提交信息并推送
- `/dev-cmd-update-docs` - 更新项目的需求、设计、进度和记忆文档
- `/dev-cmd-test` - 运行项目测试并生成测试报告
- `/dev-cmd-build` - 构建项目，生成可部署的产物
- `/dev-cmd-lint` - 检查代码风格问题并自动修复
- `/dev-cmd-debug` - 启动调试会话，帮助定位和解决问题
- `/dev-cmd-git-status` - 查看 Git 仓库状态，包括变更、分支和提交历史
- `/dev-cmd-git-pull` - 拉取远程最新代码并合并到当前分支
- `/dev-cmd-standup` - 生成站会报告，记录今日完成、明日计划和 blockers
- `/dev-cmd-meeting-notes` - 整理会议纪要，包括讨论要点、决策和行动项
- `/dev-cmd-log-time` - 记录工时到时间跟踪系统
- `/dev-cmd-gen-tests` - 根据代码变更自动生成测试用例

### Stock Trading Commands (stock-cmd)
- `/stock-cmd-query` - 查询股票实时行情数据
- `/stock-cmd-buy` - 分析股票并推荐买入价格和策略
- `/stock-cmd-sell` - 分析股票并推荐卖出价格和策略
- `/stock-cmd-analyze` - 对股票进行技术分析（MA、RSI、MACD、布林带、成交量）
- `/stock-cmd-predict` - 基于历史数据和技术指标进行价格预测分析
- `/stock-cmd-recommend` - 根据筛选条件推荐合适的股票
- `/stock-cmd-alerts` - 设置股票价格提醒
- `/stock-cmd-portfolio` - 分析投资组合，计算盈亏和风险指标
- `/stock-cmd-history` - 查询股票历史数据

### Design Commands (design-cmd)
- `/design-cmd-mockup` - 根据描述生成UI设计稿或页面布局建议
- `/design-cmd-color-palette` - 根据主题或现有配色生成配色方案
- `/design-cmd-font-pair` - 推荐适合项目的字体搭配方案
- `/design-cmd-icon-suggest` - 根据功能需求推荐合适的图标方案
- `/design-cmd-design-review` - 审查现有设计稿，提出改进建议

### Operations Commands (ops-cmd)
- `/ops-cmd-deploy` - 部署应用到指定环境
- `/ops-cmd-rollback` - 回滚应用到上一个稳定版本
- `/ops-cmd-logs` - 查看应用日志，支持过滤和搜索
- `/ops-cmd-health-check` - 检查应用和服务健康状态
- `/ops-cmd-backup` - 备份数据库或文件
- `/ops-cmd-restore` - 从备份恢复数据库或文件
- `/ops-cmd-migrate` - 执行数据库迁移
- `/ops-cmd-scale` - 扩缩容应用实例

### Data Commands (data-cmd)
- `/data-cmd-query` - 查询数据，支持条件过滤和排序
- `/data-cmd-export` - 导出数据到指定格式（CSV、Excel、JSON）
- `/data-cmd-import` - 导入数据到数据库
- `/data-cmd-stats` - 生成数据统计分析报告

### Project Management Commands (pm-cmd)
- `/pm-cmd-tasks` - 管理项目任务，增删改查
- `/pm-cmd-sprint` - 管理冲刺，创建冲刺、分配任务、查看进度
- `/pm-cmd-report` - 生成项目进度报告
- `/pm-cmd-risk` - 识别和管理项目风险

### Security Commands (sec-cmd)
- `/sec-cmd-scan` - 执行安全扫描，检查漏洞
- `/sec-cmd-audit` - 安全审计，检查权限和访问记录
- `/sec-cmd-secrets` - 检查代码中是否泄露密钥或凭证

### API Commands (api-cmd)
- `/api-cmd-test` - 测试 API 接口
- `/api-cmd-docs` - 根据代码生成或更新 API 文档
- `/api-cmd-mock` - 根据 API 描述生成 Mock 数据

## Activation Process

When invoked, this skill performs the following:

### Step 1: Check Command Status
Execute: `ls ~/.claude/commands/dev-cmd-*.md 2>/dev/null | wc -l`
If the count is 0 or files are missing, proceed to Step 2.

### Step 2: Generate Commands (If Needed)
If commands are not found, execute:
```
python ~/.claude/skills/custom-slash-commands/scripts/generate_commands.py
```
Or on Windows:
```
python %USERPROFILE%/.claude/skills/custom-slash-commands/scripts/generate_commands.py
```

### Step 3: Display Welcome
Show a formatted welcome message with:
- Number of commands available
- Command categories with counts
- Quick start examples

## Command Configuration

Commands are defined in `config.json` at:
`~/.claude/skills/custom-slash-commands/config.json`

### Adding New Commands
To add a new command:
1. Edit `config.json` and add a new entry in the `commands` array
2. The next time this skill is invoked, commands will be automatically regenerated

### Command Format
```json
{
  "command": "command-name",
  "prefix": "prefix-name",
  "description": "What this command does",
  "workflow": ["Step 1", "Step 2", "Step 3"]
}
```

## Troubleshooting

### Commands not appearing
If slash commands like `/dev-cmd-code-review` don't appear:
1. Restart Claude Code
2. Invoke this skill: `/custom-slash-commands`
3. Check that commands are generated in `~/.claude/commands/`

### Regenerate Commands
To force regeneration of all command files:
1. Delete files in `~/.claude/commands/` matching `*-cmd-*.md`
2. Invoke this skill or run the generation script manually

## Quick Start

```bash
# See all available commands
/custom-slash-commands

# Direct usage examples
/dev-cmd-code-review     # Start code review
/dev-cmd-commit          # Commit changes
/stock-cmd-query AAPL    # Query stock price
/ops-cmd-health-check    # Check system health
```

---
*Total: 49 commands across 8 categories*