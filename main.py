import discord
import os
from flask import Flask
from threading import Thread

# --- إعداد سيرفر الويب لمنع توقف البوت ---
app = Flask('')

@app.route('/')
def home():
    return "TEST NETWORK is Online!"

def run():
    # Render يمرر المنفذ (Port) عبر متغير البيئة
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات ديسكورد ---
intents = discord.Intents.all()  # تفعيل كل الصلاحيات
client = discord.Client(intents=intents)

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396

@client.event
async def on_ready():
    print(f'✅ Logged in as: {client.user.name}')
    print('--- Bot is ready to welcome members ---')

@client.event
async def on_member_join(member):
    # 1. إرسال الترحيب (إنجليزي - بدون إيموجي)
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        welcome_msg = f"Welcome to the server {member.name}. We are glad to have you here."
        await channel.send(welcome_msg)
    
    # 2. إعطاء الرتبة تلقائياً
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
            print(f"Role assigned to {member.name}")
        except Exception as e:
            print(f"Failed to assign role: {e}")

# --- تشغيل البوت ---
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get('TOKEN')
    if token:
        try:
            client.run(token)
        except discord.errors.HTTPException as e:
            print(f"❌ Discord API Error: {e}")
    else:
        print("❌ Error: No TOKEN found in Environment Variables!")
