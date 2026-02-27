import discord
from discord.ext import commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread
from PIL import Image, ImageDraw
import requests
from io import BytesIO

# --- Web Server ---
app = Flask('')
@app.route('/')
def home(): return "SYSTEM ONLINE"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot Config ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

# --- IDs ---
WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} is ready')

# --- Welcome Image Function ---
def create_welcome_image(member):
    width, height = 600, 250
    image = Image.new('RGB', (width, height), color='black')
    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)
    avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")
    avatar_size = 180 
    avatar_image = avatar_image.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
    mask = Image.new('L', (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    image.paste(avatar_image, ((width - avatar_size) // 2, (height - avatar_size) // 2), mask)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# --- Events ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role: await member.add_roles(role)
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        img = create_welcome_image(member)
        file = discord.File(img, filename='welcome.png')
        await channel.send(f"**Welcome {member.mention}**\n**You are member #{len(member.guild.members)}**", file=file)

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.content.lower() == "hi":
        await message.channel.send("hi 😊")
    if "http" in message.content.lower() and not any(role.id == ALLOWED_ROLE_ID for role in message.author.roles):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, links are not allowed!", delete_after=3)
    await bot.process_commands(message)

# --- Organized Help Menu ---
@bot.command(name="?")
async def help_menu(ctx):
    embed = discord.Embed(title="✨ TEST NETWORK Commands", color=0x3498db)
    
    embed.add_field(
        name="🎮 **General**", 
        value="`-?`, `-ping`, `-avatar @user`, `-boost`", 
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ **Information**", 
        value="`-info`, `-time`", 
        inline=False
    )
    
    embed.add_field(
        name="🛠️ **Admin Tools**", 
        value="`-clear10`, `-clearall`, `-testwelcome`", 
        inline=False
    )
    
    await ctx.send(embed=embed)

# --- Boost Command ---
@bot.command(name="boost")
async def boost(ctx):
    embed = discord.Embed(
        title="🚀 Server Boost",
        description="Help us reach new levels! Every boost unlocks amazing perks for everyone.",
        color=0xff73fa # Boost Pink Color
    )
    embed.add_field(name="How to boost?", value="Click on the server name and select **'Server Boost'**.", inline=False)
    embed.set_footer(text="Thank you for supporting us!")
    await ctx.send(embed=embed)

# --- Rest of Commands (With Role Protection) ---

@bot.command(name="testwelcome")
async def test_welcome(ctx):
    # تقييد الأمر للإدارة فقط
    if any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles):
        img = create_welcome_image(ctx.author)
        file = discord.File(img, filename='welcome.png')
        await ctx.send(f"**Welcome {ctx.author.mention}**\n**You are member #{len(ctx.guild.members)}**", file=file)
    else:
        await ctx.send("❌ Access Denied: Admin role required.", delete_after=3)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar of {member.name}", color=0x000000)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(title="🛠 SERVER DISCOVERY", color=0xf1c40f)
    embed.add_field(name="🧪 Overview", value="Private environment for Bot Development.", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="time")
async def time_cmd(ctx):
    joined = ctx.author.joined_at.strftime("%Y/%m/%d")
    created = ctx.author.created_at.strftime("%Y/%m/%d")
    embed = discord.Embed(title="👤 Time Info", color=0x3498db)
    embed.add_field(name="Joined", value=joined, inline=True)
    embed.add_field(name="Created", value=created, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="clear10")
async def clear10(ctx):
    if any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles):
        await ctx.channel.purge(limit=11)
        await ctx.send("Sweep success! 🧹", delete_after=3)

@bot.command(name="clearall")
async def clearall(ctx):
    if any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles):
        await ctx.channel.purge(limit=100)
        await ctx.send("Channel reset! 🗑️", delete_after=3)

@bot.event
async def on_command_error(ctx, error): pass

if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
