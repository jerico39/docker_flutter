# ベースイメージ: Flutter公式（CirrusLabs）
FROM ghcr.io/cirruslabs/flutter:stable

# システムアップデートと必要なツールのインストール
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    xz-utils \
    zip \
    libglu1-mesa \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Flutterのキャッシュをあらかじめ取得
RUN flutter doctor -v

# 作業ディレクトリ設定
WORKDIR /app

# Flutterのパスを環境変数に設定
ENV PATH="$PATH:/flutter/bin"

# デフォルトコマンド
CMD ["bash"]
