# Custom Slash Commands Framework

一个灵活的框架，让你为 Claude Code 定义和使用自定义斜杠命令。通过简单的 JSON 配置文件，你可以创建自己的命令，如 `/dev-cmd-code-review`、`/stock-cmd-query` 等。

## 功能特点

- **自定义命令**：创建任意数量的斜杠命令
- **前缀分组**：按前缀对命令进行分组（如 `dev-cmd-*`、`stock-cmd-*`）
- **简单配置**：只需 JSON 配置文件，无需编写代码
- **工作流支持**：可选的工作流步骤定义，也可仅用描述驱动
- **社区分享**：Fork 项目，分享你的命令配置给其他人

## 安装指南

### 方式一：npx 一键安装（推荐）

```bash
npx skills add git@github.com:shubaomi/custom-slash-commands.git -g -a claude-code -y
```

### 方式二：Git 克隆安装

```bash
# 克隆仓库
git clone git@github.com:shubaomi/custom-slash-commands.git

# 复制到 Claude Code 的 skills 目录
cp -r custom-slash-commands ~/.claude/skills/custom-slash-commands

# 重启 Claude Code 即可使用
```

### 方式三：下载 .skill 文件安装

1. 从 GitHub Release 或 Actions 页下载 `.skill` 文件
2. 将 `custom-slash-commands.skill` 文件复制到 `~/.claude/skills/` 目录
3. 重启 Claude Code

### 方式四：直接 Fork 自定义

如果你想自定义命令：
1. Fork 仓库到你的 GitHub
2. 克隆你的 Fork
3. 复制到 `~/.claude/skills/` 目录
4. 根据需要修改 `config.json`

## 快速开始

### 1. 配置你的命令

编辑 `config.json` 文件，添加你需要的命令：

```json
{
  "commands": [
    {
      "command": "code-review",
      "prefix": "dev-cmd",
      "description": "执行代码审查，检查代码质量",
      "workflow": []
    }
  ]
}
```

### 2. 使用命令

在 Claude Code 中直接使用：

```
/your-prefix-your-command
```

例如：
- `/dev-cmd-code-review` — 执行代码审查
- `/dev-cmd-commit` — 提交代码
- `/stock-cmd-query` — 查询股票

### 3. 自定义工作流（可选）

如果命令需要特定的工作流步骤，添加 `workflow` 数组：

```json
{
  "command": "commit",
  "prefix": "dev-cmd",
  "description": "提交代码到远程仓库",
  "workflow": [
    "执行 git status 查看当前状态",
    "生成提交信息",
    "执行 git commit",
    "执行 git push"
  ]
}
```

## 配置指南

### 配置文件位置

配置文件 `config.json` 位于 skill 目录内：

```
custom-slash-commands/
├── SKILL.md       # Skill 主文件
├── config.json    # 配置文件
└── README.md     # 本文档
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

### 配置示例

```json
{
  "commands": [
    {
      "command": "code-review",
      "prefix": "dev-cmd",
      "description": "执行代码审查，检查质量、安全、最佳实践",
      "workflow": [
        "执行git diff查看当前变更",
        "进行全面代码审查",
        "输出审查报告"
      ]
    },
    {
      "command": "commit",
      "prefix": "dev-cmd",
      "description": "提交代码到远程仓库",
      "workflow": []
    },
    {
      "command": "update-docs",
      "prefix": "dev-cmd",
      "description": "更新需求文档、设计文档、进度文档和记忆文档",
      "workflow": []
    }
  ]
}
```

## 预设命令列表

以下命令在默认配置中提供，可根据需要修改或删除：

### 开发命令（dev-cmd）- 13 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/dev-cmd-code-review` | 执行代码审查，检查质量、安全、最佳实践 | ✅ 完整 |
| `/dev-cmd-commit` | 提交代码到远程仓库，自动生成提交信息 | ✅ 完整 |
| `/dev-cmd-update-docs` | 更新项目的需求、设计、进度和记忆文档 | ✅ 完整 |
| `/dev-cmd-test` | 运行项目测试并生成测试报告 | ✅ 完整 |
| `/dev-cmd-build` | 构建项目，生成可部署的产物 | ✅ 完整 |
| `/dev-cmd-lint` | 检查代码风格问题并自动修复 | ✅ 完整 |
| `/dev-cmd-debug` | 启动调试会话，帮助定位和解决问题 | ✅ 完整 |
| `/dev-cmd-git-status` | 查看 Git 仓库状态 | ✅ 完整 |
| `/dev-cmd-git-pull` | 拉取远程最新代码 | ✅ 完整 |
| `/dev-cmd-standup` | 生成站会报告 | ✅ 完整 |
| `/dev-cmd-meeting-notes` | 整理会议纪要 | ✅ 完整 |
| `/dev-cmd-log-time` | 记录工时 | ✅ 完整 |
| `/dev-cmd-gen-tests` | 根据变更自动生成测试用例 | ✅ 完整 |

### 股票命令（stock-cmd）- 9 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/stock-cmd-query` | 查询股票实时行情数据 | ✅ 完整 |
| `/stock-cmd-buy` | 分析股票并推荐买入价格和策略 | ✅ 完整 |
| `/stock-cmd-sell` | 分析股票并推荐卖出价格和策略 | ✅ 完整 |
| `/stock-cmd-analyze` | 技术分析（MA、RSI、MACD、布林带） | ✅ 完整 |
| `/stock-cmd-predict` | 基于历史数据的价格预测分析 | ✅ 完整 |
| `/stock-cmd-recommend` | 根据条件推荐合适的股票 | ✅ 完整 |
| `/stock-cmd-alerts` | 设置股票价格提醒 | ✅ 完整 |
| `/stock-cmd-portfolio` | 分析投资组合，计算盈亏和风险 | ✅ 完整 |
| `/stock-cmd-history` | 查询股票历史数据 | ✅ 完整 |

### 设计命令（design-cmd）- 5 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/design-cmd-mockup` | 根据描述生成UI设计稿或页面布局建议 | ✅ 完整 |
| `/design-cmd-color-palette` | 根据主题生成配色方案 | ✅ 完整 |
| `/design-cmd-font-pair` | 推荐适合项目的字体搭配方案 | ✅ 完整 |
| `/design-cmd-icon-suggest` | 根据功能需求推荐合适的图标方案 | ✅ 完整 |
| `/design-cmd-design-review` | 审查现有设计稿，提出改进建议 | ✅ 完整 |

### 运维命令（ops-cmd）- 8 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/ops-cmd-deploy` | 部署应用到指定环境 | ✅ 完整 |
| `/ops-cmd-rollback` | 回滚应用到上一个稳定版本 | ✅ 完整 |
| `/ops-cmd-logs` | 查看应用日志，支持过滤和搜索 | ✅ 完整 |
| `/ops-cmd-health-check` | 检查应用和服务健康状态 | ✅ 完整 |
| `/ops-cmd-backup` | 备份数据库或文件 | ✅ 完整 |
| `/ops-cmd-restore` | 从备份恢复数据库或文件 | ✅ 完整 |
| `/ops-cmd-migrate` | 执行数据库迁移 | ✅ 完整 |
| `/ops-cmd-scale` | 扩缩容应用实例 | ✅ 完整 |

### 数据命令（data-cmd）- 4 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/data-cmd-query` | 查询数据，支持条件过滤和排序 | ✅ 完整 |
| `/data-cmd-export` | 导出数据到指定格式（CSV、Excel、JSON） | ✅ 完整 |
| `/data-cmd-import` | 导入数据到数据库 | ✅ 完整 |
| `/data-cmd-stats` | 生成数据统计分析报告 | ✅ 完整 |

### 项目管理命令（pm-cmd）- 4 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/pm-cmd-tasks` | 管理项目任务，增删改查 | ✅ 完整 |
| `/pm-cmd-sprint` | 管理冲刺，创建冲刺、分配任务、查看进度 | ✅ 完整 |
| `/pm-cmd-report` | 生成项目进度报告 | ✅ 完整 |
| `/pm-cmd-risk` | 识别和管理项目风险 | ✅ 完整 |

### 安全命令（sec-cmd）- 3 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/sec-cmd-scan` | 执行安全扫描，检查漏洞 | ✅ 完整 |
| `/sec-cmd-audit` | 安全审计，检查权限和访问记录 | ✅ 完整 |
| `/sec-cmd-secrets` | 检查代码中是否泄露密钥或凭证 | ✅ 完整 |

### API 命令（api-cmd）- 3 个

| 命令 | 描述 | 工作流 |
|------|------|--------|
| `/api-cmd-test` | 测试 API 接口 | ✅ 完整 |
| `/api-cmd-docs` | 根据代码生成或更新 API 文档 | ✅ 完整 |
| `/api-cmd-mock` | 根据 API 描述生成 Mock 数据 | ✅ 完整 |

## 常见问题

### Q: 如何添加新命令？

编辑 `config.json`，在 `commands` 数组中添加新条目：

```json
{
  "command": "新命令名",
  "prefix": "前缀",
  "description": "命令描述",
  "workflow": []
}
```

### Q: workflow 数组可以为空吗？

可以！如果 workflow 为空数组，skill 会根据 description 的描述来驱动执行。LLM 可以理解自然语言描述并执行相应的任务。

### Q: 可以跨平台使用吗？

可以！配置文件是标准 JSON，支持 Windows、macOS、Linux。

### Q: 如何分享我的命令配置？

1. Fork 这个仓库
2. 修改 `config.json` 添加你的命令
3. 提交并推送到你的 Fork
4. 分享你的仓库地址

### Q: 命令冲突了怎么办？

如果多个命令有相同的名称，skill 会执行第一个匹配的命令。建议使用唯一的前缀来避免冲突。

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
