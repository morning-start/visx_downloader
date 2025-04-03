import argparse
import json
from pathlib import Path
import os
import requests
from tqdm import tqdm


def format_size(size_bytes):
    """Convert bytes to KB or MB based on the size."""
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} bytes"


def get_file_name(headers: str):
    return headers.split("; ")[1].split("=")[1]


def get_extension_info(ext_id: str) -> dict:
    url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    payload = json.dumps(
        {
            "filters": [{"criteria": [{"filterType": 7, "value": ext_id}]}],
            "flags": 103,
        }
    )
    headers = {
        "Accept": "application/json;api-version=6.0-preview.1",
        "User-Agent": "Apifox/1.0.0",
        "Content-Type": "application/json",
        "Host": "marketplace.visualstudio.com",
        "Connection": "keep-alive",
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()["results"][0]["extensions"][0]


def download_file(
    publisher_name: str, extension_name: str, version: str, destination: str = "./"
):
    url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher_name}/vsextensions/{extension_name}/{version}/vspackage"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        headers = dict(response.headers)
        file_name = get_file_name(headers["Content-Disposition"])
        file_size = format_size(int(headers["Content-Length"]))
        if Path(f"{destination}/{file_name}").exists():
            print(f"{file_name} already exists. Skipping download.")
            return
        print(f"Downloading {file_name} ({file_size})...")
        with open(f"{destination}/{file_name}", "wb") as file:
            total_size = int(headers.get("Content-Length", 0))
            with tqdm(
                total=total_size, unit="iB", unit_scale=True, desc=file_name, ascii=True
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    bar.update(len(chunk))
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def run(ext_id: str, version: str = None, destination: str = "./extensions"):
    Path(destination).mkdir(parents=True, exist_ok=True)
    if version is None:
        res = get_extension_info(ext_id)
        last_version = res["versions"][0]["version"]
        publisher_name = res["publisher"]["publisherName"]
        extension_name = res["extensionName"]
    else:
        publisher_name = ext_id.split(".")[0]
        extension_name = ext_id.split(".")[1]
        last_version = version
    try:
        download_file(publisher_name, extension_name, last_version, destination)
    except Exception as e:
        print(f"Error: {e}")
        # Delete downloaded file
        Path(f"{destination}/{extension_name}-{last_version}.vsix").unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download VSCode extension.",
        epilog="Example:\n"
        "  python download_extension.py ms-python.python --version 2023.1.0 --destination ./extensions\n"
        "\n"
        "Note: If no version is specified, the latest version will be downloaded.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "ext_id",
        type=str,
        help="Extension ID (e.g., publisher.name). This is the unique identifier of the VSCode extension.",
    )
    parser.add_argument(
        "-v",  # 添加简写
        "--version",
        type=str,
        help="Specific version of the extension. If not specified, the latest version will be downloaded.",
        default=None,
    )
    default_destination = os.getenv("VSEXTP_DOWNLOAD_PATH", "./extensions")
    parser.add_argument(
        "-d",  # 添加简写
        "--destination",
        type=str,
        help="Destination folder where the extension will be saved. Default is the current directory.",
        default=default_destination,
    )

    args = parser.parse_args()
    run(args.ext_id, args.version, args.destination)
