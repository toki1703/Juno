from PIL import Image
import os

# 元画像のパス
source_image_path = "/var/www/html/voice/background.jpg"
# 出力フォルダ
output_folder = "/var/www/html/voice/icons"

# 作成するアイコンサイズのリスト
sizes = [
    (48, 48),
    (72, 72),
    (96, 96),
    (128, 128),
    (144, 144),
    (192, 192),
    (256, 256),
    (384, 384),
    (512, 512)
]

# 出力フォルダを作成
os.makedirs(output_folder, exist_ok=True)

# 元画像を開く
try:
    img = Image.open(source_image_path)
    for size in sizes:
        # リサイズ
        img_resize = img.resize(size)
        # 出力ファイル名
        output_path = os.path.join(output_folder, f"icon-{size[0]}x{size[1]}.png")
        # 保存
        img_resize.save(output_path, format="PNG")
        print(f"Saved: {output_path}")
except FileNotFoundError:
    print(f"Error: Source image '{source_image_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
