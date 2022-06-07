import os

from telethon import Button, events

from NIXA import *

IMG = os.environ.get(
    "PING_PIC", "https://telegra.ph/file/ed8051b0e0a2f844b2373.jpg"
)
ms = 4

ALIVE = os.environ.get(
    "ALIVE", "@Simple_Mundaa"
)

CAPTION = f"**𝗣 𝗢 𝗡 𝗚 😂 **\n\n   » {ms}\n   » ᴍʏ ᴍᴀsᴛᴇʀ ~『{ALIVE}』"


@NIXA.on(events.NewMessage(pattern="^/ping"))
async def _(event):
    UMM = [[
             Button.url("• sᴜᴘᴘᴏʀᴛ •", url="https://t.me/TechQuardSupport"),
             Button.url("• ᴜᴘᴅᴀᴛᴇs •", url="https://t.me/TechQuard")
                       ]]
    await NIXA.send_file(event.chat_id, IMG, caption=CAPTION, buttons=UMM)
