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
        # هذا السطر هو المسؤول عن إظهار الأوامر (/) فوراً في السيرفر
        await self.tree.sync()
        print(f"✅ Slash commands synced for {self.user}")

bot = MyBot()

WELCOME_CHANNEL_ID = 1476043469519716455
AUTO_ROLE_ID = 1476035055565410396
ALLOWED_ROLE_ID = 1476034819925217381

@bot.event
async def on_ready():
    print(f'🚀 {bot.user.name} is online and ready!')

# --- الترحيب بنظام Embed ---
@bot.event
async def on_member_join(member):
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except: pass

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="👋 New Member Joined!",
            description=f"Welcome {member.mention} to the environment.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

# --- أمر -info بنظام Embed (مربع منسق) ---
@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
        title="🛠 𝐒𝐄𝐑𝐕𝐄𝐑 𝐃𝐈𝐒𝐂𝐎𝐕𝐄𝐑𝐘 | 𝐓𝐄𝐒𝐓 𝐄𝐍𝐕𝐈𝐑𝐎𝐍𝐌𝐄𝐍𝐓",
        color=discord.Color.gold(), # لون ذهبي فخم
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
            "• **𝐁𝐞𝐭𝐚 𝐓𝐞𝐬𝐭𝐢𝐧𝐠:** 𝐒𝐭𝐫𝐞𝐬𝐬-𝐭𝐞𝐬𝐭𝐢𝐧𝐠 𝐛𝐨𝐭 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬.\n"
            "• **𝐔𝐈/𝐔𝐗 𝐃𝐞𝐬𝐢𝐠𝐧:** 𝐂𝐫𝐚𝐟𝐭𝐢𝐧𝐠 𝐄𝐦𝐛𝐞𝐝𝐬 & 𝐁𝐮𝐭𝐭𝐨𝐧𝐬.\n"
            "• **𝐃𝐞𝐛𝐮𝐠𝐠𝐢𝐧𝐠:** 𝐅𝐢𝐱𝐢𝐧𝐠 𝐀𝐏𝐈 𝐢𝐬𝐬𝐮𝐞𝐬.\n"
            "• **𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐌𝐚𝐩𝐩𝐢𝐧𝐠:** 𝐓𝐞𝐬𝐭𝐢𝐧𝐠 𝐫𝐨𝐥𝐞 𝐡𝐢𝐞𝐫𝐚𝐫𝐜𝐡𝐢𝐞𝐬."
        ), 
        inline=False
    )
    
    embed.set_footer(text="System Information Request", icon_url=bot.user.display_avatar.url)
    await ctx.send(embed=embed)

# --- أوامر Slash التي تظهر تلقائياً بمجرد كتابة / ---

@bot.tree.command(name="time", description="عرض مدة انضمامك للسيرفر وعمر حسابك")
async def time_slash(interaction: discord.Interaction):
    member = interaction.user
    joined = member.joined_at.strftime("%Y/%m/%d")
    created = member.created_at.strftime("%Y/%m/%d")
    embed = discord.Embed(title="👤 معلومات المستخدم", color=discord.Color.blue())
    embed.add_field(name="📅 انضم للسيرفر", value=joined, inline=True)
    embed.add_field(name="🚀 إنشاء الحساب", value=created, inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear10", description="حذف آخر 10 رسائل")
async def clear10_slash(interaction: discord.Interaction):
    has_role = any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)
    if has_role:
        await interaction.response.defer(ephemeral=True) # يمنع الخطأ إذا تأخر الحذف
        await interaction.channel.purge(limit=10)
        await interaction.followup.send("🧹 تم حذف 10 رسائل بنجاح.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ ليس لديك صلاحية (الرتبة المطلوبة مفقودة).", ephemeral=True)

@bot.tree.command(name="clearall", description="تنظيف الشات بالكامل (آخر 100 رسالة)")
async def clearall_slash(interaction: discord.Interaction):
    has_role = any(role.id == ALLOWED_ROLE_ID for role in interaction.user.roles)
    if has_role:
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=100)
        await interaction.followup.send(f"🗑️ تم تنظيف {len(deleted)} رسالة.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ لا تمتلك صلاحية لهذه العملية.", ephemeral=True)

# دعم الأوامر اليدوية (-clear10 و /clearall كرسالة عادية)
@bot.event
async def on_message(message):
    if message.author.bot: return
    
    has_role = any(role.id == ALLOWED_ROLE_ID for role in message.author.roles)
    
    if message.content == "-clear10" and has_role:
        await message.channel.purge(limit=11)
        await message.channel.send("🧹 Deleted 10 messages.", delete_after=5)
    
    if message.content == "/clearall" and has_role:
        await message.channel.purge(limit=100)
        await message.channel.send("🗑️ Channel cleared.", delete_after=5)

    await bot.process_commands(message)

# تشغيل
if __name__ == "__main__":
    Thread(target=run).start()
    bot.run(os.environ.get('TOKEN'))
