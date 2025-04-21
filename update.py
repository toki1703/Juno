from datetime import datetime
import json

def update_version(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    current_version = None
    current_time = None
    version_line = None
    time_line = None
    css_line = None
    for line in content.splitlines():
        if 'meta name="data-app-version"' in line:
            version_line = line
            current_version = line.split('content="')[1].split('"')[0]
        if 'meta name="data-app-time"' in line:
            time_line = line
            current_time = line.split('content="')[1].split('"')[0]
        if 'link rel="stylesheet" href="style.css?' in line:
            css_line = line
        if current_version and current_time and css_line:
        # if current_version and current_time:
            break

    if not current_version:
        raise ValueError("Current version not found in the file.")
    if not current_time:
        raise ValueError("Current time not found in the file.")
    # if not css_line:
        # raise ValueError("CSS version not found in the file.")

    # Extract the date and increment part from the current version
    current_date_str, current_increment = current_version.rsplit('.', 1)
    current_date = datetime.strptime(current_date_str, '%y.%m.%d')
    current_increment = int(current_increment)

    # Get today's date
    today = datetime.today()

    if today.date() == current_date.date():
        # If the date is the same, increment the version number
        new_increment = current_increment + 1
    else:
        # If the date is different, reset the increment
        new_increment = 0

    # Create the new version string
    new_version = f"{today.strftime('%y.%m.%d')}.{new_increment}"
    new_time = today.strftime('%Y/%m/%d %H:%M:%S')

    new_content = content.replace(current_version, new_version).replace(current_time, new_time)

    # Write the new content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    version_json_path = '/var/www/html/voice/version.json'
    with open(version_json_path, 'r', encoding='utf-8') as file:
        version_data = json.load(file)

    # Update the version in the version.json file
    version_data['version'] = new_version
    version_data['time'] = new_time

    # Write the new version back to the version.json file
    with open(version_json_path, 'w', encoding='utf-8') as file:
        json.dump(version_data, file, ensure_ascii=False, indent=4)

    print(f"Updated version from {current_version} to {new_version}")

# 使用例
# 変更点：ファイルパスの修正
update_version('/var/www/html/voice/index.html')
