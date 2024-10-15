#!/bin/bash

#スクリプト内でのみプロキシ設定を外す
export http_proxy=""
export https_proxy=""

# コマンドをここに記述
python3.9 /usr/local/tri/src/main.py
