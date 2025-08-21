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
    
    # แยกชื่อโดเมนจาก URL สำหรับการค้นหา
    search_keyword = keyword
    if keyword.startswith("http://") or keyword.startswith("https://"):
        # ตัด https:// หรือ http:// ออก
        search_keyword = keyword.replace("https://", "").replace("http://", "")
        # ตัด path ออก (เช่น /home, /api, etc.)
        if "/" in search_keyword:
            search_keyword = search_keyword.split("/")[0]
    
    # สร้าง embed สำหรับข้อความสวยงาม
    embed = discord.Embed(
        title="🔍 กำลังค้นหาข้อมูล",
        description=f"กำลังค้นหา **{search_keyword}**\n(จากคำค้นหาเดิม: {keyword})\nโปรดรอสักครู่...",
        color=0x3498db
    )
    msg = await ctx.send(embed=embed)

    # ดาวน์โหลดไฟล์จาก Google Drive
    try:
        gdown.download(GDRIVE_URL, temp_file, quiet=True)  # เปลี่ยนเป็น quiet=True
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ เกิดข้อผิดพลาด",
            description=f"ดาวน์โหลดไฟล์ไม่สำเร็จ:\n```{str(e)[:500]}```",
            color=0xe74c3c
        )
        await msg.edit(embed=error_embed)
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
                    # จำกัดความยาวบรรทัดเพื่อป้องกันข้อความล้น
                    clean_line = line.strip()
                    if len(clean_line) > 100:
                        clean_line = clean_line[:100] + "..."
                    results.append(f"[บรรทัด {line_number:,}] {clean_line}")
            if file_matches > 0:
                matched_files += 1
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ เกิดข้อผิดพลาด",
            description=f"อ่านไฟล์ไม่สำเร็จ:\n```{str(e)[:500]}```",
            color=0xe74c3c
        )
        await msg.edit(embed=error_embed)
        return

    if total_matches == 0:
        no_result_embed = discord.Embed(
            title="❌ ไม่พบผลลัพธ์",
            description=f"ไม่พบคำว่า **{keyword}** ในไฟล์",
            color=0xe67e22
        )
        await msg.edit(embed=no_result_embed)
    else:
        # ใช้ keyword เป็นชื่อไฟล์ (แทนที่อักขระพิเศษด้วย _)
        safe_keyword = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in keyword)
        output_file = f"{safe_keyword.replace(' ', '_')}.txt"
        
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(f"ผลการค้นหา: {keyword}\n")
            out.write(f"วันที่: {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n")
            out.write(f"พบทั้งหมด: {total_matches:,} ครั้ง\n")
            out.write("="*50 + "\n\n")
            out.write("\n".join(results))

        success_embed = discord.Embed(
            title="✅ ค้นหาเสร็จสิ้น",
            color=0x2ecc71
        )
        success_embed.add_field(
            name="📊 สถิติ",
            value=f"🔍 คำค้นหา: **{keyword}**\n📝 ผลลัพธ์: **{total_matches:,}** ครั้ง\n📄 ชื่อไฟล์: `{output_file}`",
            inline=False
        )
        success_embed.set_footer(text="ไฟล์ผลลัพธ์แนบมาด้วยค่ะ")
        
        await msg.edit(embed=success_embed)
        await ctx.send(file=discord.File(output_file))

    # ลบไฟล์ชั่วคราวหลังใช้งาน
    if os.path.exists(temp_file):
        os.remove(temp_file)
    if 'output_file' in locals() and os.path.exists(output_file):
        os.remove(output_file)

# ใส่ Token ของคุณ
TOKEN = "MTQwODEyOTA0MDA2NTIzNzAxMg.G9M506.QDLCfIzBGZlFBKo62kx50EjjyUHqSTBjPL_2MY"
bot.run(TOKEN)
