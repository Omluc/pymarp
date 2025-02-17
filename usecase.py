#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymarp_binary

def main():
    input_md = "slides.md"
    output_pdf = "slides.pdf"
    # marp CLIの追加オプション
    extra_args = ["--pdf", "--allow-local-files"]

    print("Converting markdown -> PDF using pymarp_binary ...")
    pymarp_binary.convert_file(input_md, output_pdf, extra_args)
    print(f"Done: {output_pdf}")

if __name__ == "__main__":
    main()
