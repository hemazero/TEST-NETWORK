import discord
from discord.ext import commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# --- Simple Web Server to keep the bot alive ---
app = Flask('')
@app.route('/')
def home(): return "TEST NETWORK is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot Configuration ---
# Prefix is set to '-' only as requested
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'✅ Logged in as: {bot.user.name}')
    print('Status: Stable & English Version')

# --- Welcome System (Embed) ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Welcome!",
            description=f"Hello {member.mention}, welcome to our server!",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

# --- Info Command (The requested styled text in Embed) ---
@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
        title="🛠 𝐒𝐄𝐑𝐕𝐄𝐑 𝐃𝐈𝐒𝐂𝐎𝐕𝐄𝐑𝐘 | 𝐓𝐄𝐒𝐓 𝐄𝐍𝐕𝐈𝐑𝐎𝐍𝐌𝐄𝐍𝐓",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(
        name="🧪 𝐎𝐯𝐞𝐫𝐯𝐢𝐞𝐰", 
        value="𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐓𝐄𝐒𝐓. > 𝐓𝐡𝐢𝐬 𝐢𝐬 𝐚 𝐩𝐫𝐢𝐯𝐚𝐭𝐞, 𝐝𝐞𝐝𝐢𝐜𝐚𝐭𝐞𝐝 𝐞𝐧𝐯𝐢𝐫𝐨𝐧𝐦𝐞𝐧𝐭 𝐮𝐬𝐞𝐝 𝐞𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞𝐥𝐲 𝐟𝐨𝐫 𝐃𝐢𝐬𝐜𝐨𝐫𝐝 𝐁𝐨𝐭 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭 𝐚𝐧𝐝 𝐟𝐞𝐚𝐭𝐮𝐫𝐞 𝐩𝐫𝐨𝐭𝐨𝐭𝐲𝐩𝐢𝐧𝐠.", 
        inline=False
    )
    embed.add_field(
        name="🎯 𝐏𝐫𝐢𝐦𝐚𝐫𝐲 𝐎𝐛𝐣𝐞𝐜𝐭𝐢𝐯𝐞𝐬", 
        value=(
            "• **𝐁𝐞𝐭𝐚 𝐓𝐞𝐬𝐭𝐢𝐧𝐠:** Stress-testing commands.\n"
            "• **𝐔𝐈/𝐔𝐗 𝐃𝐞𝐬𝐢𝐠𝐧:** Refining Embeds & Buttons.\n"
            "• **𝐃𝐞𝐛𝐮𝐠𝐠𝐢𝐧𝐠:** Fixing API issues.\n"
            "• **𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐌𝐚𝐩𝐩𝐢𝐧𝐠:** Testing role hierarchy."
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
    embed = discord.Embed(title="👤 User Time Info", color=discord.Color.blue())
    embed.add_field(name="Joined Server", value=joined, inline=True)
    embed.add_field(name="Account Created", value=created, inline=True)
    await ctx.send(embed=embed)

# --- Clear Commands (Restricted to Role) ---
@bot.command(name="clear10")
async def clear10(ctx):
    if any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles):
        await ctx.channel.purge(limit=11)
        await ctx.send("🧹 Deleted 10 messages.", delete_after=3)
    # No "else" here means the bot will stay silent if no permission (No Error Msg)

@bot.command(name="clearall")
async def clearall(ctx):
    if any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles):
        await ctx.channel.purge(limit=100)
        await ctx.send("🗑️ Channel cleared.", delete_after=3)

# --- Error Handling (Removed to prevent "Unknown Command" spam) ---
@bot.event
async def on_command_error(ctx, error):
    # This will ignore errors and prevent the bot from crashing or replying with error codes
    pass

# Run everything
if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
