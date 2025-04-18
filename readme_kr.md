# MCPALL

<div align="center">

![버전](https://img.shields.io/badge/버전-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen)
![MCP](https://img.shields.io/badge/MCP-1.6.0%2B-orange)
![라이선스](https://img.shields.io/badge/라이선스-MIT-green)

</div>

<div align="center">
  
[中文](./readme.md) | [English](./readme_en.md) | [日本語](./readme_jp.md) | [한국어](./readme_kr.md)

</div>

## 📑 프로젝트 개요

MCPALL은 Model Context Protocol (MCP)를 기반으로 한 다기능 서비스 모음 플랫폼으로, 다양한 MCP 서비스의 신속한 개발 및 통합을 지원합니다. 이 플랫폼은 높은 모듈화를 갖추어 새로운 서비스 모듈을 쉽게 확장할 수 있도록 설계되었습니다.

## 🚀 현재 모듈

| 모듈명 | 설명 | 상세 링크 |
|-------|-----|----------|
| 📞 **useronlie** | 사용자 전화 조회 서비스 | [상세 보기](./useronlie/README.md) |
| 📚 **xmol** | 문헌 검색 및 질의응답 시스템 | [상세 보기](./xmol/README.md) |

## 🛠️ 기술 스택

- **Python 3.11+**: 핵심 개발 언어
- **FastMCP**: MCP 프로토콜 구현 프레임워크
- **통신 프로토콜**: HTTP/SSE 및 STDIO 두 가지 전송 방식 지원

## ⚙️ 일반 개발 가이드

### 환경 설정

```bash
# Python 3.11+ 설치 확인
python --version

# MCP 프레임워크 설치
pip install "mcp[cli]>=1.6.0"

# 의존성 관리 도구로 uv 사용 권장
pip install uv
```

### 모듈 구조 표준

각 새 모듈은 다음과 같은 기본 구조를 따라야 합니다:

```
module_name/
├── core/               # 핵심 기능 구현
│   ├── __init__.py
│   ├── server.py       # MCP 서버 구현
│   └── ...             # 기타 기능 모듈
├── README.md           # 모듈 상세 문서
├── run.py              # 시작 스크립트
├── pyproject.toml      # 프로젝트 설정
└── ...                 # 기타 설정 파일
```

### 새 모듈 개발 단계

1. **모듈 디렉토리 구조 생성**
   ```bash
   mkdir -p new_module/core
   touch new_module/{README.md,run.py,pyproject.toml}
   touch new_module/core/{__init__.py,server.py}
   ```

2. **MCP 서버 구현**
   ```python
   # new_module/core/server.py (기본 프레임워크)
   from fastmcp import McpServer, Tool, Resource

   class NewModuleServer(McpServer):
       def __init__(self):
           super().__init__("새 모듈 이름")
           # 도구 및 리소스 등록
           self.register_tool(Tool("도구 이름", self.tool_handler))
           self.register_resource("resource://path", self.resource_handler)
   
       async def tool_handler(self, params):
           # 도구 로직 구현
           return {"result": "도구 실행 결과"}
   
       async def resource_handler(self, params):
           # 리소스 액세스 로직 구현
           return {"data": "리소스 내용"}
   ```

3. **시작 스크립트 생성**
   ```python
   # new_module/run.py
   import asyncio
   import argparse
   from core.server import NewModuleServer
   
   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
       parser.add_argument("--host", default="127.0.0.1")
       parser.add_argument("--port", type=int, default=8000)
       args = parser.parse_args()
   
       server = NewModuleServer()
       
       if args.transport == "stdio":
           asyncio.run(server.run_stdio())
       else:
           asyncio.run(server.run_sse(host=args.host, port=args.port))
   
   if __name__ == "__main__":
       main()
   ```

4. **프로젝트 의존성 설정**
   ```toml
   # new_module/pyproject.toml
   [build-system]
   requires = ["setuptools>=61.0"]
   build-backend = "setuptools.build_meta"
   
   [project]
   name = "new_module"
   version = "0.1.0"
   requires-python = ">=3.11"
   dependencies = [
       "mcp>=1.6.0",
   ]
   ```

5. **모듈 README 작성**
   각 모듈은 자체 README 파일을 가지고 있어야 하며, 기능, 설정 및 사용 방법을 상세히 설명해야 합니다.

## 🚀 범용 실행 방법

모든 모듈은 두 가지 실행 모드를 지원합니다:

```bash
# STDIO 모드 (Claude Desktop과 직접 통합에 적합)
cd <module_name>
python run.py

# SSE 모드 (HTTP 서비스로 실행)
cd <module_name>
python run.py --transport sse --host 127.0.0.1 --port 8000
```

## 🏗️ Claude와 통합

1. Claude Desktop 설정 (`%AppData%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "<서비스 이름>": {
      "isActive": true,
      "name": "<표시 이름>",
      "url": "http://localhost:<포트>/sse"
    }
  }
}
```

2. 설정을 적용하기 위해 Claude Desktop 애플리케이션을 재시작합니다

## 🔧 확장 가능한 생태계

MCPALL은 무한히 확장 가능한 서비스 생태계로 설계되었습니다. 다음은 몇 가지 잠재적인 확장 방향입니다:

- **데이터 처리 서비스**: 데이터 분석, 시각화, 보고서 생성
- **AI 보조 도구**: 텍스트 생성, 이미지 처리, 음성 인식
- **개발 도구 체인**: 코드 생성, 프로젝트 관리, 테스트 자동화
- **지식 베이스 서비스**: 문서 검색, 지식 그래프, Q&A 시스템
- **운영 모니터링**: 시스템 상태, 성능 모니터링, 로그 분석

MCPALL 플랫폼에 서비스를 추가하려면 위의 개발 표준을 따라 모듈 디렉토리를 프로젝트 루트에 추가하기만 하면 됩니다.

## 📋 MCP 서비스 개발 핵심 개념

### 도구 (Tools)

도구는 MCP 서비스가 제공하는 특정 작업을 수행하기 위한 호출 가능한 함수입니다.

```python
# 도구 정의 예시
@server.tool("도구 이름")
async def tool_handler(params):
    # 매개변수 처리 및 비즈니스 로직
    return {"result": "처리 결과"}
```

### 리소스 (Resources)

리소스는 MCP 서비스가 제공하는 데이터 액세스 포인트로, URI로 식별됩니다.

```python
# 리소스 정의 예시
@server.resource("resource://path")
async def resource_handler(params):
    # 리소스 액세스 로직
    return {"data": "리소스 내용"}
```

### 리소스 스키마 (Schema)

스키마 정의를 통해 리소스의 구조와 유효성 검사 규칙을 선언할 수 있습니다.

```python
# 리소스 스키마 예시
resource_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "data": {"type": "array", "items": {"type": "string"}}
    }
}
```

더 자세한 개발 정보는 [MCP 개발 문서](https://github.com/anthropics/anthropic-cookbook/tree/main/mcp)를 참조하세요.

## 📄 라이선스

MIT

## 👥 기여 가이드라인

1. 프로젝트 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경 사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📮 연락처

- 프로젝트 관리자: [귀하의 이름](mailto:your-email@example.com)
- 프로젝트 저장소: [GitHub](https://github.com/your-username/mcpall) 