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
ALLOWED_ROLE_ID = 1476034819925217381  # آيدي الرتبة المسموح لها بالمسح

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')

# --- الترحيب بنظام Embed منسق ---
@bot.event
async def on_member_join(member):
    # إعطاء الرتبة التلقائية
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: print("Error adding role")

    # إرسال الترحيب المنسق
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="New Member Joined!",
            description=f"Welcome to the server {member.mention}. We are glad to have you here.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="TEST NETWORK System")
        await channel.send(embed=embed)

# --- أمر حساب الوقت ---
@bot.command(name="time")
async def account_time(ctx):
    member = ctx.author
    joined_at = member.joined_at.strftime("%Y/%m/%d")
    created_at = member.created_at.strftime("%Y/%m/%d")
    
    embed = discord.Embed(title=f"👤 User Information", color=discord.Color.blue())
    embed.add_field(name="📅 Joined Server", value=f"{joined_at}", inline=True)
    embed.add_field(name="🚀 Account Age", value=f"{created_at}", inline=True)
    await ctx.send(embed=embed)

# --- أوامر الحذف (Clear) ---

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # التحقق من وجود الرتبة المسموح لها
    has_role = any(role.id == ALLOWED_ROLE_ID for role in message.author.roles)

    # أمر /clearall
    if message.content == "/clearall":
        if has_role:
            deleted = await message.channel.purge(limit=100)
            await message.channel.send(f"🗑️ Done! Deleted {len(deleted)} messages.", delete_after=5)
        else:
            await message.channel.send("❌ You don't have the required role to use this.", delete_after=5)
        return

    # أمر -clear10
    if message.content == "-clear10":
        if has_role:
            deleted = await message.channel.purge(limit=11)
            await message.channel.send(f"🧹 Done! Deleted 10 messages.", delete_after=5)
        else:
            await message.channel.send("❌ You don't have the required role to use this.", delete_after=5)
        return

    await bot.process_commands(message)

# تشغيل
Thread(target=run).start()
bot.run(os.environ.get('TOKEN'))
