# Custom Slash Commands Framework

一个灵活的框架，让你为 Claude Code 定义和使用自定义斜杠命令。通过简单的 JSON 配置文件，你可以创建自己的命令，如 `/dev-cmd-code-review`、`/stock-cmd-query` 等。

## 功能特点

- **安装即用**：安装后自动激活，无需手动运行脚本
- **自更新**：修改 config.json 后自动重新生成命令
- **对话管理**：通过对话方式添加、更新、删除命令
- **49+ 预设命令**：涵盖开发、股票、设计、运维、数据、项目管理、安全、API 等领域

## 安装指南

### 方式一：npx 一键安装（推荐）

```bash
npx skills add https://github.com/shubaomi/custom-slash-commands.git -g -a claude-code -y
```

> 如果在 Windows 环境下遇到问题，可以手动克隆安装（方式二）。

### 方式二：Git 克隆安装

```bash
# 克隆仓库
git clone https://github.com/shubaomi/custom-slash-commands.git

# 复制到 Claude Code 的 skills 目录
cp -r custom-slash-commands ~/.claude/skills/custom-slash-commands
```

### 方式三：下载 .skill 文件安装

1. 从 [GitHub Releases](https://github.com/shubaomi/custom-slash-commands/releases) 下载 `.skill` 文件
2. 将 `custom-slash-commands.skill` 文件复制到 `~/.claude/skills/` 目录

---

## 快速开始

### 1. 安装后自动激活

安装 skill 后，输入以下命令启动自动激活：

```
/custom-slash-commands
```

这将自动：
1. 检查命令文件是否存在
2. 如缺失，自动生成 49 个命令文件
3. 展示命令菜单和使用说明

### 2. 直接使用命令

激活完成后，即可直接使用各类命令：

| 命令示例 | 说明 |
|---------|------|
| `/dev-cmd-code-review` | 代码审查 |
| `/dev-cmd-commit` | 提交代码 |
| `/stock-cmd-query AAPL` | 查询股票行情 |
| `/ops-cmd-health-check` | 健康检查 |
| `/design-cmd-mockup` | 生成 UI 设计建议 |

### 3. 通过对话管理命令

添加新命令：
```
/custom-slash-commands
# 请添加一个新命令 /my-cmd-deploy 用于部署应用到服务器
```

查看所有命令：
```
/custom-slash-commands
# 展示所有可用命令
```

## 配置指南

### 配置文件位置

`config.json` 位于 skill 目录内：

```
custom-slash-commands/
├── SKILL.md              # Skill 主文件（自激活逻辑）
├── config.json            # 命令配置
├── scripts/
│   └── generate_commands.py  # 命令生成脚本
└── README.md             # 本文档
```

### 配置字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `command` | 是 | 命令名称（不含前缀），如 "code-review" |
| `prefix` | 否 | 前缀，用于分组，如 "dev-cmd" |
| `description` | 是 | 命令描述，定义命令的功能 |
| `workflow` | 否 | 工作流步骤数组，为空时使用 description 驱动 |

### 命令命名规则

命令的完整名称 = `前缀-命令名`

例如：
- prefix: `dev-cmd`，command: `code-review`
- 完整命令: `/dev-cmd-code-review`

### 通过对话添加/修改命令

当你输入 `/custom-slash-commands` 并描述需求时，skill 会：
1. 解析你的需求
2. 修改 config.json
3. 自动重新生成命令文件
4. 让你立即使用新命令

## 预设命令列表

### 开发命令（dev-cmd）- 13 个

| 命令 | 描述 |
|------|------|
| `/dev-cmd-code-review` | 执行代码审查，检查质量、安全、最佳实践 |
| `/dev-cmd-commit` | 提交代码到远程仓库，自动生成提交信息 |
| `/dev-cmd-update-docs` | 更新项目的需求、设计、进度和记忆文档 |
| `/dev-cmd-test` | 运行项目测试并生成测试报告 |
| `/dev-cmd-build` | 构建项目，生成可部署的产物 |
| `/dev-cmd-lint` | 检查代码风格问题并自动修复 |
| `/dev-cmd-debug` | 启动调试会话，帮助定位和解决问题 |
| `/dev-cmd-git-status` | 查看 Git 仓库状态 |
| `/dev-cmd-git-pull` | 拉取远程最新代码 |
| `/dev-cmd-standup` | 生成站会报告 |
| `/dev-cmd-meeting-notes` | 整理会议纪要 |
| `/dev-cmd-log-time` | 记录工时 |
| `/dev-cmd-gen-tests` | 根据变更自动生成测试用例 |

### 股票命令（stock-cmd）- 9 个

| 命令 | 描述 |
|------|------|
| `/stock-cmd-query` | 查询股票实时行情数据 |
| `/stock-cmd-buy` | 分析股票并推荐买入价格和策略 |
| `/stock-cmd-sell` | 分析股票并推荐卖出价格和策略 |
| `/stock-cmd-analyze` | 技术分析（MA、RSI、MACD、布林带） |
| `/stock-cmd-predict` | 基于历史数据的价格预测分析 |
| `/stock-cmd-recommend` | 根据条件推荐合适的股票 |
| `/stock-cmd-alerts` | 设置股票价格提醒 |
| `/stock-cmd-portfolio` | 分析投资组合，计算盈亏和风险 |
| `/stock-cmd-history` | 查询股票历史数据 |

### 设计命令（design-cmd）- 5 个

| 命令 | 描述 |
|------|------|
| `/design-cmd-mockup` | 根据描述生成UI设计稿或页面布局建议 |
| `/design-cmd-color-palette` | 根据主题或现有配色生成配色方案 |
| `/design-cmd-font-pair` | 推荐适合项目的字体搭配方案 |
| `/design-cmd-icon-suggest` | 根据功能需求推荐合适的图标方案 |
| `/design-cmd-design-review` | 审查现有设计稿，提出改进建议 |

### 运维命令（ops-cmd）- 8 个

| 命令 | 描述 |
|------|------|
| `/ops-cmd-deploy` | 部署应用到指定环境 |
| `/ops-cmd-rollback` | 回滚应用到上一个稳定版本 |
| `/ops-cmd-logs` | 查看应用日志，支持过滤和搜索 |
| `/ops-cmd-health-check` | 检查应用和服务健康状态 |
| `/ops-cmd-backup` | 备份数据库或文件 |
| `/ops-cmd-restore` | 从备份恢复数据库或文件 |
| `/ops-cmd-migrate` | 执行数据库迁移 |
| `/ops-cmd-scale` | 扩缩容应用实例 |

### 数据命令（data-cmd）- 4 个

| 命令 | 描述 |
|------|------|
| `/data-cmd-query` | 查询数据，支持条件过滤和排序 |
| `/data-cmd-export` | 导出数据到指定格式（CSV、Excel、JSON） |
| `/data-cmd-import` | 导入数据到数据库 |
| `/data-cmd-stats` | 生成数据统计分析报告 |

### 项目管理命令（pm-cmd）- 4 个

| 命令 | 描述 |
|------|------|
| `/pm-cmd-tasks` | 管理项目任务，增删改查 |
| `/pm-cmd-sprint` | 管理冲刺，创建冲刺、分配任务、查看进度 |
| `/pm-cmd-report` | 生成项目进度报告 |
| `/pm-cmd-risk` | 识别和管理项目风险 |

### 安全命令（sec-cmd）- 3 个

| 命令 | 描述 |
|------|------|
| `/sec-cmd-scan` | 执行安全扫描，检查漏洞 |
| `/sec-cmd-audit` | 安全审计，检查权限和访问记录 |
| `/sec-cmd-secrets` | 检查代码中是否泄露密钥或凭证 |

### API 命令（api-cmd）- 3 个

| 命令 | 描述 |
|------|------|
| `/api-cmd-test` | 测试 API 接口 |
| `/api-cmd-docs` | 根据代码生成或更新 API 文档 |
| `/api-cmd-mock` | 根据 API 描述生成 Mock 数据 |

## 常见问题

### Q: 命令没有出现？

1. 确保 Claude Code 已重启
2. 输入 `/custom-slash-commands` 触发自动激活
3. 检查 `~/.claude/commands/` 目录下是否有 `*-cmd-*.md` 文件

### Q: 如何强制重新生成所有命令？

```
/custom-slash-commands
# 强制重新生成所有命令文件
```

或手动运行：
```bash
python ~/.claude/skills/custom-slash-commands/scripts/generate_commands.py --force
```

### Q: 如何分享我的命令配置？

1. Fork 这个仓库
2. 修改 `config.json` 添加你的命令
3. 提交并推送到你的 Fork
4. 分享你的仓库地址

## 工作原理

`★ Insight ─────────────────────────────────────`
**双层架构**：这个 skill 有两层工作机制：
1. **Skill 层**（`~/.claude/skills/custom-slash-commands/`）：存储配置和生成脚本
2. **Commands 层**（`~/.claude/commands/`）：实际的 slash 命令文件

当你使用 `/custom-slash-commands` 时，skill 会自动把 config.json 转换为命令文件，实现"安装即用"。
`─────────────────────────────────────────────────`

## 贡献指南

欢迎贡献你的命令配置！

### 提交新命令

1. Fork 本仓库
2. 添加你的命令到 `config.json`
3. 提交 Pull Request
4. 描述你的命令用途和使用方法

### 分享模板

如果你创建了通用的命令模板（如开发流程、股票交易等），欢迎分享！

## 许可证

MIT License - 自由使用、修改和分享

---

*如果你觉得这个框架有用，请给项目一个 Star！*