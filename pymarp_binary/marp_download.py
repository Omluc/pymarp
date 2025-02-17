import os
import sys
import stat
import shutil
import tarfile
import zipfile
import urllib.request
import platform

def download_marp(version="v4.1.1", target_folder=None, delete_installer=False):
    """
    GitHub Releases等から Marp CLI バイナリをダウンロードし、
    target_folder (デフォルトは pymarp_binary/files ) に展開。
    """
    if target_folder is None:
        # カレントからの相対パスでもよいが、安全のため絶対パス化
        base_dir = os.path.abspath(os.path.dirname(__file__))
        target_folder = os.path.join(base_dir, "files")

    os.makedirs(target_folder, exist_ok=True)
    bin_dir = os.path.join(target_folder, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    # ダウンロードするファイル名を OS で切り替える
    pf = sys.platform
    arch = platform.machine().lower()  # 'x86_64', 'arm64' etc

    # Marp CLIのReleaseページに合わせる
    if pf.startswith("win"):
        # Windows
        filename = f"marp-cli-{version}-win.zip"
        url = f"https://github.com/marp-team/marp-cli/releases/download/{version}/{filename}"
    elif pf.startswith("darwin"):
        # macOS
        filename = f"marp-cli-{version}-mac.tar.gz"
        url = f"https://github.com/marp-team/marp-cli/releases/download/{version}/{filename}"
    else:
        # Linux
        filename = f"marp-cli-{version}-linux.tar.gz"
        url = f"https://github.com/marp-team/marp-cli/releases/download/{version}/{filename}"

    installer_path = os.path.join(target_folder, filename)

    # ダウンロード
    if not os.path.exists(installer_path):
        print(f"Downloading Marp CLI from {url}")
        urllib.request.urlretrieve(url, installer_path)
    else:
        print(f"Using already downloaded file: {installer_path}")

    # 解凍
    if filename.endswith(".zip"):
        with zipfile.ZipFile(installer_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
    elif filename.endswith(".tar.gz"):
        with tarfile.open(installer_path, "r:gz") as tar_ref:
            tar_ref.extractall(target_folder)
    else:
        raise RuntimeError("Unknown file format. Expected zip or tar.gz")

    # ダウンロードしたアーカイブの中で実行ファイルがどこにあるかを特定 → bin_dir に移動
    if pf.startswith("win"):
        src_marp = os.path.join(target_folder, "marp.exe")  # .exe 決め打ちでOK
    else:
        src_marp = os.path.join(target_folder, "marp")

    dst_marp = os.path.join(bin_dir, os.path.basename(src_marp))
    if os.path.exists(src_marp):
        shutil.move(src_marp, dst_marp)

        # macOS/Linuxなら実行権限付与
        if not pf.startswith("win"):
            st = os.stat(dst_marp)
            os.chmod(dst_marp, st.st_mode | stat.S_IEXEC)
    else:
        print(f"Warning: couldn't find {src_marp}")

    if delete_installer:
        os.remove(installer_path)
