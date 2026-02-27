import discord
from discord.ext import commands
from discord import app_commands
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
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents)

    async def setup_hook(self):
        # مزامنة الأوامر لتظهر في قائمة الديسكورد (Slash Commands)
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

bot = MyBot()

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')

# --- الترحيب المنسق ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="New Member Joined!",
            description=f"Welcome to the server {member.mention}. We are glad to have you here.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

# --- أمر -info المنسق (نص عادي عريض كما طلبت) ---
@bot.command(name="info")
async def info(ctx):
    info_text = (
        "🛠 𝐒𝐄𝐑𝐕𝐄𝐑 𝐃𝐈𝐒𝐂𝐎𝐕𝐄𝐑𝐘 | 𝐓𝐄𝐒𝐓 𝐄𝐍𝐕𝐈𝐑𝐎𝐍𝐌𝐄𝐍𝐓\n\n"
        "🧪 𝐎𝐯𝐞𝐫𝐯𝐢𝐞𝐰\n"
        "𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐓𝐄𝐒𝐓. > 𝐓𝐡𝐢𝐬 𝐢𝐬 𝐚 𝐩𝐫𝐢𝐯𝐚𝐭𝐞, 𝐝𝐞𝐝𝐢𝐜𝐚𝐭𝐞𝐝 𝐞𝐧𝐯𝐢𝐫𝐨𝐧𝐦𝐞𝐧𝐭 𝐮𝐬𝐞𝐝 𝐞𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞𝐥𝐲 𝐟𝐨𝐫 𝐃𝐢𝐬𝐜𝐨𝐫𝐝 𝐁𝐨𝐭 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭 𝐚𝐧𝐝 𝐟𝐞𝐚𝐭𝐮𝐫𝐞 𝐩𝐫𝐨𝐭𝐨𝐭𝐲𝐩𝐢𝐧𝐠.\n\n"
        "🎯 𝐏𝐫𝐢𝐦𝐚𝐫𝐲 𝐎𝐛𝐣𝐞𝐜𝐭𝐢𝐯𝐞𝐬\n"
        "𝐁𝐞𝐭𝐚 𝐓𝐞𝐬𝐭𝐢𝐧𝐠: 𝐒𝐭𝐫𝐞𝐬𝐬-𝐭𝐞𝐬𝐭𝐢𝐧𝐠 𝐛𝐨𝐭 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐚𝐧𝐝 𝐥𝐨𝐠𝐢𝐜.\n\n"
        "𝐔𝐈/𝐔𝐗 𝐃𝐞𝐬𝐢𝐠𝐧: 𝐂𝐫𝐚𝐟𝐭𝐢𝐧𝐠 𝐚𝐧𝐝 𝐫𝐞𝐟𝐢𝐧𝐢𝐧𝐠 𝐄𝐦𝐛𝐞𝐝𝐬, 𝐁𝐮𝐭𝐭𝐨𝐧𝐬, 𝐚𝐧𝐝 𝐌𝐨𝐝𝐚𝐥𝐬.\n\n"
        "𝐃𝐞𝐛𝐮𝐠𝐠𝐢𝐧𝐠: 𝐈𝐝𝐞𝐧𝐭𝐢𝐟𝐲𝐢𝐧𝐠 𝐚𝐧𝐝 𝐟𝐢𝐱𝐢𝐧𝐠 𝐀𝐏𝐈 𝐢𝐬𝐬𝐮𝐞𝐬 𝐨𝐫 𝐜𝐫𝐚𝐬𝐡 𝐥𝐨𝐨𝐩𝐬.\n\n"
        "𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐌𝐚𝐩𝐩𝐢𝐧𝐠: 𝐓𝐞𝐬𝐭𝐢𝐧𝐠 𝐫𝐨𝐥𝐞 𝐡𝐢𝐞𝐫𝐚𝐫𝐜𝐡𝐢𝐞𝐬 𝐚𝐧𝐝 𝐢𝐧𝐭𝐞𝐫𝐚𝐜𝐭𝐢𝐨𝐧 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲."
    )
    await ctx.send(info_text)

# --- أوامر Slash (تظهر بمجرد كتابة الحرف الأول /) ---

@bot.tree.command(name="time", description="Show your time in server and discord")
async def time_slash(interaction: discord.Interaction):
    member = interaction.user
    joined_at = member.joined_at.strftime("%Y/%m/%d")
    created_at = member.created_at.strftime("%Y/%m/%d")
    embed = discord.Embed(title="👤 User Info", color=discord.Color.blue())
    embed.add_field(name="📅 Joined Server", value=joined_at, inline=True)
    embed.add_field(name="🚀 Account Age", value=created_at, inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear10", description="Delete last 10 messages")
async def clear10_slash(interaction: discord.Interaction):
    has_role = any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)
    if has_role:
        await interaction.response.send_message("🧹 Cleaning...", ephemeral=True)
        await interaction.channel.purge(limit=10)
    else:
        await interaction.response.send_message("❌ No permission.", ephemeral=True)

@bot.tree.command(name="clearall", description="Delete many messages")
async def clearall_slash(interaction: discord.Interaction):
    has_role = any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)
    if has_role:
        await interaction.response.send_message("🗑️ Channel Cleared!", ephemeral=True)
        await interaction.channel.purge(limit=100)
    else:
        await interaction.response.send_message("❌ No permission.", ephemeral=True)

# الاستجابة للأوامر اليدوية القديمة
@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.content.startswith("-") or message.content.startswith("/"):
        has_role = any(role.id == ALLOWED_ROLE_ID for role in message.author.roles)
        
        if message.content == "/clearall" and has_role:
            await message.channel.purge(limit=100)
        elif message.content == "-clear10" and has_role:
            await message.channel.purge(limit=11)
            
    await bot.process_commands(message)

# تشغيل
Thread(target=run).start()
bot.run(os.environ.get('TOKEN'))
