---
name: notebooklm-universal-loader
description: A unified loader to feed URLs, files, and downloaded content into NotebookLM.
---

# NotebookLM Universal Loader

一个纯粹、高效的 NotebookLM 资源加载工具。支持从 URL、本地文件或文件夹直接投喂知识。

## 🎯 核心能力

1.  **URL 直传**：直接将网页链接添加到 NotebookLM（由 NotebookLM 原生抓取）。
2.  **文件下载**：自动识别 PDF/EPUB/DOC 链接，下载到本地后上传。
3.  **本地文件**：支持单个文件上传。
4.  **目录扫描**：递归扫描文件夹，批量上传所有文档。

## 🌟 高级集成 (Specialized Integrations)

Loader 内置了对特定知识库的深度支持，能够自动处理复杂的下载流程。

### 1. Anna's Archive (`annas-archive.org` / `.li`)
*   **全自动下载**：支持直接粘贴详情页 URL。
*   **二级页面支持**：**NEW!** 直接支持粘贴 `/slow_download/` 等倒计时下载页，脚本会自动等待倒计时结束并点击下载。
*   **智能排队**：自动处理等待时间。

### 2. Z-Library (`z-lib.do` / singlelogin)
*   **自动登录**：读取本地配置进行自动登录。
*   **双模式下载**：即支持新版界面的“三点菜单”下载，也支持旧版的“转换”按钮。
*   **格式优选**：优先下载 PDF，其次下载 EPUB。

### 3. Researcher Pilot (`scripts/researcher.py`)
*   **功能**：上传并自动提问/分析。
*   **注意**：目前因 Google API 变动，`ask` (提问) 功能暂时不稳定 (Pending Fix).
*   **用法**：
    ```bash
    python3 scripts/researcher.py --notebook "Topic" --source "url" --query "Summarize this"
    ```

## 🪄 格式处理黑科技

*   **EPUB 零依赖转换**：内置纯 Python 实现的 EPUB 解析器。无需安装任何额外库，脚本会自动解压 EPUB，清洗 HTML 标签，提取纯文本上传。解决所有兼容性问题。
*   **智能分割**：如果是超大文件（超过 NotebookLM Token 限制），脚本会自动将其分割成多个部分上传。
*   **原生支持**：
    *   PDF (推荐)
    *   TXT / Markdown
    *   DOCX

## ⚙️ Execution Workflow (Agent Instructions)

This section defines the precise steps the Agent MUST follow when executing this skill.

1.  **Pre-flight Check (Dependency Verification)**:
    *   Check if `notebooklm` CLI is available: Run `notebooklm --version`.
    *   **IF** the command fails (command not found):
        *   Automatically run: `pip install notebooklm-py` (or `pip install git+https://github.com/teng-lin/notebooklm-py.git`).
        *   **CRITICAL**: Check if user is logged in by running `notebooklm auth check` (or similar). If not logged in, STOP and ask the user to run `notebooklm auth login`.
    *   **IF** `notebooklm` is available, proceed to step 2.

2.  **Input Analysis**:
    *   Identify if the input is a URL, Z-Library link, Anna's Archive link, or Local File.
    *   Construct the appropriate command based on the "Examples" section below.

3.  **Execution**:
    *   Run the `loader.py` script.
    *   Monitor the output. If the script fails due to an auth error, guide the user to re-login.


## 🔧 使用案例 (Examples)

### 1. 导入网页 (Loader)

用户："分析这篇博客"

```bash
# 直接传链接
python3 scripts/loader.py "https://example.com/blog-post"
```

### 2. 智能分析 (Researcher)
```bash
# 上传并生成简报 (Output to console & file)
python3 scripts/researcher.py \
    --notebook "News Analysis" \
    --source "https://it.sohu.com/..." \
    --query "核心观点是什么？" \
    --output "report.md"
```

### 2. 从 Anna's Archive 搬运

用户："帮我读这本书"

```bash
# 粘贴详情页
python3 scripts/loader.py "https://annas-archive.li/md5/..."

# 或者直接粘贴下载倒计时页 (无需等待倒计时结束，脚本会替你等)
python3 scripts/loader.py "https://annas-archive.li/slow_download/..."
```

### 3. 从 Z-Library 搬运

```bash
python3 scripts/loader.py "https://z-library.se/book/..."
```

### 4. 导入本地资源 (Local)

用户："把桌面上这堆资料传上去"

```bash
# 单个文件
python3 scripts/loader.py "/Users/ge/Desktop/paper.pdf"

# 整个文件夹 (批量上传)
python3 scripts/loader.py "/Users/ge/Documents/Research_Project/"
```

### 4. 混合指令 (Mixed)

用户："新建一个笔记本，把这个网页和那个文件放进去"

```bash
python3 scripts/loader.py \
    "https://example.com/article" \
    "/Users/ge/Desktop/note.txt" \
    --notebook "Project Analysis"
```

## 🛠️ 参数说明

*   `inputs`: (必填) 一个或多个 URL 或 文件路径。
*   `--notebook / -n`: (选填) 指定目标笔记本名称。
*   `--download / -d`: (选填) 强制开启下载模式（主要用于 URL 结尾不包含文件后缀的情况）。

## 依赖
*   Python 3+
*   `notebooklm` CLI (已安装并登录)
