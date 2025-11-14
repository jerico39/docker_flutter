import 'package:http/http.dart' as http;
import '../config/app_config.dart';

class ApiService {
  static Future<void> vote(String option) async {
    try {
      final response = await http.post(
        Uri.parse(AppConfig.vote),
        body: {"option": option},
      );

      if (response.statusCode != 200) {
        throw Exception("Vote failed: ${response.statusCode}");
      }
    } catch (e) {
      rethrow;
    }
  }
}
