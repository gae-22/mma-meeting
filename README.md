# MMA-MEETING

これは部会を楽にしようという部長のめんどくさい精神から生まれた web アプリです．

以下の機能があります．ほぼ Wiki からの引用．

-   今年度のすべての議題
-   直近の部会の議題
-   投票用の GoogleForm へのリンク，パスワード
-   部会の開催予定日時，教室

その他にも，`GAS`を用いて，GoogleForm を自動で作成しています．

# Installation

## 1. Clone this repository

このリポジトリをクローンする．

```bash
git clone ssh://git@gitlab.mma.club.uec.ac.jp:2223/gae/mma-meeting.git
```

## 3. Download Goggle API credentials

`GAS`を用いて，GoogleForm を自動で作成しているため，`Google API`の認証情報が必要になる．
必要なスコープを設定した`json`ファイルをダウンロードし，`datas`ディレクトリに配置する．

## 4. Run the server

```bash
docker compose up --build 
```
