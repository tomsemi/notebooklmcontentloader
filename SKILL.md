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

## 📋 触发条件 (Triggers)

当用户有以下意图时使用此 Skill：

*   "把这个链接传上去"
*   "读一下这几篇论文"
*   "把这个文件夹里的文档都分析一下"
*   "下载这本书并上传"

## 🔧 使用案例 (Examples)

### 1. 导入网页链接 (URLs)

用户："分析这篇博客"

```bash
# 直接传链接
python3 content_loader/scripts/loader.py "https://example.com/blog-post"
```

### 2. 导入可下载文件 (Files via URL)

用户："把这篇 Arxiv 论文传上去"

```bash
# 脚本会自动识别 .pdf 后缀并先下载
python3 content_loader/scripts/loader.py "https://arxiv.org/pdf/2301.1234.pdf"

# 如果后缀不明显，可强制开启下载模式
python3 content_loader/scripts/loader.py "https://example.com/download?id=123" --download
```

### 3. 导入本地资源 (Local)

用户："把桌面上这堆资料传上去"

```bash
# 单个文件
python3 content_loader/scripts/loader.py "/Users/ge/Desktop/paper.pdf"

# 整个文件夹 (批量上传)
python3 content_loader/scripts/loader.py "/Users/ge/Documents/Research_Project/"
```

### 4. 混合指令 (Mixed)

用户："新建一个笔记本，把这个网页和那个文件放进去"

```bash
python3 content_loader/scripts/loader.py \
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
