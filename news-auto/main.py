import gspread
from oauth2client.service_account import ServiceAccountCredentials
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

# === 認証設定 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "credentials.json")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope) 
client = gspread.authorize(creds)

# === スプレッドシート読み込み ===
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/10MWXeSRmXRjJirBnIjNDv2Z07KFGW3k-BrokbLY2p2A/edit")
sheet = spreadsheet.worksheet("news")
records = sheet.get_all_records()  # 辞書形式のリストで取得

# === 日付の新しい順に並べ替え ===
records.sort(
    key=lambda x: datetime.strptime(x["日付"], "%Y/%m/%d"),
    reverse=True
)

# === Jinja2テンプレート設定 ===
template_dir = os.path.join(BASE_DIR, "templates")
env = Environment(loader=FileSystemLoader(template_dir, encoding='utf-8'))

list_template = env.get_template("newslist_template.html")
detail_template = env.get_template("news_detail_template.html")

# === 出力フォルダの準備 ===
output_dir = BASE_DIR  # 例：news-autoフォルダ
article_dir = os.path.join(output_dir, "articles")
os.makedirs(article_dir, exist_ok=True)

# === 一覧ページ生成 ===
list_html = list_template.render(news_list=records)
with open(os.path.join(output_dir, "newslist.html"), "w", encoding="utf-8") as f:
    f.write(list_html)

# === 個別ページを生成（スプレッドシートのファイル名列を使用） ===
for news in records:
    filename = news.get("ファイル名")

    if not filename or not filename.endswith(".html"):
        print("[スキップ] ファイル名が不正または未入力:", news)
        continue

    detail_html = detail_template.render(news=news)
    file_path = os.path.join(article_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(detail_html)

print("[完了] newslist.html および 個別記事ページを生成しました。")
