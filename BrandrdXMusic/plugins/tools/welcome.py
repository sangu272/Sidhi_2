import os
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from BrandrdXMusic import LOGGER
from pyrogram.types import Message
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic import app
from BrandrdXMusic.utils.database import *

LOGGER = getLogger(__name__)


class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(500, 500)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chat, id, uname):
    background = Image.open("BrandrdXMusic/assets/wel2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize(
        (350, 450)
    ) 
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('assets/font.ttf', size=35)
    font2 = ImageFont.truetype('assets/font.ttf', size=60)
    
   
    draw.text((650, 150), f'NAME : {unidecode(user)}', fill=(212, 175, 55), font=font)
    draw.text((650, 250), f'ID : {id}', fill=(255, 153, 51), font=font)
    draw.text((650, 350), f"USERNAME : {uname}", fill=(19, 136, 8),font=font)
    pfp_position = (100, 133)  
    background.paste(pfp, pfp_position, pfp)  
    background.save(
        f"downloads/welcome#{id}.png"
    )
    return f"downloads/welcome#{id}.png"


@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "**❖ ᴜsᴀɢᴇ ➥** /swel [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ]"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
      A = await wlcm.find_one({"chat_id" : chat_id})
      state = message.text.split(None, 1)[1].strip()
      state = state.lower()
      if state == "enable":
        if A:
           return await message.reply_text("✦ Special Welcome Already Enabled")
        elif not A:
           await add_wlcm(chat_id)
           await message.reply_text(f"✦ Enabled Special Welcome in {message.chat.title}")
      elif state == "disable":
        if not A:
           return await message.reply_text("✦ Special Welcome Already Disabled")
        elif A:
           await rm_wlcm(chat_id)
           await message.reply_text(f"✦ Disabled Special Welcome in {message.chat.title}")
      else:
        await message.reply_text(usage)
    else:
        await message.reply("✦ Only Admins Can Use This Command")
 
@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    count = await app.get_chat_members_count(chat_id)
   # A = await wlcm.find_one({"chat_id" : chat_id})
   # if not A:
     #  return
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "assets/upic.png"
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        button_text = "❍ 𓆩 𝗦𝐓𝐘𝐋𝐈𝐒𝐇 ⌯ 𝗡𝐀𝐌𝐄 𓆪 ❍"
        add_button_text = "❍ 𝐏𝐑𝐎𝐌𝐎𝐓𝐈𝐎𝐍 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 ❍"
        deep_link = f"https://t.me/TG_BIO_STYLE"
        add_link = f"https://t.me/SIDHI_MUSIC/10"
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption= f"""
 •●◉✿ ᴡᴇʟᴄᴏᴍᴇ ʙᴀʙʏ ✿◉●•
▰▱▱▱▱▱▱▱▱▱▱▱▱▱▰

☉ 𝐍ᴀᴍᴇ ⧽ {user.mention}
☉ 𝐈ᴅ ⧽ `{user.id}`
☉ 𝐔_𝐍ᴀᴍᴇ ⧽ @{user.username}
☉ 𝐓ᴏᴛᴀʟ 𝐌ᴇᴍʙᴇʀs ⧽ {count}
❖ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ ๛[❤️‍🔥 • 𝛚𝛐𝛚 • ❤️‍🔥 ](https://t.me/ll_ITZ_NAWAB_HERE_ll)
▰▱▱▱▱▱▱▱▱▱▱▱▱▱▰
""",
reply_markup=InlineKeyboardMarkup([
    [InlineKeyboardButton(button_text, url=deep_link)],
    [InlineKeyboardButton(text=add_button_text, url=add_link)],
 ])
)
    except Exception as e:
        LOGGER.error(e)
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        pass


      
