import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# تشغيل سيرفر ويب لإبقاء البوت حياً
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# إعدادات البوت
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396

@bot.event
async def on_ready():
    print(f'✅ Connected as: {bot.user.name}')

@bot.event
async def on_member_join(member):
    # 1. إرسال ترحيب (إنجليزي بدون إيموجي)
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Welcome to the server {member.name}. We are glad to have you here.")

    # 2. إعطاء الرتبة
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
            print(f"Role assigned to {member.name}")
        except:
            print("Check bot permissions (Role must be higher than the target role)")

# تشغيل البوت
if __name__ == "__main__":
    Thread(target=run).start()
    token = os.environ.get('TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ Error: TOKEN environment variable not found!")
