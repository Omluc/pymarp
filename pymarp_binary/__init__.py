import os
import sys
import subprocess

__version__ = "0.1.0"

def get_marp_path():
    """
    バイナリ同梱された marp 実行ファイルのパスを返す。
    OSに合わせたファイル名を指定。
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    bin_dir = os.path.join(base_dir, "files", "bin")  # 解凍先フォルダに合わせる
    if sys.platform.startswith("win"):
        # Windowsの場合: marp.exe か marp.cmd
        return os.path.join(bin_dir, "marp.cmd")
    else:
        # macOS/Linuxの場合: 実行権限付き 'marp'
        return os.path.join(bin_dir, "marp")

def convert_file(input_file, output_file=None, extra_args=None):
    """
    同梱バイナリの marp CLI を呼び出す簡易ラッパ。
    ex) convert_file("slides.md", "slides.pdf", ["--pdf"])
    """
    if extra_args is None:
        extra_args = []

    marp_exe = get_marp_path()
    cmd = [marp_exe, input_file] + extra_args
    if output_file:
        cmd += ["-o", output_file]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Marp CLI failed with exit code {e.returncode}: {e}")

    return output_file
