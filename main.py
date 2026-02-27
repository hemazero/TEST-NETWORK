import discord
from discord.ext import commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# --- Web Server for Railway uptime ---
app = Flask('')
@app.route('/')
def home(): return "TEST NETWORK is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot Config ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

# --- IDs (Ensure these are correct) ---
WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')

# --- Function to generate Welcome Image ---
def create_welcome_image(member, member_count):
    # 1. Create a black background image (800x400)
    width, height = 800, 400
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)

    # 2. Load and process member's avatar
    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)
    avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")
    
    # Resize avatar
    avatar_size = 150
    avatar_image = avatar_image.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # Make avatar circular
    mask = Image.new('L', (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    
    # Paste avatar onto background
    avatar_x = (width - avatar_size) // 2
    avatar_y = (height - avatar_size) // 2 - 50 # Slightly above center
    image.paste(avatar_image, (avatar_x, avatar_y), mask)

    # 3. Add Welcome Text
    # Define fonts - attempt to load a font, fallback to default
    try:
        # Update path to a valid ttf font file if needed (e.g., 'arial.ttf' for Arabic support)
        font_path = 'arial.ttf' 
        font_title = ImageFont.truetype(font_path, 40)
        font_body = ImageFont.truetype(font_path, 30)
    except IOError:
        print("Warning: Standard font not found, using default. Arabic text might not render correctly.")
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    # Define text content
    text_title = f"مرحبا ({member.name})"
    text_body = f"انت العضو رقم {member_count}"

    # Calculate text positions to center them
    title_bbox = draw.textbbox((0, 0), text_title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = avatar_y + avatar_size + 20

    body_bbox = draw.textbbox((0, 0), text_body, font=font_body)
    body_width = body_bbox[2] - body_bbox[0]
    body_x = (width - body_width) // 2
    body_y = title_y + 50

    # Draw text on image
    draw.text((title_x, title_y), text_title, font=font_title, fill='white')
    draw.text((body_x, body_y), text_body, font=font_body, fill='white')

    # 4. Save to BytesIO to send
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# --- Real Welcome Event ---
@bot.event
async def on_member_join(member):
    # Auto-assign role
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

    # Get welcome channel
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        member_count = len(member.guild.members)
        # Generate image
        welcome_file = create_welcome_image(member, member_count)
        # Send image as file
        file = discord.File(welcome_file, filename='welcome.png')
        await channel.send(f"Welcome {member.mention}!", file=file)

# --- Command: Test Welcome Image ---
@bot.command(name="testwelcome")
async def test_welcome(ctx):
    # This sends the welcome image using the command author's info for testing
    member_count = len(ctx.guild.members)
    await ctx.send("🔍 **Testing Welcome Image:**")
    # Generate image
    welcome_file = create_welcome_image(ctx.author, member_count)
    # Send image as file
    file = discord.File(welcome_file, filename='welcome.png')
    await ctx.send(file=file)

# --- Info Command (Static Embed with standard formatting) ---
@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
        title="🛠 SERVER DISCOVERY | TEST ENVIRONMENT",
        color=0xf1c40f, # Gold
        timestamp=datetime.utcnow()
    )
    embed.add_field(
        name="🧪 Overview", 
        value="Welcome to TEST. > This is a private, dedicated environment used exclusively for Discord Bot Development and feature prototyping.", 
        inline=False
    )
    embed.add_field(
        name="🎯 Primary Objectives", 
        value=(
            "• **Beta Testing:** Stress-testing commands.\n"
            "• **UI/UX Design:** Refining Embeds & Buttons.\n"
            "• **Debugging:** Fixing API issues.\n"
            "• **Permission Mapping:** Testing role hierarchy."
        ), 
        inline=False
    )
    await ctx.send(embed=embed)

# --- Time Command ---
@bot.command(name="time")
async def time_cmd(ctx):
    member = ctx.author
    joined = member.joined_at.strftime("%Y/%m/%d")
    created = member.created_at.strftime("%Y/%m/%d")
    embed = discord.Embed(title="👤 User Time Info", color=0x3498db)
    embed.add_field(name="Joined Server", value=f"**{joined}**", inline=True)
    embed.add_field(name="Account Created", value=f"**{created}**", inline=True)
    await ctx.send(embed=embed)

# --- Clear Commands (Restricted by Role ID) ---
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

# --- Silence Errors ---
@bot.event
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
