# Discord定期投稿Bot

シドニー時間の毎日6:00と毎週月曜6:00に自動投稿するDiscord Bot

## 機能

- 毎日6:00（シドニー時間）に日付投稿 + スレッド作成
- 毎週月曜6:00（シドニー時間）に週次投稿 + スレッド作成

## Renderでのデプロイ方法

### 1. GitHubリポジトリを作成

1. このフォルダをGitHubにプッシュ

### 2. Renderでデプロイ

1. https://render.com/ にアクセスしてサインアップ
2. 「New +」→「Background Worker」を選択
3. GitHubリポジトリを接続
4. 以下の設定を入力：
   - **Name**: discord-bot（任意の名前）
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

### 3. 環境変数を設定

Renderの「Environment」タブで以下を設定：

- `DISCORD_BOT_TOKEN`: あなたのDiscord Botトークン
- `DISCORD_CHANNEL_ID`: あなたのDiscordチャンネルID

### 4. デプロイ

「Create Background Worker」をクリックしてデプロイ完了！

## ローカルでのテスト

```bash
export DISCORD_BOT_TOKEN="your_token_here"
export DISCORD_CHANNEL_ID="your_channel_id_here"
python bot.py
```
