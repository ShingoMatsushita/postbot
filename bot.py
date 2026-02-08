import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
import os

# botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# シドニー時間の設定
SYDNEY = pytz.timezone('Australia/Sydney')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '1449383366423089233'))

def get_weekday():
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    return weekdays[datetime.now(SYDNEY).weekday()] + '曜日'

# 毎日の投稿タスク（シドニー時間の6:00に実行）
@tasks.loop(hours=24)
async def daily_post():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f'❌ チャンネルが見つかりません')
        return

    today = datetime.now(SYDNEY).strftime('%Y年%m月%d日')
    weekday = get_weekday()

    message_text = f"📅 **{today}（{weekday}）**"
    message = await channel.send(message_text)

    thread = await message.create_thread(
        name=f"{today}のタスク",
        auto_archive_duration=1440
    )

    await thread.send("今日のやることをここに書いてください！✨")
    print(f"✅ 毎日の投稿完了: {today}")

# 毎週月曜日の投稿タスク（シドニー時間の6:00に実行）
@tasks.loop(hours=24)
async def weekly_post():
    now = datetime.now(SYDNEY)

    # 月曜日（weekday() == 0）でない場合はスキップ
    if now.weekday() != 0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f'❌ チャンネルが見つかりません')
        return

    week_start = now.strftime('%Y年%m月%d日')

    message_text = f"📆 **今週の予定（{week_start}〜）**"
    message = await channel.send(message_text)

    thread = await message.create_thread(
        name=f"{week_start}週のタスク",
        auto_archive_duration=10080
    )

    await thread.send("今週のやることをここに書いてください！✨")
    print(f"✅ 毎週の投稿完了: {week_start}")

@daily_post.before_loop
async def before_daily_post():
    await bot.wait_until_ready()

    # シドニー時間の6:00まで待機
    now = datetime.now(SYDNEY)
    target_time = now.replace(hour=6, minute=0, second=0, microsecond=0)

    # もし今日の6:00が過ぎていたら、明日の6:00まで待つ
    if now >= target_time:
        target_time = target_time.replace(day=target_time.day + 1)

    wait_seconds = (target_time - now).total_seconds()
    print(f'⏰ 次の毎日投稿まで {wait_seconds/3600:.1f} 時間待機します（{target_time.strftime("%Y-%m-%d %H:%M")} Sydney時間）')
    await discord.utils.sleep_until(target_time)

@weekly_post.before_loop
async def before_weekly_post():
    await bot.wait_until_ready()

    # シドニー時間の6:00まで待機
    now = datetime.now(SYDNEY)
    target_time = now.replace(hour=6, minute=0, second=0, microsecond=0)

    # もし今日の6:00が過ぎていたら、明日の6:00まで待つ
    if now >= target_time:
        target_time = target_time.replace(day=target_time.day + 1)

    wait_seconds = (target_time - now).total_seconds()
    print(f'⏰ 次の毎週投稿チェックまで {wait_seconds/3600:.1f} 時間待機します（{target_time.strftime("%Y-%m-%d %H:%M")} Sydney時間）')
    await discord.utils.sleep_until(target_time)

@bot.event
async def on_ready():
    print(f'{bot.user}としてログインしました')
    print(f'サーバー数: {len(bot.guilds)}')
    print('定期投稿タスクを開始します...')

    # タスクを開始
    daily_post.start()
    weekly_post.start()

    print('✅ Bot起動完了！定期投稿を待機中...')

# botを起動
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError('DISCORD_BOT_TOKEN環境変数が設定されていません')

bot.run(TOKEN)
