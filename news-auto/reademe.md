つるつるズ公式サイト NEWS自動生成システム

東京都立墨田川高校吹奏楽部OB・OGによる団体「つるつるズ」のホームページ内に掲載されるNEWS記事を、簡単に更新できるようにするための自動生成システムです。


【概要】
Googleスプレッドシートに入力された記事情報をもとに、以下のHTMLを自動生成します。
newslist.html（一覧ページ）
articles/YYYYMMDDN.html（個別記事ページ）


【ディレクトリ構成】
project-root/
├── index.html
├── about.html
├── member.html
├── schedule.html
├── CSS/
│   ├── stylesheet.css
│   ├── headfoot.css
│   └── article.css
│   └── newslist.css
├── images/
│   └── （ロゴなど）
├── news-auto/
│   ├── main.py
│   ├── templates/
│   │   ├── newslist_template.html
│   │   └── news_detail_template.html
│   ├── credentials.json
│   └── articles/ ← 生成された個別記事HTMLが入る
|   |__ newslist.html ← 生成された一覧ページ
├── run.bat
└── README.md



【スプレッドシートの列構成】
| タイトル | 日付 | 内容 | 画像URL | 関連リンク | ファイル名 |

・ファイル名列は YYMMDDN.html 形式
・Excel関数で自動生成する例：
=TEXT(B2, "yyMMdd") & COUNTIF($B$2:B2, B2) & ".html"


【使い方】
Google Cloud Consoleでサービスアカウントを作成し、credentials.jsonを取得
スプレッドシートにAPIの読み取り権限を付与
news-autoフォルダに credentials.json を設置
ターミナルで以下を実行：

cd news-auto
python main.py

newslist.html と、各記事のHTMLが articles/ に出力される


【補足】
・index.htmlからのトップニュースリンクは、スプレッドシートで管理するファイル名をもとに手動で貼る
・相対パスで記述しておくと file:// でも localhost でも表示できる
・古い記事HTMLは削除されないため、不要ファイルは手動で削除推奨


【開発環境】
Python 3.8以上
使用ライブラリ：gspread, oauth2client, jinja2
必要に応じて pip install でインストール


【制作】
つるつるズ 2025年度技術担当
運用や公開についてはメンバー間で相談のうえ管理