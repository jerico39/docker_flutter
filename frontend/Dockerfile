# ベースイメージ: Flutter 3.24.3 + Linux
FROM ghcr.io/cirruslabs/flutter:3.24.3

# 作業ディレクトリ
WORKDIR /app

# Flutter Web と Android 対応
RUN flutter config --enable-web
RUN flutter doctor

# Android SDK の PATH
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools

# Android SDK Command line tools のインストール
RUN apt-get update && apt-get install -y unzip wget openjdk-17-jdk git curl && rm -rf /var/lib/apt/lists/*
RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip \
    && unzip cmdline-tools.zip -d $ANDROID_SDK_ROOT/cmdline-tools \
    && rm cmdline-tools.zip

# ライセンス同意 & 必要ツール
RUN yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT --licenses
RUN sdkmanager --sdk_root=$ANDROID_SDK_ROOT "platform-tools" "platforms;android-34" "build-tools;34.0.0"

# ソースコードコピー
COPY . .

# pub get
RUN flutter pub get

# ポート公開（Web 用）
EXPOSE 8080

# デフォルトコマンドは Bash（Web や Android ビルドで自由に使える）
CMD ["bash"]
