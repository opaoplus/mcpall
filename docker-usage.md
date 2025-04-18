# Docker 部署指南

## 概述

本文档介绍如何使用 Docker 和 Docker Compose 部署和运行 MCPALL 项目的各个模块。

## 前提条件

- 安装 [Docker](https://docs.docker.com/get-docker/)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)

## 部署方式

### 方式一：使用 Docker Compose（推荐）

Docker Compose 配置文件已经预设了各个模块的不同运行模式，您可以根据需要启动特定的服务。

```bash
# 构建所有服务
docker-compose build

# 启动特定服务（例如 useronlie 模块的 SSE 模式）
docker-compose up useronlie-sse

# 启动特定服务（例如 xmol 模块的 SSE 模式）
docker-compose up xmol-sse

# 后台运行服务
docker-compose up -d useronlie-sse

# 停止所有服务
docker-compose down
```

### 方式二：直接使用 Docker

您也可以直接使用 Docker 命令来构建和运行特定模块，更灵活地指定端口和参数。

```bash
# 构建镜像（通用镜像，不传递任何特定参数）
docker build -t mcpall .

# 运行容器 (SSE 模式)，可自由指定端口映射
docker run -p 8000:8000 -e MODULE=useronlie -e TRANSPORT=sse -e HOST=0.0.0.0 -e PORT=8000 mcpall

# 运行其他模块，使用不同端口
docker run -p 8001:8001 -e MODULE=xmol -e TRANSPORT=sse -e HOST=0.0.0.0 -e PORT=8001 mcpall

# 运行容器 (STDIO 模式，交互式)
docker run -it -e MODULE=useronlie -e TRANSPORT=stdio mcpall
```

### 同时运行多个模块

您可以同时运行多个不同的模块，只需确保它们使用不同的端口：

```bash
# 启动多个服务
docker-compose up -d useronlie-sse xmol-sse

# 或者使用原始 Docker 命令
docker run -d -p 8000:8000 -e MODULE=useronlie -e TRANSPORT=sse -e PORT=8000 mcpall
docker run -d -p 8001:8001 -e MODULE=xmol -e TRANSPORT=sse -e PORT=8001 mcpall
```

## 添加新模块

1. 按照项目开发指南添加新模块到项目中
2. 修改 `docker-compose.yml` 文件，添加新的服务配置：

```yaml
new-module-sse:
  build:
    context: .
  environment:
    - MODULE=new_module
    - TRANSPORT=sse
    - HOST=0.0.0.0
    - PORT=8002
  ports:
    - "8002:8002"

new-module-stdio:
  build:
    context: .
  environment:
    - MODULE=new_module
    - TRANSPORT=stdio
  stdin_open: true
  tty: true
```

## 使用 uv 运行 Python 

容器内部使用 `python -m uv run` 命令来运行 Python 脚本，这样可以利用 uv 的性能优势。这与项目标准的运行方式一致，默认使用 uv 运行模块。

```dockerfile
# 使用 uv 运行 (默认)
CMD cd /app/${MODULE} && python -m uv run run.py --transport ${TRANSPORT} --host ${HOST} --port ${PORT}

# 如果需要使用普通 Python 运行
# CMD cd /app/${MODULE} && python run.py --transport ${TRANSPORT} --host ${HOST} --port ${PORT}
```

## 环境变量

您可以通过环境变量自定义容器的行为：

- `MODULE`：指定要运行的模块名称
- `TRANSPORT`：指定传输方式，可选 `stdio` 或 `sse`
- `HOST`：在 SSE 模式下的监听地址
- `PORT`：在 SSE 模式下的监听端口

## 配置设计说明

本项目的 Docker 配置采用了一种简化但灵活的设计理念：

1. **单一通用镜像**：
   - 我们构建一个通用的基础镜像，不包含任何特定模块的配置
   - Dockerfile 中定义了默认参数值，但这些值仅在未指定环境变量时使用

2. **运行时配置**：
   - 所有模块特定的配置都在运行容器时通过环境变量传入
   - 这样可以使用同一个镜像运行不同的模块和配置

这种设计有以下优点：
- 更简洁的配置文件
- 更好的资源利用（不需要为每个模块构建单独的镜像）
- 灵活性更高（可以在运行时动态决定要运行的模块和配置）

## 端口管理

在 Docker 容器中，端口管理完全通过 `-p` 参数或 docker-compose.yml 中的 ports 配置实现，无需在 Dockerfile 中使用 EXPOSE 指令：

```bash
# 将容器内的 8000 端口映射到主机的 8000 端口
docker run -p 8000:8000 -e PORT=8000 ...

# 将容器内的 8000 端口映射到主机的 9000 端口
docker run -p 9000:8000 -e PORT=8000 ...

# 一个容器同时运行多个端口(不常用)
docker run -p 8000:8000 -p 8001:8001 ...
```

**注意**：确保容器内应用程序设置的端口（通过 PORT 环境变量）与 Docker 的端口映射中的容器端口一致。

## 与 Claude 集成

当使用 SSE 模式运行服务后，可以按照以下步骤将其集成到 Claude Desktop：

1. 修改 Claude Desktop 配置文件（`%AppData%\Claude\claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "useronlie": {
      "isActive": true,
      "name": "用户在线查询服务",
      "url": "http://localhost:8000/sse"
    },
    "xmol": {
      "isActive": true,
      "name": "文献检索系统",
      "url": "http://localhost:8001/sse"
    }
  }
}
```

2. 重启 Claude Desktop 应用使配置生效

## 常见问题

1. **端口冲突**：如果出现端口冲突，可以通过 `-p` 参数指定不同的主机端口
2. **交互式运行**：对于 STDIO 模式，确保使用 `-it` 参数和 `stdin_open: true` 以及 `tty: true` 配置
3. **数据持久化**：如需持久化数据，请添加适当的卷映射配置：

```yaml
services:
  useronlie-sse:
    # ... 其他配置 ...
    volumes:
      - ./data/useronlie:/app/useronlie/data
``` 