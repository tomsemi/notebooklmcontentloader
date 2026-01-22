# NotebookLM Universal Loader

[English](#english) | [中文](#chinese)

<a name="english"></a>
## 🇬🇧 English

**NotebookLM Universal Loader** is a powerful, unified tool designed to effortlessly feed content into Google's NotebookLM. Whether you have URLs, local files, or resources from specific shadow libraries, this tool handles it all.

### 🎯 Key Features

1.  **Universal Input**:
    *   **URL Direct**: Add web links directly (using NotebookLM's native scraping).
    *   **Smart Download**: Automatically detects PDF/EPUB/DOC links, downloads them, and uploads.
    *   **Local Files**: Upload individual files from your computer.
    *   **Directory Scanning**: Recursively scan folders and batch upload all documents.
    
2.  **Specialized Integrations**:
    *   **Anna's Archive**: Full support for `annas-archive.li`. Just paste a detail page URL or even a `/slow_download/` countdown page. The script automatically handles the wait time for you.
    *   **Z-Library**: Supports `z-lib.do` / `singlelogin`. Handles auto-login (via config), supports both new and old download interfaces, and prioritizes PDF over EPUB.

3.  **Format Intelligence**:
    *   **Zero-Dependency EPUB Conversion**: Built-in raw Python EPUB parser. It unzips and sanitizes EPUBs into clean text for optimal RAG (Retrieval-Augmented Generation) performance, handling compatibility issues automatically.
    *   **Large File Splitting**: Automatically splits files that exceed NotebookLM's token limits into smaller chunks.

### 🚀 Usage

Run the loader script with one or more inputs.

#### Basic Usage
```bash
# Upload a URL
python3 scripts/loader.py "https://example.com/some-article"

# Upload a local file
python3 scripts/loader.py "/Users/me/Documents/paper.pdf"

# Upload an entire folder
python3 scripts/loader.py "/Users/me/Documents/Research"
```

#### Specialized Sources
```bash
# Anna's Archive (Auto-wait for countdowns)
python3 scripts/loader.py "https://annas-archive.li/slow_download/..."

# Z-Library
python3 scripts/loader.py "https://z-library.se/book/..."
```

#### Advanced
```bash
# Mix inputs and specify a target notebook name
python3 scripts/loader.py \
    "https://example.com/article" \
    "/Users/me/local_note.txt" \
    --notebook "My New Project"
```

### 📋 Prerequisites / 依赖要求

**Critical**: This tool relies on the `notebooklm-py` library. You must install it first.
**核心依赖**：本工具依赖 `notebooklm-py` 库，请务必先安装。

```bash
pip install notebooklm-py
# OR / 或者
pip install git+https://github.com/teng-lin/notebooklm-py.git
```

After installation, verify it works: / 安装后请验证：
```bash
notebooklm --version
notebooklm auth login  # Log in to your Google Account / 登录谷歌账号
```

*   Python 3+


---

<a name="chinese"></a>
## 🇨🇳 中文

**NotebookLM Universal Loader** 是一个纯粹、高效的资源加载工具，旨在帮助你将各种来源的内容“投喂”给 NotebookLM。无论是网页链接、本地文件，还是特定电子书库的资源，它都能一键处理。

### 🎯 核心功能

1.  **全能输入支持**：
    *   **URL 直传**：直接将网页链接添加到 NotebookLM（使用 NotebookLM 原生抓取）。
    *   **智能下载**：自动识别 PDF/EPUB/DOC 链接，下载到本地后上传。
    *   **本地文件**：支持上传单个文件。
    *   **目录扫描**：递归扫描文件夹，批量上传所有文档。

2.  **深度集成 (Specialized Integrations)**：
    *   **Anna's Archive**：完美支持 `annas-archive.li`。可以直接粘贴详情页链接，甚至支持 `/slow_download/` 等倒计时下载页，脚本会自动等待倒计时结束并下载。
    *   **Z-Library**：支持 `z-lib.do` / `singlelogin`。读取配置自动登录，支持新旧两种下载界面，并优先下载 PDF 格式。

3.  **格式处理黑科技**：
    *   **EPUB 零依赖转换**：内置纯 Python 实现的 EPUB 解析器。自动解压并清洗 HTML 标签，提取纯文本上传，从根本上解决兼容性问题。
    *   **智能分割**：针对超过 NotebookLM Token 限制的大文件，自动拆分成多个部分上传。

### 🚀 使用指南

#### 基础用法
```bash
# 导入网页
python3 scripts/loader.py "https://example.com/some-article"

# 导入本地文件
python3 scripts/loader.py "/Users/me/Documents/paper.pdf"

# 批量导入文件夹
python3 scripts/loader.py "/Users/me/Documents/Research"
```

#### 电子书库专用
```bash
# Anna's Archive (支持自动等待倒计时)
python3 scripts/loader.py "https://annas-archive.li/slow_download/..."

# Z-Library
python3 scripts/loader.py "https://z-library.se/book/..."
```

#### 混合指令
```bash
# 混合多种来源并指定笔记本名称
python3 scripts/loader.py \
    "https://example.com/article" \
    "/Users/me/local_note.txt" \
    --notebook "我的研究项目"
```

### 📋 依赖要求
*   Python 3+
*   已安装并登录 `notebooklm` CLI 工具。
