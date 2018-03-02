import config
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO, StringIO
import discord

bot = commands.Bot(command_prefix="-", description="Give new members a bubbly start to their experience!")

@bot.event
async def on_ready():
    print("Logged in")
    print(bot.user.name)
    print(bot.user.id)
    print("--------")

@bot.event
async def on_member_join(mem):
    im = Image.open("./banner2.png")
    
    draw = ImageDraw.Draw(im, mode='RGBA')
    
    text = mem.display_name
    fsiz = 48
    font=ImageFont.truetype("./Starfish.ttf", fsiz)
    while draw.textsize(text, font=font)[0] > 430:
        fsiz -= 1
        font=ImageFont.truetype("./Starfish.ttf", fsiz)

    
    x = round(37 * 1.25)
    y = round(158 * 1.6)
    #shadowcolor = (100, 100, 100)
    #shadowcolor = (255,255,255)
    fillcolor = (165, 214, 254)
    shadowcolor = (105, 154, 194)
    a = "center"
    draw.text((x-1, y-1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x+1, y+1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x+1, y-1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x-1, y+1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x, y), text, font=font, fill=fillcolor, align=a)
    
    temp = BytesIO()
    im.save(temp, format="png")
    temp.seek(0)
    await bot.send_file(mem.server.default_channel ,temp, content="Give a popping welcome to " + mem.display_name + " :candy:", filename="welcome.png")

@bot.command(pass_context=True)
async def whalecum(ctx, mem: discord.Member = None):
    mem = mem if mem else ctx.message.author
    im = Image.open("./banner2.png")
    
    draw = ImageDraw.Draw(im, mode='RGBA')
    
    text = mem.display_name
    fsiz = 48
    font=ImageFont.truetype("./Starfish.ttf", fsiz)
    while draw.textsize(text, font=font)[0] > 430:
        fsiz -= 1
        font=ImageFont.truetype("./Starfish.ttf", fsiz)

    
    x = round(37 * 1.25)
    y = round(158 * 1.6)
    #shadowcolor = (100, 100, 100)
    #shadowcolor = (255,255,255)
    fillcolor = (165, 214, 254)
    shadowcolor = (105, 154, 194)
    a = "center"
    draw.text((x-1, y-1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x+1, y+1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x+1, y-1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x-1, y+1), text, font=font, fill=shadowcolor, align=a)
    draw.text((x, y), text, font=font, fill=fillcolor, align=a)
    
    temp = BytesIO()
    im.save(temp, format="png")
    temp.seek(0)
    await bot.upload(temp, content="Test", filename="welcome.png")


bot.run(config.token)