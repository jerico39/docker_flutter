import 'dart:io';
import 'package:flutter/foundation.dart';

class AppConfig {
  static String get apiBaseUrl {
    // Web の場合
    if (kIsWeb) {
      return "http://localhost:8000";
    }

    // Android エミュレーター
    if (Platform.isAndroid) {
      return "http://10.0.2.2:8000";
    }

    // iOS シミュレーター
    if (Platform.isIOS) {
      return "http://localhost:8000";
    }

    // デスクトップ
    return "http://localhost:8000";
  }

  static String get vote => "$apiBaseUrl/vote";
}
