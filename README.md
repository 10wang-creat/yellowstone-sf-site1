# 2026 黃石公園 & 舊金山家庭旅遊網站

15 天 14 夜家庭自駕遊（2026/9/26 – 10/10，4 人）的行程規劃網站。純靜態 HTML，無需建置工具，直接開啟 `index.html` 或部署到 GitHub Pages 即可。

## 架構

```
├── index.html                 首頁（行程總覽、時間軸）
├── itinerary.html             每日行程
├── accommodation.html         住宿資訊
├── budget.html                預算規劃
├── packing.html               行李清單
├── tips.html                  旅遊須知
├── health.html                長輩健康注意事項
├── yellowstone-scoring.html   黃石景點分級建議
├── map.html                   互動地圖（Google Maps）
├── assets/css/main.css        全站共用樣式（色盤、導覽列、頁首、頁尾）
└── images/                    圖片
```

## 樣式規範

全站共用樣式集中在 `assets/css/main.css`，各頁 `<style>` 只保留該頁專屬樣式。色盤為夏季冷柔色系：

| 用途 | 色碼 |
|---|---|
| 骨架（導覽列、標題、頁尾） | 藏藍 `#34435E` |
| 主色（強調、hover、徽章） | 鼠尾草綠 `#9DB6A8` |
| 次強調 | 海藍 `#6D93C8` |
| 背景 | 珍珠白 `#F0EEF3` |
| 功能色（安全／注意／警告） | `#6FA287` / `#CFA15E` / `#B85C6E` |

新增頁面時：複製任一頁的 `<head>` 連結與 `<nav>` 區塊，並在所有頁面的導覽列加上新連結。
