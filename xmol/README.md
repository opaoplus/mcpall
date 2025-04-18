# 📚 XMol文献检索助手

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

基于**MCP**（Model Context Protocol）的学术文献检索助手，能够帮助用户快速查找、理解和分析高影响因子学术文献。结合Claude等大语言模型使用，为科研人员提供强大的文献调研工具。

## ✨ 主要功能

- 🔍 **智能文献检索** - 根据关键词组合搜索高质量学术文献
- 📊 **灵活过滤** - 支持自定义影响因子阈值筛选文献质量
- 📄 **完整元数据** - 提供文献标题、期刊、影响因子、DOI和URL等信息
- 📝 **摘要解析** - 自动提取并展示文献摘要内容
- 🔄 **多协议支持** - 支持SSE和STDIO两种通信模式

## 🛠️ 安装与配置

### 环境配置

1. 在`.env`文件中设置必要的环境变量：

```bash
Cookie="您的X-MOL网站Cookie"  # 必需
Impact=8                    # 文献最低影响因子(可选)
lang=zh                     # 语言设置(可选，zh或en)
```

### 安装依赖

```bash
# 使用uv安装依赖
uv pip install -e .

# 或安装开发依赖
uv pip install -e ".[dev]"
```

## 🚀 运行服务

```bash
# 标准IO模式（默认）
uv run run.py

# SSE模式（HTTP服务器）
uv run run.py --transport sse --port 8000 --host 127.0.0.1 --ssepath /sse

# 带Cookie参数运行
uv run run.py --cookie "您的X-MOL网站Cookie" --transport sse

```

## ⚙️ 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--transport` | 传输协议 (`stdio`或`sse`) | `stdio` |
| `--port` | 服务器端口号 | `8000` |
| `--host` | 服务器主机地址 | `0.0.0.0` |
| `--ssepath` | SSE路径 | `/sse` |


## 🔌 与Claude集成

### 在Claude桌面应用中配置

1. 打开Claude桌面应用配置文件：

```bash
# Windows
%APPDATA%\Claude\claude_desktop_config.json

# macOS
~/Library/Application Support/Claude/claude_desktop_config.json
```

2. 添加MCP服务器配置：

```json
{
  "mcpServers": {
    "xmol": {
      "command": "uv",
      "args": [
        "--directory",
        "/path",
        "run",
        "run.py"
      ]
    }
  }
}
```

## 📖 使用指南

### 基本流程

1. 向服务发送学术问题
2. Claude会分析问题并提供相关关键词
3. 系统根据关键词检索文献并返回结果
4. 选择感兴趣的文献获取详细信息

### 💡 搜索技巧

- ✅ **精确术语** - 使用专业术语而非通用词汇获得更精准的结果
- ✅ **关键词数量** - 控制在1-3个之间获得最佳搜索结果
- ✅ **多组搜索** - 尝试多组关键词组合以获得全面覆盖
- ✅ **影响因子调整** - 根据研究领域特点调整影响因子阈值

## 🔧 可用工具

### `search_title_by_keywords`

根据关键词搜索文献，返回标题列表。

**参数：**
- `keywords`: 关键词列表，例如 `["CRISPR", "遗传疾病"]`
- `impact_factor`: 影响因子下限（可选）
- `page_index`: 页码，默认为1
- `searchSort`: 排序方式，可选值:
  - `publishDate`: 按发布日期排序
  - `default`: 按相关性排序

### `get_literature_detail`

根据DOI获取文献的详细信息。

**参数：**
- `doi`: 文献的DOI标识符

## 📁 项目结构

```
./
├── .env                # 环境变量配置
├── .gitignore          # Git忽略文件
├── README.md           # 项目说明文档  
├── pyproject.toml      # 项目依赖和配置
├── run.py              # 启动脚本
├── cache/              # 缓存目录
└── core/               # 核心功能模块
    ├── __init__.py     # 核心模块初始化
    ├── server.py       # MCP服务器实现
    └── content/        # 内容获取模块
        ├── __init__.py # 内容模块初始化
        ├── content.py  # 文献内容获取
        └── logger.py   # 日志配置
```

## ⚠️ 注意事项

- 需要有效的X-MOL网站Cookie才能正常使用
- 影响因子阈值会影响搜索结果的质量和数量
- SSE模式下可通过Web浏览器或支持SSE的客户端访问服务
- 首次搜索可能需要较长时间，请耐心等待

## 📄 许可证

MIT