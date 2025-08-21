import discord
from discord.ext import commands
import os

# ใช้ intents แบบใหม่
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="g")  # เปลี่ยนชื่อคำสั่งเป็น !g
async def search_command(ctx, *, keyword: str):
    base_path = r"C:\Users\4444444\Desktop\g\Rov\all"  # ตำแหน่งโฟลเดอร์ไฟล์
    total_matches = 0
    matched_files = 0
    results = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".txt"):  # เฉพาะไฟล์ .txt
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_matches = 0
                    for line_number, line in enumerate(f, start=1):
                        if keyword.lower() in line.lower():
                            total_matches += 1
                            file_matches += 1
                            results.append(f"{file} [บรรทัด {line_number}] {line.strip()}")
                    if file_matches > 0:
                        matched_files += 1

    if total_matches == 0:
        await ctx.send(f"❌ ไม่พบคำว่า **{keyword}** ในไฟล์ใดเลย")
    else:
        await ctx.send(
            f"🔍 พบคำว่า **{keyword}** ทั้งหมด `{total_matches}` ครั้ง "
            f"ใน `{matched_files}` ไฟล์"
        )

        # บันทึกผลลัพธ์ลงไฟล์
        output_file = os.path.join(base_path, "search_results.txt")
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n".join(results))

        await ctx.send(file=discord.File(output_file))

TOKEN = os.getenv("DISCORD_BOT_TOKEN") or "ใส่โทเคนตรงนี้"
bot.run(TOKEN)
