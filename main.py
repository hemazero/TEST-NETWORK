import discord
from discord.ext import commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread

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

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')

# --- Function to generate Welcome Embed (Reusable) ---
def create_welcome_embed(member):
    embed = discord.Embed(
        title="Welcome to the Server!",
        description=f"Hello {member.mention}, we are glad to have you here.",
        color=0x3498db # Blue
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="TEST NETWORK System")
    return embed

# --- Real Welcome Event ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = create_welcome_embed(member)
        await channel.send(embed=embed)

# --- Command: Test Welcome ---
@bot.command(name="testwelcome")
async def test_welcome(ctx):
    # This sends the welcome embed using the command author's info
    embed = create_welcome_embed(ctx.author)
    await ctx.send("🔍 **Testing Welcome Message:**")
    await ctx.send(embed=embed)

# --- Info Command ---
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

# --- Silence Errors ---
@bot.event
async def on_command_error(ctx, error):
    pass

if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
