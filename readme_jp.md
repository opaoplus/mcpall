# MCPALL

<div align="center">

![バージョン](https://img.shields.io/badge/バージョン-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen)
![MCP](https://img.shields.io/badge/MCP-1.6.0%2B-orange)
![ライセンス](https://img.shields.io/badge/ライセンス-MIT-green)

</div>

<div align="center">
  
[中文](./readme.md) | [English](./readme_en.md) | [日本語](./readme_jp.md) | [한국어](./readme_kr.md)

</div>

## 📑 プロジェクト概要

MCPALLは、Model Context Protocol (MCP)に基づく多機能サービス集合プラットフォームで、様々なMCPサービスの迅速な開発と統合をサポートします。このプラットフォームは高度にモジュール化されており、新しいサービスモジュールを簡単に拡張できるように設計されています。

## 🚀 現在のモジュール

| モジュール名 | 説明 | 詳細リンク |
|------------|------|-----------|
| 📞 **useronlie** | ユーザー電話照会サービス | [詳細を見る](./useronlie/README.md) |
| 📚 **xmol** | 文献検索と質問応答システム | [詳細を見る](./xmol/README.md) |

## 🛠️ 技術スタック

- **Python 3.11+**：コア開発言語
- **FastMCP**：MCPプロトコル実装フレームワーク
- **通信プロトコル**：HTTP/SSEとSTDIOの両方の転送方式をサポート

## ⚙️ 一般的な開発ガイド

### 環境のセットアップ

```bash
# Python 3.11+がインストールされていることを確認
python --version

# MCPフレームワークをインストール
pip install "mcp[cli]>=1.6.0"

# 依存関係管理ツールとしてuvを推奨
pip install uv
```

### モジュール構造の標準

各新モジュールは以下の基本構造に従うべきです：

```
module_name/
├── core/               # コア機能の実装
│   ├── __init__.py
│   ├── server.py       # MCPサーバー実装
│   └── ...             # その他の機能モジュール
├── README.md           # モジュールの詳細ドキュメント
├── run.py              # 起動スクリプト
├── pyproject.toml      # プロジェクト設定
└── ...                 # その他の設定ファイル
```

### 新しいモジュールを開発するステップ

1. **モジュールディレクトリ構造の作成**
   ```bash
   mkdir -p new_module/core
   touch new_module/{README.md,run.py,pyproject.toml}
   touch new_module/core/{__init__.py,server.py}
   ```

2. **MCPサーバーの実装**
   ```python
   # new_module/core/server.py (基本フレームワーク)
   from fastmcp import McpServer, Tool, Resource

   class NewModuleServer(McpServer):
       def __init__(self):
           super().__init__("新モジュール名")
           # ツールとリソースの登録
           self.register_tool(Tool("ツール名", self.tool_handler))
           self.register_resource("resource://path", self.resource_handler)
   
       async def tool_handler(self, params):
           # ツールロジックの実装
           return {"result": "ツール実行結果"}
   
       async def resource_handler(self, params):
           # リソースアクセスロジックの実装
           return {"data": "リソース内容"}
   ```

3. **起動スクリプトの作成**
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

4. **プロジェクト依存関係の設定**
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

5. **モジュールREADMEの作成**
   各モジュールは独自のREADMEファイルを持ち、機能、設定、使用方法を詳細に説明する必要があります。

## 🚀 汎用実行方法

すべてのモジュールは2つの実行モードをサポートしています：

```bash
# STDIOモード（Claude Desktopとの直接統合に適しています）
cd <module_name>
python run.py

# SSEモード（HTTPサービスとして実行）
cd <module_name>
python run.py --transport sse --host 127.0.0.1 --port 8000
```

## 🏗️ Claudeとの統合

1. Claude Desktopの設定（`%AppData%\Claude\claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "<サービス名>": {
      "isActive": true,
      "name": "<表示名>",
      "url": "http://localhost:<ポート>/sse"
    }
  }
}
```

2. 設定を適用するためにClaude Desktopアプリケーションを再起動します

## 🔧 拡張可能なエコシステム

MCPALLは無限に拡張可能なサービスエコシステムとして設計されています。以下はいくつかの潜在的な拡張方向です：

- **データ処理サービス**：データ分析、視覚化、レポート生成
- **AIアシスタントツール**：テキスト生成、画像処理、音声認識
- **開発ツールチェーン**：コード生成、プロジェクト管理、テスト自動化
- **知識ベースサービス**：ドキュメント検索、ナレッジグラフ、Q&Aシステム
- **運用監視**：システム状態、パフォーマンス監視、ログ分析

MCPALLプラットフォームにサービスを追加するには、上記の開発標準に従い、モジュールディレクトリをプロジェクトのルートに追加するだけです。

## 📋 MCPサービス開発の核心概念

### ツール (Tools)

ツールはMCPサービスが提供する特定のタスクを実行するための呼び出し可能な関数です。

```python
# ツール定義の例
@server.tool("ツール名")
async def tool_handler(params):
    # パラメータ処理とビジネスロジック
    return {"result": "処理結果"}
```

### リソース (Resources)

リソースはMCPサービスが提供するデータアクセスポイントで、URIによって識別されます。

```python
# リソース定義の例
@server.resource("resource://path")
async def resource_handler(params):
    # リソースアクセスロジック
    return {"data": "リソース内容"}
```

### リソーススキーマ (Schema)

スキーマ定義を通じて、リソースの構造と検証ルールを宣言できます。

```python
# リソーススキーマの例
resource_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "data": {"type": "array", "items": {"type": "string"}}
    }
}
```

詳細な開発情報については、[MCP開発ドキュメント](https://github.com/anthropics/anthropic-cookbook/tree/main/mcp)を参照してください。

## 📄 ライセンス

MIT

## 👥 貢献ガイドライン

1. プロジェクトリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📮 連絡先

- プロジェクトメンテナ：[あなたの名前](mailto:your-email@example.com)
- プロジェクトリポジトリ：[GitHub](https://github.com/your-username/mcpall) 