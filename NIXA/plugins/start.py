from NIXA import NIXA
from telethon import events, Button
from Config import BOT_USERNAME

@NIXA.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply("ʜᴇʟʟᴏ ɪ ᴀᴍ sᴜᴘᴇʀ ғᴀsᴛ ᴍᴜsɪᴄ ʙᴏᴛ
ᴀɴᴅ ɴᴏ ʟᴀɢ ɪssᴜᴇ ᴡɪᴛʜ ʙᴇsᴛ sᴏᴜɴᴅ ǫᴜᴀʟɪᴛʏ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs. ᴛʜɪs ᴍᴜsɪᴄ ʙᴏᴛ ʙᴀsᴇᴅ ᴏɴ ᴛᴇʟᴇᴛʜᴏɴ
 ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ sᴜᴍɪᴛ ʏᴀᴅᴀᴠ...",
                    buttons=[
                        [
                          Button.url("➕ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url="https://t.me/{BOT_USERNAME}?startgroup=true")],
                       ],
                       [
                          Button.url("• sᴜᴘᴘᴏʀᴛ •", url="https://t.me/TechQuardSupport"),
                          Button.url("• ᴜᴘᴅᴀᴛᴇs •", url="https://t.me/TechQuard")
                       ],
                       [
                          Button.url("• ᴅᴇᴠᴇʟᴏᴘᴇʀ •", url="https://t.me/Simple_Mundaa"),
                          Button.url("• ʏᴏᴜᴛᴜʙᴇ •", url="https://youtube.com/channel/UCtI7hbY-BD7wvuIzoSU0cEw")
                       ]
                       )
