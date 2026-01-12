# Bilibili Dynamics Auto-Deleter (Edge Version)

一个基于 Python Selenium 的自动化脚本，专为 Microsoft Edge 浏览器设计，用于批量删除 Bilibili 个人空间的动态。

## ⚠️ 免责声明 

* **风险提示**：本脚本仅供学习交流和个人使用。批量删除动态属于高频操作，可能会触发 B 站的风控机制（如暂时限制动态操作）。
* **责任声明**：作者不对使用本脚本导致的任何账号异常、数据丢失或封禁负责。请在运行脚本前自行评估风险。

## ✨ 功能特点

* **完全自动化**：模拟人工操作流程（点击菜单 -> 点击删除 -> 点击确认）。
* **Edge 浏览器支持**：专为 Microsoft Edge 优化，无需安装 Chrome。
* **智能翻页加载**：脚本会自动检测当前页面是否删除完毕，并尝试向下滚动加载更多动态，支持无限滚动列表。
* **防风控机制**：内置随机等待时间，模拟真实人类的操作间隔，降低被检测风险。
* **断点续删**：如果脚本意外停止，重新运行即可接着删除。

## 🛠️ 环境准备

在运行脚本之前，请确保您的电脑满足以下条件：

1. **Python 3.x**：已安装 Python 环境。
2. **Microsoft Edge 浏览器**：建议更新至最新版本。
3. **Edge WebDriver (`msedgedriver.exe`)**：
    * **第一步**：打开 Edge 浏览器，访问 `edge://settings/help` 查看当前版本号（例如 `143.0.xxxx.xx`）。
    * **第二步**：前往 [Microsoft Edge WebDriver 下载页面](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)。
    * **第三步**：下载与您浏览器版本**完全一致**的 x64 版本驱动。
    * **第四步**：解压下载的文件，将 `msedgedriver.exe` **放置在与本脚本 (`.py` 文件) 相同的文件夹中**。

## 📦 安装依赖

打开终端 (CMD 或 PowerShell)，运行以下命令安装 Selenium 库：

```bash
pip install selenium
```


