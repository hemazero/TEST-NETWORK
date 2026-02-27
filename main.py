import discord
from discord.ext import commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# --- إعداد سيرفر الويب ---
app = Flask('')
@app.route('/')
def home(): return "TEST NETWORK is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
OWNER_ID = 1476034819925217381  # الآيدي الخاص بك

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Welcome to the server {member.name}. We are glad to have you here.")
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

# --- أمر حساب الوقت (Time) ---
@bot.command(name="time")
async def account_time(ctx):
    member = ctx.author
    joined_at = member.joined_at.strftime("%Y/%m/%d")
    created_at = member.created_at.strftime("%Y/%m/%d")
    now = datetime.now(member.joined_at.tzinfo)
    days_in_server = (now - member.joined_at).days
    days_in_discord = (now - member.created_at).days

    embed = discord.Embed(title=f"👤 User Info - {member.name}", color=discord.Color.blue())
    embed.add_field(name="📅 Joined Server", value=f"**Date:** {joined_at}\n**Since:** {days_in_server} days", inline=True)
    embed.add_field(name="🚀 Account Age", value=f"**Created:** {created_at}\n**Total:** {days_in_discord} days", inline=True)
    await ctx.send(embed=embed)

# --- أوامر الحذف (Clear) ---

# 1. حذف 10 رسائل (أمر يبدأ بـ -)
@bot.command(name="clear10")
async def clear_ten(ctx):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ You don't have permission to use this command.")
    
    deleted = await ctx.channel.purge(limit=11) # يحذف 10 + رسالة الأمر نفسه
    await ctx.send(f"🧹 Done! Deleted {len(deleted)-1} messages.", delete_after=3)

# 2. حذف كل الرسائل (أمر يبدأ بـ /)
@bot.command(name="clearall")
async def clear_all(ctx):
    # ملاحظة: برمجياً نستخدم الـ prefix المعرف للبوت وهو "-"
    # لكن سأجعل البوت يستجيب لـ /clearall أيضاً
    pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # التحقق إذا كتب المستخدم /clearall يدوياً
    if message.content == "/clearall" and message.author.id == OWNER_ID:
        deleted = await message.channel.purge(limit=100) # يحذف آخر 100 رسالة (الحد الأقصى المعتاد)
        return await message.channel.send(f"🗑️ Channel cleared! {len(deleted)} messages removed.", delete_after=5)

    await bot.process_commands(message)

# تشغيل
Thread(target=run).start()
bot.run(os.environ.get('TOKEN'))
