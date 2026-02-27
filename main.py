import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# --- Web Server for Uptime ---
app = Flask('')
@app.route('/')
def home(): return "TEST NETWORK is Online!"

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
    print(f'✅ Logged in as: {bot.user.name}')

# --- Function to generate Square Image with WELCOME text inside ---
def create_welcome_image(member):
    # 1. Create a Square black background (400x400)
    width, height = 400, 400
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)
    
    # 2. Process Avatar
    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)
    avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")
    
    avatar_size = 180
    avatar_image = avatar_image.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    mask = Image.new('L', (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    
    avatar_x = (width - avatar_size) // 2
    avatar_y = 60 # Pushed slightly up to make room for WELCOME
    image.paste(avatar_image, (avatar_x, avatar_y), mask)

    # 3. Add WELCOME text INSIDE the image
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path): font_path = 'arial.ttf'
        font = ImageFont.truetype(font_path, 45)
    except:
        font = ImageFont.load_default()

    text = "WELCOME"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = avatar_y + avatar_size + 30
    
    draw.text((text_x, text_y), text, font=font, fill='white')

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# --- Events ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        member_count = len(member.guild.members)
        welcome_file = create_welcome_image(member)
        file = discord.File(welcome_file, filename='welcome.png')
        
        # Send Name and Member Count as text BELOW the image
        username = member.global_name if member.global_name else member.name
        await channel.send(
            f"**Welcome {username}**\n**You are member #{member_count}**", 
            file=file
        )

# --- Test Command ---
@bot.command(name="testwelcome")
async def test_welcome(ctx):
    member_count = len(ctx.guild.members)
    welcome_file = create_welcome_image(ctx.author)
    file = discord.File(welcome_file, filename='welcome.png')
    
    username = ctx.author.global_name if ctx.author.global_name else ctx.author.name
    await ctx.send(
        f"**Welcome {username}**\n**You are member #{member_count}**", 
        file=file
    )

# --- Clear Commands ---
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
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
