import subprocess
from pathlib import Path


def write_version_file(version, author, app_name):
    """
    根据模板配置写入 version_file.txt

    :param version: 版本号
    :param author: 作者或公司名称
    :param app_name: 应用名称
    """
    VERSION = version
    AUTHOR = author
    APP_NAME = app_name

    metadata = {
        "FILE_VERSION": f"({",".join(VERSION.split("."))})",  # 文件版本号
        "PRODUCT_VERSION": f"({",".join(VERSION.split("."))})",  # 产品版本
        "COMPANY_NAME": AUTHOR,  # 公司名称
        "FILE_DESCRIPTION": f"{APP_NAME} downloader",  # 文件描述
        "INTERNAL_NAME": f"{APP_NAME} downloader",  # 内部名称
        "LEGAL_COPYRIGHT": f"Copyright (C) 2023 {AUTHOR}",  # 版权信息
        "ORIGINAL_FILENAME": "visx.exe",  # 原始文件名
        "PRODUCT_NAME": APP_NAME,  # 产品名称
    }
    info = Path("./templates/version_tmp.txt").read_text(encoding="utf-8")
    info = info.format(**metadata)
    Path("./version_file.txt").write_text(info, encoding="utf-8")


AUTHOR = "MorningStart"
VERSION = "3.0.0.0"
APP_NAME = "visx"
ICON = "icon.ico"


write_version_file(VERSION, AUTHOR, APP_NAME)
# 构建 pyinstaller 命令
cmd = [
    "pyinstaller",
    "--onefile",
    f"--version-file=version_file.txt",
    f"--icon={ICON}",
    f"--name={APP_NAME}",
    "main.py",  # 假设主程序文件名为 main.py，可按需修改
]

try:
    # 执行 pyinstaller 命令
    subprocess.run(cmd, check=True)
    print("应用构建成功！")
except subprocess.CalledProcessError as e:
    print(f"应用构建失败: {e}")
