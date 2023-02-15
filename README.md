# ig-pr-times
### 概要
- 任意のユーザーのPR投稿を監視するツールです。
- 新規PR投稿をSlackに通知します。

### 使い方
#### 1. リポジトリをクローン
``` bash
$ git clone git@github.com:hk512/ig-pr-times.git
```

#### 2. リポジトリに移動
``` bash
$ cd ig-pr-times
```

#### 3. 仮想環境の作成&有効化
``` bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. 必要なライブラリのインストール
``` bash
pip install --upgrade pip
pip install instaloader
```

#### 5. Configファイルの作成
``` bash
$ cp config/config.sample.json config/config.json
```

#### 6. Configファイルの編集
example
```json
{
  "user_id": "your user id",
  "password": "your login password",
  "webhook_url": "your webhook url",
  "targets": [
    "target user id",
    "target user id",
    "target user id"
  ]
}
```

各項目について
- user_id: InstagramのユーザーのID
- password: Instagramのパスワード
- webhook_url: SlackのWebhook URL
- targets: 監視するユーザーのID(複数指定可)