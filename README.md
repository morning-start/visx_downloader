# Visx Downloader

## 简介

这是一个简单的Python脚本，用于从官方网站下载VSCode扩展的Visx文件。你可以使用该脚本指定扩展的ID，选择下载特定版本或获取最新版本的扩展，并将其保存到指定的目标文件夹中。

## 功能特性

1. **下载VSCode扩展**：根据提供的扩展ID从Visual Studio Marketplace下载相应的扩展文件。
2. **版本选择**：可以指定下载特定版本的扩展，如果不指定版本，则自动下载最新版本。
3. **文件大小显示**：在下载过程中显示文件的大小，以KB或MB为单位。
4. **进度条显示**：使用`tqdm`库显示下载进度条，让用户清楚了解下载状态。
5. **删除旧插件**：新增功能，默认情况下会删除该扩展ID相关的旧插件文件。

## 安装与依赖

1. **Python环境**：确保你已经安装了Python 3.x版本。
2. **依赖库安装**：运行脚本前，需要安装以下依赖库：
    - `typer`：用于解析命令行参数。
    - `json`：Python内置库，用于处理JSON数据。
    - `pathlib`：Python内置库，用于处理文件路径。
    - `os`：Python内置库，用于与操作系统交互。
    - `requests`：用于发送HTTP请求。
    - `tqdm`：用于显示进度条。

你可以使用以下命令安装依赖库：

```bash
uv sync
```

## 使用方法

### 使用可执行文件（exe）

```ps1
visx.exe <ext_id> # 下载最新版本的扩展
visx.exe -h # 显示帮助信息
```

### 使用Python脚本

1. **克隆或下载代码仓库**：将本项目的代码下载到本地。
2. **进入项目目录**：使用命令行进入项目所在的目录。

    ```bash
    cd visx_downloader
    ```

3. **同步环境（可选）**：如果项目有特定的环境同步需求，可以运行`uv sync`命令（根据实际情况可能不需要此步骤）。
4. **下载扩展**：

```bash
uv run main.py <ext_id> # 下载最新版本的扩展
uv run main.py <ext_id> --version <version_number> --destination <target_folder> # 下载指定版本的扩展到指定文件夹
uv run main.py -h # 显示帮助信息
```

其中，`<ext_id>`是VSCode扩展的唯一标识符，格式为`publisher.name`（例如`ms-python.python`）；`<version_number>`是你想要下载的特定版本号；`<target_folder>`是保存扩展文件的目标文件夹路径。

## 命令行参数说明

- `ext_id`（必需）：扩展的ID（例如`publisher.name`），这是VSCode扩展的唯一标识符。
- `-v`或`--version`（可选）：扩展的特定版本。如果未指定，将下载最新版本。
- `-d`或`--destination`（可选）：扩展将保存到的目标文件夹。默认值会参考环境变量`VSEXTP_DOWNLOAD_PATH`。若设置了该环境变量，会使用其值作为默认保存路径；若未设置，则默认保存到`./extensions`目录。

### 环境变量 `VSEXTP_DOWNLOAD_PATH` 说明

`VSEXTP_DOWNLOAD_PATH` 是一个可选的环境变量，用于指定VSCode扩展文件的默认下载路径。当你在命令行中未使用 `-d` 或 `--destination` 参数指定目标文件夹时，脚本会检查该环境变量是否存在。如果存在，脚本会将扩展文件下载到该环境变量指定的路径；如果不存在，则会使用 `./extensions` 作为默认的下载路径。

你可以通过以下方式设置环境变量：

#### Windows

在命令提示符或PowerShell中使用以下命令：

```ps1
$env:VSEXTP_DOWNLOAD_PATH = "C:\path\to\your\download\folder"
```

## 示例

```bash
uv run main.py ms-python.python --version 2023.1.0 --destination ./my_extensions
```

上述命令将下载`ms-python.python`扩展的`2023.1.0`版本，并将其保存到`./my_extensions`文件夹中。

## 错误处理

1. 如果下载过程中出现错误，脚本将打印错误信息，并尝试删除已下载的文件（如果已经部分下载）。
2. 如果指定的扩展文件已经存在于目标文件夹中，脚本将跳过下载并提示用户文件已存在。

## 贡献与反馈

如果你在使用过程中发现任何问题，或者有改进建议，欢迎提交问题或Pull Request。你也可以通过项目的讨论区分享你的使用经验和反馈。
