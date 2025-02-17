#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages, Command
import pymarp_binary  # __version__などを取得

class DownloadMarpCommand(Command):
    """
    "python setup_binary.py download_marp" で Marp CLI をダウンロード・展開。
    """
    description = "Download and unpack Marp CLI"
    user_options = []

    def initialize_options(self):
        self.run_command("download_marp")
        pass

    def finalize_options(self):
        self.run_command("download_marp")
        pass

    def run(self):
        from pymarp_binary.marp_download import download_marp
        target_dir = os.path.join(os.path.dirname(__file__), "pymarp_binary", "files")
        download_marp(target_folder=target_dir, delete_installer=False)

setup(
    name="pymarp_binary",
    version=pymarp_binary.__version__,
    description="Marp CLI with binary included (local example)",
    packages=find_packages(),
    package_data={
        "pymarp_binary": ["files/*", "files/bin/*"]
    },
    cmdclass={
        "download_marp": DownloadMarpCommand
    },
    python_requires=">=3.7",
    # 必要なら classifiers や author, license などを追加
)
