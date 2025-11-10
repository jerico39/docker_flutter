# Flutter SDK 付き Ubuntu ベース
FROM ubuntu:22.04

# 環境変数
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="$PATH:/flutter/bin"

# 必要パッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    android-tools-adb \
    sudo \
    bash-completion \
    && rm -rf /var/lib/apt/lists/*

# Flutter SDK をインストール
RUN git clone https://github.com/flutter/flutter.git /flutter
ENV PATH="/flutter/bin:/flutter/bin/cache/dart-sdk/bin:$PATH"

# 作業ディレクトリ
WORKDIR /app

# 権限設定（非rootユーザーを作る場合）
RUN useradd -ms /bin/bash developer && echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER developer
