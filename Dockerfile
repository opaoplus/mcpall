FROM python:3.11-slim

WORKDIR /app

# 安装基础工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制整个项目
COPY . /app/

# 安装通用依赖
RUN pip install --no-cache-dir "mcp[cli]>=1.6.0" uv

# 设置环境变量
ENV PYTHONPATH=/app

# 构建参数，用于指定要运行的模块和传输方式
ARG MODULE=useronlie
ARG TRANSPORT=stdio
ARG HOST=0.0.0.0
ARG PORT=8000

# 设置启动命令
CMD cd /app/${MODULE} && python -m uv run run.py --transport ${TRANSPORT} --host ${HOST} --port ${PORT} 