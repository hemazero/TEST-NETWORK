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
LOG_CHANNEL_ID = 1476043469519716455 # يمكنك تغييره لروم خاص بالسجلات

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} is fully operational')

# --- Welcome Image Function (TV Style) ---
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

    # 1. Auto-Reply
    if message.content.lower() == "hi":
        await message.channel.send("hi 😊")

    # 2. Auto-Mod (Link Protection)
    if "http" in message.content.lower() and not any(role.id == ALLOWED_ROLE_ID for role in message.author.roles):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, links are not allowed!", delete_after=3)

    await bot.process_commands(message)

# --- New Commands ---

@bot.command(name="?")
async def help_menu(ctx):
    embed = discord.Embed(title="📖 Bot Help Menu", color=discord.Color.blue())
    embed.add_field(name="-info", value="Server development details.", inline=True)
    embed.add_field(name="-time", value="Your account age info.", inline=True)
    embed.add_field(name="-server", value="General server statistics.", inline=True)
    embed.add_field(name="-avatar @user", value="Show someone's profile picture.", inline=True)
    embed.add_field(name="-ping", value="Check bot response speed.", inline=True)
    embed.add_field(name="-clear10 / -clearall", value="Admin clean up tools.", inline=False)
    embed.set_footer(text="Use the prefix '-' before each command.")
    await ctx.send(embed=embed)

@bot.command(name="server")
async def server_info(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name} Stats", color=discord.Color.green())
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.random())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

# --- Original Commands ---
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

@bot.command(name="testwelcome")
async def test_welcome(ctx):
    img = create_welcome_image(ctx.author)
    file = discord.File(img, filename='welcome.png')
    await ctx.send(f"**Welcome {ctx.author.mention}**\n**You are member #{len(ctx.guild.members)}**", file=file)

@bot.event
async def on_command_error(ctx, error): pass

if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
