import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

# ダミーWebサーバーを起動するためのファイルをインポート
from keep_alive import keep_alive

# .envファイルから環境変数（トークンやキー）を読み込む
load_dotenv()
DISCORD_TOKEN = os.getenv('MTQ4NjIzNzUxODAyOTY1MTk5MA.GAvJO7.zqD_897BsjvepSnhn5txVSCPNAbDKzn4-crgJs')
GEMINI_API_KEY = os.getenv('AIzaSyBVP0VZNYFDCr8ok5vBhUlF34EwbfBSAww')

# Gemini APIの設定（軽快に動くFlashモデルを指定しています）
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Discordボットの権限（Intents）設定
# メッセージの内容を読み取るために必要です
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # ボットがDiscordに正常に接続された時に表示されます
    print(f'ログイン完了: {client.user}')

@client.event
async def on_message(message):
    # ボット自身のメッセージには反応しないようにする（無限ループ防止）
    if message.author == client.user:
        return

    # ボットがメンション（@）された時だけ反応する
    if client.user in message.mentions:
        # メッセージからメンション部分（@ボット名）を削除して、純粋な質問だけを取り出す
        prompt = message.content.replace(f'<@{client.user.id}>', '').strip()

        if not prompt:
            await message.channel.send("何か話しかけてください！")
            return

        # Discord上で「入力中...」のアニメーションを表示しながらGeminiに通信
        async with message.channel.typing():
            try:
                # Geminiに質問を投げて回答を生成
                response = model.generate_content(prompt)
                # 生成された回答をDiscordに返信
                await message.reply(response.text)
            except Exception as e:
                # 何かエラーが起きた時の処理
                await message.reply(f"すみません、エラーが発生しました: {e}")

# RenderのWeb Serviceで起動し続けるためのダミーサーバーを実行
keep_alive()

# ボットを起動する
client.run(DISCORD_TOKEN)
