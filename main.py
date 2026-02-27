import discord
from discord.ext import commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# --- إعداد سيرفر الويب (اختياري في ريلواي ولكن جيد للاحتياط) ---
app = Flask('')
@app.route('/')
def home(): return "TEST NETWORK is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
intents = discord.Intents.all()
# استخدمنا commands.Bot لسهولة إضافة الأوامر
bot = commands.Bot(command_prefix="-", intents=intents)

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')

@bot.event
async def on_member_join(member):
    # الترحيب التلقائي
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Welcome to the server {member.name}. We are glad to have you here.")
    
    # الرتبة التلقائية
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
        except:
            print("Failed to assign role. Check permissions.")

# --- أمر حساب الوقت (Time Command) ---
@bot.command(name="time")
async def account_time(ctx):
    member = ctx.author
    
    # حساب تاريخ الانضمام للسيرفر
    joined_at = member.joined_at.strftime("%Y/%m/%d")
    # حساب تاريخ إنشاء الحساب في ديسكورد
    created_at = member.created_at.strftime("%Y/%m/%d")
    
    # حساب المدة بالأيام (اختياري للإضافة)
    now = datetime.now(member.joined_at.tzinfo)
    days_in_server = (now - member.joined_at).days
    days_in_discord = (now - member.created_at).days

    # إنشاء المربع المنسق (Embed)
    embed = discord.Embed(
        title=f"👤 User Information - {member.name}",
        description="Here are the details about your time with us!",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    embed.add_field(
        name="📅 Joined Server", 
        value=f"**Date:** {joined_at}\n**Duration:** {days_in_server} days ago", 
        inline=False
    )
    
    embed.add_field(
        name="🚀 Discord Anniversary", 
        value=f"**Created on:** {created_at}\n**Total age:** {days_in_discord} days", 
        inline=False
    )
    
    embed.set_footer(text="TEST NETWORK • Security & System", icon_url=bot.user.avatar.url if bot.user.avatar else None)

    await ctx.send(embed=embed)

# تشغيل الخادم والبوت
Thread(target=run).start()
bot.run(os.environ.get('TOKEN'))
