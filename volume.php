<?php
$output = shell_exec("sox -t alsa default -n trim 0 0.1 stat 2>&1");

// RMS amplitude の値を抽出するために正規表現を修正
if (preg_match('/RMS\s+amplitude\s*:\s*([\d.]+)/', $output, $matches)) {
    $rms = $matches[1];
    $volume = $rms * 100;
    echo "現在のマイク音量: $volume ％";
    echo "<br>";
    if ($rms >= 0.01) {
        echo "録音される";
    } else {
        echo "録音されない";
    }
    
} else {
    echo "RMS amplitudeが見つかりませんでした。\n";
    echo $output;
}
?>
