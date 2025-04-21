<?php

header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

// version.jsonのファイルパス
$filePath = 'version.json';

// ファイルが存在するかチェック
if (file_exists($filePath)) {
    // JSONファイルを読み込み
    $jsonContent = file_get_contents($filePath);

    // JSONを配列にデコード
    $data = json_decode($jsonContent, true);

    // 'version'キーが存在するか確認
    if (isset($data['version'])) {
        // versionを返す
        $ver = $data['version'];
    } else {
        $ver = "";
    }
} else {
    echo 'version.jsonファイルが見つかりません';
}

$host = "localhost";
$user = "root";
$password = "toki180918";
$database = "transcribe";

$conn = new mysqli($host, $user, $password, $database);
if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(["error" => "DB接続エラー: " . $conn->connect_error]);
    exit;
}

// URLパラメータ取得
$from = isset($_GET['from']) ? $_GET['from'] : null;
$to = isset($_GET['to']) ? $_GET['to'] : null;

// ベースSQL
$sql = "SELECT id, start_time, end_time, text, created_at FROM transcriptions";

// 時間指定があればWHERE句追加
$conditions = [];
$params = [];

if ($from !== null) {
    $conditions[] = "start_time >= ?";
    $params[] = $from;
}
if ($to !== null) {
    $conditions[] = "end_time <= ?";
    $params[] = $to;
}

if (!empty($conditions)) {
    $sql .= " WHERE " . implode(" AND ", $conditions);
}

$sql .= " ORDER BY created_at DESC";

// プリペアドステートメントで安全に処理
$stmt = $conn->prepare($sql);

// パラメータがある場合にバインド
if (!empty($params)) {
    $types = str_repeat("s", count($params)); // 全て文字列として扱う
    $stmt->bind_param($types, ...$params);
}

$data = [];
if ($stmt->execute()) {
    $result = $stmt->get_result();
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    echo json_encode(
        [
            "transcribe" => $data,
            "version" => $ver
        ], 
        JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT
    );
} else {
    http_response_code(500);
    echo json_encode(["error" => "クエリ失敗: " . $stmt->error]);
}

$stmt->close();
$conn->close();
