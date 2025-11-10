import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const VoteApp());
}

class VoteApp extends StatelessWidget {
  const VoteApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '投票アプリ',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const VotePage(),
    );
  }
}

class VotePage extends StatefulWidget {
  const VotePage({super.key});

  @override
  State<VotePage> createState() => _VotePageState();
}

class _VotePageState extends State<VotePage> {
  String selectedOption = "A";
  String message = "";

  Future<void> submitVote() async {
    final url = Uri.parse('http://localhost:8000/vote');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'option': selectedOption}),
      );

      if (response.statusCode == 200) {
        setState(() {
          message = "投票が完了しました！";
        });
      } else {
        setState(() {
          message = "エラー: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        message = "サーバーに接続できませんでした: $e";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("投票アプリ")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text("どちらに投票しますか？"),
            RadioListTile<String>(
              title: const Text("選択肢A"),
              value: "A",
              groupValue: selectedOption,
              onChanged: (value) {
                setState(() {
                  selectedOption = value!;
                });
              },
            ),
            RadioListTile<String>(
              title: const Text("選択肢B"),
              value: "B",
              groupValue: selectedOption,
              onChanged: (value) {
                setState(() {
                  selectedOption = value!;
                });
              },
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: submitVote,
              child: const Text("投票する"),
            ),
            const SizedBox(height: 20),
            Text(message),
          ],
        ),
      ),
    );
  }
}
