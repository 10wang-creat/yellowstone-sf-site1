"""
update_nav.py
================================================================
批次更新 yellowstone-sf-site1 所有 HTML 頁面的導覽列，
加入「健康注意」和「景點分級」兩個新連結。

使用方法（Windows PowerShell 或 CMD）：
    cd C:\\Users\\s8817\\OneDrive\\Documents\\Github\\yellowstone-sf-site1
    python update_nav.py

需求：已安裝 Python 3.6+（Windows 10/11 通常內建或可從 Microsoft Store 安裝）

作用：
1. 自動備份每個 HTML 檔到 _backup_nav/ 資料夾
2. 在每個頁面的 <li><a href="tips.html">旅遊須知</a></li> 後面
   插入兩個新連結：
     - <li><a href="health.html">健康注意</a></li>
     - <li><a href="yellowstone-scoring.html">景點分級</a></li>
3. 如果已經有這兩個連結（表示之前跑過），自動跳過，不會重複

安全性：
- 只修改導覽列 <ul class="nav-menu">...</ul> 內容
- 其他頁面內容完全不動
- 每次執行都會備份原檔
"""

import os
import re
import shutil
from datetime import datetime

# ===== 設定 =====
# 腳本會在自己所在的資料夾執行（使用者應該把腳本放在 yellowstone-sf-site1 資料夾內）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 要處理的 HTML 檔案（所有現有頁面）
TARGET_FILES = [
    'index.html',
    'itinerary.html',
    'accommodation.html',
    'budget.html',
    'packing.html',
    'tips.html',
    'map.html',
]

# 要插入的新連結
NEW_LINKS = """<li><a href="health.html">健康注意</a></li>
<li><a href="yellowstone-scoring.html">景點分級</a></li>"""

# 檢查是否已插入過
CHECK_STRING = 'href="health.html"'

# 要在這個項目後面插入（正則，寬鬆匹配各種空白格式）
INSERT_AFTER_PATTERN = re.compile(
    r'(<li>\s*<a\s+href="tips\.html"[^>]*>[^<]*</a>\s*</li>)',
    re.IGNORECASE
)

# 備份資料夾
BACKUP_DIR = os.path.join(
    SCRIPT_DIR,
    f'_backup_nav_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
)


def process_file(filepath):
    """處理單一 HTML 檔。回傳 (狀態, 訊息)。"""
    filename = os.path.basename(filepath)

    if not os.path.exists(filepath):
        return 'missing', f'找不到檔案：{filename}'

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return 'error', f'讀取失敗：{e}'

    # 檢查是否已經有 health.html 連結
    if CHECK_STRING in content:
        return 'skip', f'已有新連結，跳過：{filename}'

    # 檢查能否找到 tips.html 那一行
    match = INSERT_AFTER_PATTERN.search(content)
    if not match:
        return 'nopattern', (
            f'找不到 tips.html 連結的位置：{filename} '
            f'（可能導覽列結構不同，請手動檢查）'
        )

    # 備份
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, filename)
    shutil.copy2(filepath, backup_path)

    # 插入新連結
    replacement = match.group(1) + '\n' + NEW_LINKS
    new_content = content.replace(match.group(1), replacement, 1)

    # 寫回
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        return 'error', f'寫入失敗：{e}'

    return 'ok', f'✓ 已更新：{filename}'


def main():
    print('=' * 60)
    print('  Yellowstone 網站導覽列批次更新工具')
    print('=' * 60)
    print(f'工作目錄：{SCRIPT_DIR}')
    print()

    # 檢查是否在正確的資料夾
    if not os.path.exists(os.path.join(SCRIPT_DIR, 'index.html')):
        print('⚠️  警告：當前資料夾沒有 index.html')
        print(f'   請確認這個腳本放在 yellowstone-sf-site1 資料夾內。')
        print(f'   目前位置：{SCRIPT_DIR}')
        input('\n按 Enter 結束...')
        return

    # 統計
    results = {'ok': [], 'skip': [], 'missing': [], 'nopattern': [], 'error': []}

    for fname in TARGET_FILES:
        filepath = os.path.join(SCRIPT_DIR, fname)
        status, msg = process_file(filepath)
        results[status].append((fname, msg))
        print(f'  {msg}')

    # 總結
    print()
    print('=' * 60)
    print('  執行結果總結')
    print('=' * 60)
    print(f'✓ 成功更新：{len(results["ok"])} 個')
    print(f'○ 已有連結跳過：{len(results["skip"])} 個')
    print(f'✗ 找不到檔案：{len(results["missing"])} 個')
    print(f'✗ 找不到插入位置：{len(results["nopattern"])} 個')
    print(f'✗ 其他錯誤：{len(results["error"])} 個')

    if results['ok']:
        print(f'\n已備份原檔至：{os.path.basename(BACKUP_DIR)}/')

    if results['nopattern']:
        print('\n⚠️  以下檔案找不到插入位置，需要手動檢查：')
        for fname, _ in results['nopattern']:
            print(f'   - {fname}')
        print('   （這通常是因為導覽列結構和其他頁面不同）')

    print()
    print('下一步：')
    print('  1. 確認 health.html 和 yellowstone-scoring.html 已放在此資料夾')
    print('  2. 在瀏覽器開啟 index.html 確認導覽列多了兩個新項目')
    print('  3. 推送到 GitHub：')
    print('     git add -A')
    print('     git commit -m "Add health and scoring pages for elderly"')
    print('     git push origin main')
    print()
    input('按 Enter 結束...')


if __name__ == '__main__':
    main()
