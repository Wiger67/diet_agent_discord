import os
from typing import Literal  

import discord
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = discord.Object(id=int(os.getenv("DISCORD_GUILD_ID")))

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)   # 管理所有 slash command

#/ping
@tree.command(description="測試 bot 有沒有活著", guild=GUILD) 
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Ciallo～(∠・ω< )⌒☆")

#/basic_info
@tree.command(description="輸入基本資料",guild=GUILD) 
@app_commands.describe(
    age="年齡",
    height_cm="身高(cm)",
    weight_kg="體重(kg)",
    sex = "性別",
    activity = "運動習慣",
    goal = "目標",
)
async def basic_info(
    interaction: discord.Interaction,
    age:app_commands.Range[int,5,100],
    height_cm:app_commands.Range[float,100,250],
    weight_kg:app_commands.Range[float,30,300],
    sex:Literal["男","女"],
    activity:Literal["久坐", "輕度", "中度", "高度", "非常高"],
    goal:Literal["減脂", "維持", "增肌","增肌減脂"],
    ):
    user = interaction.user
    await interaction.response.send_message(
        f"收到了以下資訊:\n"
        f"{user} {sex}性{age}歲，身高體重為{height_cm}cm/{weight_kg}kg。\n"
        f"運動習慣為{activity}，目標是{goal}",
        ephemeral=True
        )

# /meal
@tree.command(description="傳送實物照片，分析熱量", guild=GUILD)
async def meal(
    interaction: discord.Interaction,
    photo: discord.Attachment,
    note: str = ""
    ):
    await interaction.response.defer(thinking=True) #
    content_type = photo.content_type or ""
    if not content_type.startswith("image/"):
        await interaction.followup.send("請傳圖片檔（JPG、PNG 等）。")
        return

    image_bytes = await photo.read()

    await interaction.followup.send(
        f"收到圖片：{photo.filename}（{content_type}，{len(image_bytes)} bytes）\n"
        f"說明：{note or '（沒有填）'}"
    )


@client.event
async def on_ready():
    # 只同步指令到指定的伺服器，並非全域，所有的指令都要加上"guild=GUILD"才會被讀取。
    # 好處是這樣可以快速測試
    await tree.sync(guild=GUILD) 
    print(f"已登入：{client.user}")


client.run(TOKEN)