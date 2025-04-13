# 文献检索和问答系统
这是一个基于MCP（Model Context Protocol）的文献检索和问答系统，能够根据用户提供的关键词获取相关文献，并回显文献内容。

## 功能特点
- 根据客户端（例如Claude等大语言模型）提供的关键词搜索高影响因子文献
- 支持自定义影响因子阈值
- 提供文献的标题、期刊、影响因子、DOI和URL等信息
- 展示完整文献摘要

## 配置和运行
1. 在`.env`文件中配置必要的环境变量：
   ```
   Cookie="您的X-MOL网站Cookie"
   Impact=8  # 文献最低影响因子
   lang=zh   # 语言设置
   ```

2. 使用uv安装依赖：
   ```bash
   uv pip install -e .
   ```
   
   或者安装开发依赖：
   ```bash
   uv pip install -e ".[dev]"
   ```

3. 使用uv运行服务器：
   ```bash
   # 标准IO模式（默认）
   uv run run.py
   
   # SSE模式（HTTP服务器）
   uv run run.py --transport sse --port 8000
   ```

4. 或者使用MCP工具（需要安装开发依赖）：
   ```bash
   # 开发模式
   mcp dev xmol/server.py
   
   # 安装到Claude桌面应用
   mcp install xmol/server.py
   ```

## 使用方法
1. 向服务发送学术问题
2. 提供相关的关键词（1-3个效果最佳）
3. 系统会根据关键词搜索文献，并返回文献内容

## 搜索技巧
- 提供精确的专业术语作为关键词
- 关键词数量控制在1-3个之间（超过3个可能导致搜索结果过少）
- 可以调整影响因子阈值以获取不同质量的文献

## 可用工具
- search_title_by_keywords: 根据关键词搜索文献，返回标题列表
- get_literature_detail: 根据DOI获取文献的详细信息


## 工作流程
1. 用户提出学术问题
2. 用户或大语言模型提供关键词列表
3. 系统根据关键词检索文献
4. 系统展示文献内容，帮助用户理解相关知识

## 项目结构
```
xmol/
├── .env                # 环境变量配置
├── .gitignore          # Git忽略文件
├── .python-version     # Python版本配置
├── README.md           # 项目说明文档  
├── pyproject.toml      # 项目依赖和配置
├── run.py              # 启动脚本
├── uv.lock             # UV锁文件
└── xmol/               # 主模块
    ├── __init__.py     # 包初始化
    ├── server.py       # MCP服务器实现
    └── core/           # 核心功能模块
        ├── __init__.py # 核心模块初始化
        ├── content.py  # 文献内容获取
        └── logger.py   # 日志配置
```