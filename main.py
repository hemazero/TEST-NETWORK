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

# --- Function to generate Small & Clean Welcome Image ---
def create_welcome_image(member, member_count):
    # 1. Create a much SMALLER & Compact black background (e.g., 600x200)
    width, height = 600, 200
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)

    # 2. Process Member Avatar (Small Size)
    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)
    avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")
    
    # Standard small avatar size
    avatar_size = 80
    avatar_image = avatar_image.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # Make avatar circular
    mask = Image.new('L', (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    
    # Paste Avatar (Centered horizontally, small padding from top)
    avatar_x = (width - avatar_size) // 2
    avatar_y = 20
    image.paste(avatar_image, (avatar_x, avatar_y), mask)

    # 3. Add Clean Text (No Brackets, Small Font)
    # Define cleaner, standardized font paths
    font_sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" # Common Linux path
    font_serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" # Fallback/Alternative
    
    # Standard common sans-serif font
    if os.path.exists(font_sans): font_path = font_sans
    elif os.path.exists(font_serif): font_path = font_serif
    else: font_path = 'arial.ttf' # Windows common path

    # Load small font sizes
    try:
        font_main = ImageFont.truetype(font_path, 24)
        font_sub = ImageFont.truetype(font_path, 18)
    except IOError:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Define clean English text content
    username = member.global_name if member.global_name else member.name # Clean name
    text_main = f"Welcome {username}"
    text_sub = f"You are member #{member_count}"

    # Calculate centered positions with minimal spacing
    main_bbox = draw.textbbox((0, 0), text_main, font=font_main)
    main_width = main_bbox[2] - main_bbox[0]
    main_x = (width - main_width) // 2
    main_y = avatar_y + avatar_size + 15

    sub_bbox = draw.textbbox((0, 0), text_sub, font=font_sub)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (width - sub_width) // 2
    sub_y = main_y + 35

    # Draw Text in White
    draw.text((main_x, main_y), text_main, font=font_main, fill='white')
    draw.text((sub_x, sub_y), text_sub, font=font_sub, fill='white')

    # 4. Save to BytesIO to send
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# --- Events ---
@bot.event
async def on_member_join(member):
    # Role assignment
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

    # Get welcome channel
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        member_count = len(member.guild.members)
        # Generate & Send Image
        welcome_file = create_welcome_image(member, member_count)
        file = discord.File(welcome_file, filename='welcome.png')
        await channel.send(f"Welcome {member.mention}!", file=file)

# --- Test Command ---
@bot.command(name="testwelcome")
async def test_welcome(ctx):
    # Sends the compact, clean welcome image using command author's info
    member_count = len(ctx.guild.members)
    await ctx.send("🔍 **Testing Compact Welcome Image:**")
    # Generate & Send Image
    welcome_file = create_welcome_image(ctx.author, member_count)
    file = discord.File(welcome_file, filename='welcome.png')
    await ctx.send(file=file)

# --- Silence Command Errors ---
@bot.event
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
