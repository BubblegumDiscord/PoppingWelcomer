import config
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO, StringIO
import discord, aiohttp, datetime

bot = commands.Bot(command_prefix="-", description="Give new members a bubbly start to their experience!")


def tint_image(image, tint_color):
    return ImageChops.multiply(image, Image.new('RGBA', image.size, tint_color))

def tag(u):
    return u.name + "#" + u.discriminator

@bot.event
async def on_ready():
    print("Logged in")
    print(bot.user.name)
    print(bot.user.id)
    print("--------")

@bot.command(pass_context=True)
async def dump(ctx, *, vc:discord.Channel):
    if str(vc.type) != "voice":
        print(type(vc.type))
        return await bot.say("Please provide a voice channel, not a text channel.")
    
    mems = [m for m in vc.server.members if m.voice.voice_channel == vc ]
    await bot.send_message(ctx.message.channel, embed=discord.Embed(
        title=":book: Members currently in " + vc.name,
        description="```" + "".join([tag(m) + "\n" for m in mems]) + "```",
        colour=0x0a96de,
        timestamp=datetime.datetime.now()
    ))

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

    tx, ty = draw.textsize(text, font=font)

    x = 250 - tx//2
    y = round(158 * 1.8) - ty//2
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
    


    avatar_im = None
    url = mem.avatar_url
    if not url:
        url = mem.default_avatar_url

    while True:
        async with aiohttp.ClientSession(loop=bot.loop) as aiosession:
            with aiohttp.Timeout(10):
                async with aiosession.get(url) as resp:
                    avatar_im = BytesIO(await resp.read())
                    if avatar_im.getbuffer().nbytes > 0 or retries == 0:
                        await aiosession.close()
                        break
                    retries -= 1
                    print('0 nbytes image found. Retries left: {}'.format(retries+1))

    ava_sqdim = 78
    resize = (ava_sqdim, ava_sqdim)
    avatar_im = Image.open(avatar_im).convert("RGBA")
    avatar_im = avatar_im.resize(resize, Image.ANTIALIAS)
    avatar_im.putalpha(avatar_im.split()[3])

    is_square = False
    if not is_square:
        mask = Image.new('L', resize, 0)
        maskDraw = ImageDraw.Draw(mask)
        maskDraw.ellipse((0, 0) + resize, fill=255)
        mask = mask.resize(avatar_im.size, Image.ANTIALIAS)
        avatar_im.putalpha(mask)
        
    img_center_x = (im.width // 2)
    img_center_y = (im.height // 2)

    offset_x = 109
    offset_y = 36

    img_offset_x = img_center_x + offset_x
    img_offset_y = img_center_y + offset_y
    ava_right = img_offset_x + avatar_im.width//2
    ava_bottom = img_offset_y + avatar_im.height//2
    ava_left = img_offset_x - avatar_im.width//2
    ava_top = img_offset_y - avatar_im.height//2
    avatar_im = tint_image(avatar_im, (255, 255, 255, 80))
    im.paste(avatar_im, box=(ava_left, ava_top, ava_right, ava_bottom), mask=avatar_im)





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

    tx, ty = draw.textsize(text, font=font)

    x = 250 - tx//2
    y = round(158 * 1.8) - ty//2
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
    avatar_im = None
    url = mem.avatar_url
    if not url:
        url = mem.default_avatar_url

    while True:
        async with aiohttp.ClientSession(loop=bot.loop) as aiosession:
            with aiohttp.Timeout(10):
                async with aiosession.get(url) as resp:
                    avatar_im = BytesIO(await resp.read())
                    if avatar_im.getbuffer().nbytes > 0 or retries == 0:
                        await aiosession.close()
                        break
                    retries -= 1
                    print('0 nbytes image found. Retries left: {}'.format(retries+1))

    ava_sqdim = 78
    resize = (ava_sqdim, ava_sqdim)
    avatar_im = Image.open(avatar_im).convert("RGBA")
    avatar_im = avatar_im.resize(resize, Image.ANTIALIAS)
    avatar_im.putalpha(avatar_im.split()[3])

    is_square = False
    if not is_square:
        mask = Image.new('L', resize, 0)
        maskDraw = ImageDraw.Draw(mask)
        maskDraw.ellipse((0, 0) + resize, fill=255)
        mask = mask.resize(avatar_im.size, Image.ANTIALIAS)
        avatar_im.putalpha(mask)
        
    img_center_x = (im.width // 2)
    img_center_y = (im.height // 2)

    offset_x = 109
    offset_y = 36

    img_offset_x = img_center_x + offset_x
    img_offset_y = img_center_y + offset_y
    ava_right = img_offset_x + avatar_im.width//2
    ava_bottom = img_offset_y + avatar_im.height//2
    ava_left = img_offset_x - avatar_im.width//2
    ava_top = img_offset_y - avatar_im.height//2
    avatar_im = tint_image(avatar_im, (255, 255, 255, 80))
    im.paste(avatar_im, box=(ava_left, ava_top, ava_right, ava_bottom), mask=avatar_im)


    temp = BytesIO()
    im.save(temp, format="png")
    #im.show()
    temp.seek(0)
    await bot.upload(temp, content="Give a popping welcome to " + mem.display_name + " :candy:", filename="welcome.png")


bot.run(config.token)
