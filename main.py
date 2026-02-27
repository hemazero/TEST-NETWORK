import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# --- إعداد سيرفر الويب لضمان الاستمرارية ---
app = Flask('')
@app.route('/')
def home(): return "TEST NETWORK is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت الأساسية ---
intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self):
        # البادئة هي "-" للأوامر العادية
        super().__init__(command_prefix="-", intents=intents, help_command=None)

    async def setup_hook(self):
        # مزامنة أوامر الـ Slash لتظهر في القائمة عند كتابة /
        await self.tree.sync()
        print(f"✅ Synced Slash Commands for {self.user}")

bot = MyBot()

# --- الآيديات الخاصة بك ---
WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'🚀 {bot.user.name} جاهز للعمل!')
    await bot.change_presence(activity=discord.Game(name="/help | -info"))

# --- 1. نظام الترحيب المنسق (Embed) ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: print("Error giving role")

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="✨ عضو جديد انضم إلينا!",
            description=f"أهلاً بك {member.mention} في سيرفرنا المتواضع.\nيسعدنا انضمامك إلينا!",
            color=0x2ecc71, # لون أخضر
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="TEST NETWORK System")
        await channel.send(embed=embed)

# --- 2. أمر -info المنسق (مربع ذهبي) ---
@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
        title="🛠 𝐒𝐄𝐑𝐕𝐄𝐑 𝐃𝐈𝐒𝐂𝐎𝐕𝐄𝐑𝐘 | 𝐓𝐄𝐒𝐓 𝐄𝐍𝐕𝐈𝐑𝐎𝐍𝐌𝐄𝐍𝐓",
        color=0xf1c40f, # لون ذهبي
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
    
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# --- 3. أوامر Slash (تظهر عند كتابة / وتكمل نفسها) ---

@bot.tree.command(name="time", description="يظهر لك عمر حسابك ومدة تواجدك بالسيرفر")
async def time_slash(interaction: discord.Interaction):
    member = interaction.user
    joined = member.joined_at.strftime("%Y/%m/%d")
    created = member.created_at.strftime("%Y/%m/%d")
    embed = discord.Embed(title="👤 معلومات الوقت", color=0x3498db)
    embed.add_field(name="📅 انضممت للسيرفر في", value=joined, inline=True)
    embed.add_field(name="🚀 أنشأت حسابك في", value=created, inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear10", description="حذف آخر 10 رسائل من القناة")
async def clear10_slash(interaction: discord.Interaction):
    has_role = any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)
    if has_role:
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=10)
        await interaction.followup.send("🧹 تم حذف 10 رسائل بنجاح!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ عذراً، هذا الأمر مخصص للإدارة فقط.", ephemeral=True)

# --- 4. أوامر المساعدة المخصصة ---
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="📋 قائمة الأوامر", color=discord.Color.blue())
    embed.add_field(name="-info", value="يظهر معلومات السيرفر المنسقة", inline=True)
    embed.add_field(name="-time", value="يظهر معلومات وقتك", inline=True)
    embed.add_field(name="-clear10", value="حذف 10 رسائل (للإدارة)", inline=True)
    embed.set_footer(text="يمكنك أيضاً كتابة / لتجربة الأوامر السريعة")
    await ctx.send(embed=embed)

# تشغيل البوت والويب
if __name__ == "__main__":
    Thread(target=run).start()
    token = os.environ.get('TOKEN')
    bot.run(token)import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# --- إعداد سيرفر الويب لضمان الاستمرارية ---
app = Flask('')
@app.route('/')
def home(): return "TEST NETWORK is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت الأساسية ---
intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self):
        # البادئة هي "-" للأوامر العادية
        super().__init__(command_prefix="-", intents=intents, help_command=None)

    async def setup_hook(self):
        # مزامنة أوامر الـ Slash لتظهر في القائمة عند كتابة /
        await self.tree.sync()
        print(f"✅ Synced Slash Commands for {self.user}")

bot = MyBot()

# --- الآيديات الخاصة بك ---
WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'🚀 {bot.user.name} جاهز للعمل!')
    await bot.change_presence(activity=discord.Game(name="/help | -info"))

# --- 1. نظام الترحيب المنسق (Embed) ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: print("Error giving role")

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="✨ عضو جديد انضم إلينا!",
            description=f"أهلاً بك {member.mention} في سيرفرنا المتواضع.\nيسعدنا انضمامك إلينا!",
            color=0x2ecc71, # لون أخضر
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="TEST NETWORK System")
        await channel.send(embed=embed)

# --- 2. أمر -info المنسق (مربع ذهبي) ---
@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
        title="🛠 𝐒𝐄𝐑𝐕𝐄𝐑 𝐃𝐈𝐒𝐂𝐎𝐕𝐄𝐑𝐘 | 𝐓𝐄𝐒𝐓 𝐄𝐍𝐕𝐈𝐑𝐎𝐍𝐌𝐄𝐍𝐓",
        color=0xf1c40f, # لون ذهبي
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
    
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# --- 3. أوامر Slash (تظهر عند كتابة / وتكمل نفسها) ---

@bot.tree.command(name="time", description="يظهر لك عمر حسابك ومدة تواجدك بالسيرفر")
async def time_slash(interaction: discord.Interaction):
    member = interaction.user
    joined = member.joined_at.strftime("%Y/%m/%d")
    created = member.created_at.strftime("%Y/%m/%d")
    embed = discord.Embed(title="👤 معلومات الوقت", color=0x3498db)
    embed.add_field(name="📅 انضممت للسيرفر في", value=joined, inline=True)
    embed.add_field(name="🚀 أنشأت حسابك في", value=created, inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear10", description="حذف آخر 10 رسائل من القناة")
async def clear10_slash(interaction: discord.Interaction):
    has_role = any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)
    if has_role:
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=10)
        await interaction.followup.send("🧹 تم حذف 10 رسائل بنجاح!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ عذراً، هذا الأمر مخصص للإدارة فقط.", ephemeral=True)

# --- 4. أوامر المساعدة المخصصة ---
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="📋 قائمة الأوامر", color=discord.Color.blue())
    embed.add_field(name="-info", value="يظهر معلومات السيرفر المنسقة", inline=True)
    embed.add_field(name="-time", value="يظهر معلومات وقتك", inline=True)
    embed.add_field(name="-clear10", value="حذف 10 رسائل (للإدارة)", inline=True)
    embed.set_footer(text="يمكنك أيضاً كتابة / لتجربة الأوامر السريعة")
    await ctx.send(embed=embed)

# تشغيل البوت والويب
if __name__ == "__main__":
    Thread(target=run).start()
    token = os.environ.get('TOKEN')
    bot.run(token)
