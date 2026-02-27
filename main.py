import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- إعداد خادم الويب لإبقاء البوت حياً ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.members = True  # ضروري جداً لرؤية الأعضاء الجدد

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (TEST NETWORK)')

@bot.event
async def on_member_join(member):
    # 1. إعطاء الرتبة تلقائياً
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
            print(f"Assigned role to {member.name}")
        except Exception as e:
            print(f"Error assigning role: {e}")

    # 2. إرسال رسالة الترحيب
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        welcome_msg = f"Welcome to the server {member.name}. We are glad to have you here."
        await channel.send(welcome_msg)

# تشغيل خادم الويب والبوت
keep_alive()
token = os.environ.get('TOKEN') # سنضع التوكن في إعدادات Render
bot.run(token)
