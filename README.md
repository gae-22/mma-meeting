# MMA-MEETING

これは部会を楽にしようという部長のめんどくさい精神から生まれた web アプリです．

以下の機能があります．ほぼ Wiki からの引用．

-   今年度のすべての議題
-   直近の部会の議題
-   投票用の GoogleForm へのリンク，パスワード
-   部会の開催予定日時，教室

その他にも，`gas`を用いて，GoogleForm を自動で作成しています．

# Installation

## 1. Clone this repository

このリポジトリをクローンする．

```bash
git clone ssh://git@gitlab.mma.club.uec.ac.jp:2223/gae/mma-meeting.git
```

## 2. Start the virtual environment

```bash
python3 -m venv .venv       # 仮想環境を作成
source .venv/bin/activate   # 仮想環境を有効化
```

## 3. Install packages

以下のコマンドで`requirements.txt`からパッケージをインストールする．
ただ，仮想環境で実行することを推奨する．

```bash
pip install -r requirements.txt
```

## 4. Run the server

起動自体は以下のコマンドで行う．しかし，実際に動かすためには，`wiki`のログイン情報やスプレッドシート編集用の`json`ファイルなどの設定が必要になる．
ログイン情報に関しては，スクレイピングをするプログラムファイルに直接書くようにいっているサイトが多いが，今回は gialab にあげることを考えて，`json`ファイルに書いている．
今回は`datas`ディレクトリを設定ファイル保管場所にした．

```bash
python server.py
```

### 参考

[Flask](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/)  
[ログインのいるサイトからのスクレイピング](https://zenn.dev/mamekko/articles/ea44fe8a77da7c)  
[ログイン情報を別ファイルに保存](https://qiita.com/fujisystem/items/95208f86c21a181d55a3)
[Python で SpreadSheet を編集する](https://zenn.dev/eito_blog/articles/02c132bbc1c4bd)  
[Python でファイルの読み書き](https://zenn.dev/makio/articles/66e7e24d7c4478)
