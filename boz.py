import discord
from discord.ext import commands
import os
import gdown

# ใช้ intents แบบใหม่
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Google Drive URL ของไฟล์
GDRIVE_URL = "https://drive.google.com/uc?id=1lA0DA4m1TJU-KUediIHGdyEXpSvKnfBZ"  # ใส่ ID ไฟล์ของคุณ

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="g")
async def search_command(ctx, *, keyword: str):
    temp_file = "temp_drive_file.txt"
    msg = await ctx.send(f"🔍 กำลังดาวน์โหลดไฟล์และค้นหา **{keyword}** โปรดรอสักครู่...")

    # ดาวน์โหลดไฟล์จาก Google Drive
    try:
        gdown.download(GDRIVE_URL, temp_file, quiet=False)
    except Exception as e:
        await msg.edit(content=f"❌ ดาวน์โหลดไฟล์ไม่สำเร็จ: {e}")
        return

    total_matches = 0
    matched_files = 0
    results = []

    # อ่านไฟล์และค้นหา
    try:
        with open(temp_file, "r", encoding="utf-8", errors="ignore") as f:
            file_matches = 0
            for line_number, line in enumerate(f, start=1):
                if keyword.lower() in line.lower():
                    total_matches += 1
                    file_matches += 1
                    results.append(f"[บรรทัด {line_number}] {line.strip()}")
            if file_matches > 0:
                matched_files += 1
    except Exception as e:
        await msg.edit(content=f"❌ อ่านไฟล์ไม่สำเร็จ: {e}")
        return

    if total_matches == 0:
        await msg.edit(content=f"❌ ไม่พบคำว่า **{keyword}** ในไฟล์เลย")
    else:
        output_file = "search_results.txt"
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n".join(results))

        await msg.edit(content=f"🔍 พบคำว่า **{keyword}** ทั้งหมด `{total_matches}` ครั้ง")
        await ctx.send(file=discord.File(output_file))

    # ลบไฟล์ชั่วคราวหลังใช้งาน
    os.remove(temp_file)

# ใส่ Token ของคุณ
TOKEN = "MTQwODEyOTA0MDA2NTIzNzAxMg.GsgFHd.Q1gn746ybxkilNCLfhUkx7MFf0HasEbRQoY-N0"
bot.run(TOKEN)


