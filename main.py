import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
from PIL import Image, ImageDraw
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

# --- IDs ---
WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')

# --- Function to generate ONLY a Square Avatar Image (No Text, No Brackets) ---
def create_welcome_image(member):
    # 1. Create a SMALLER, strictly Square black background (e.g., 400x400)
    width, height = 400, 400
    image = Image.new('RGB', (width, height), color='black')
    
    # 2. Load and process member's avatar (Small Size)
    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)
    avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")
    
    # Resize avatar to a suitable small size
    avatar_size = 150
    avatar_image = avatar_image.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # Make avatar circular
    mask = Image.new('L', (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    
    # Paste Avatar (Strictly centered, No padding from top needed for true square centering)
    avatar_x = (width - avatar_size) // 2
    avatar_y = (height - avatar_size) // 2
    image.paste(avatar_image, (avatar_x, avatar_y), mask)

    # 3. Text & Brackets Removal
    # All text generation code has been deleted as requested to create a completely blank square image.

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
        # Generate & Send Image
        welcome_file = create_welcome_image(member)
        file = discord.File(welcome_file, filename='welcome.png')
        await channel.send(f"Welcome to the server, {member.mention}!", file=file)

# --- Command: Test Welcome Image ---
@bot.command(name="testwelcome")
async def test_welcome(ctx):
    # Sends the compact, square welcome image using command author's info
    await ctx.send("🔍 **Testing Compact Square Avatar Image:**")
    # Generate & Send Image
    welcome_file = create_welcome_image(ctx.author)
    file = discord.File(welcome_file, filename='welcome.png')
    await ctx.send(file=file)

# --- Other Commands ---
@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
        title="🛠 SERVER DISCOVERY | TEST ENVIRONMENT",
        color=0xf1c40f, # Gold
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

# --- Silence errors ---
@bot.event
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
