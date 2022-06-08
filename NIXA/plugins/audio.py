from pytgcalls import StreamType
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from pytgcalls.exceptions import (
    NoActiveGroupCall,
    NotInGroupCallError
)
from NIXA.status import *
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
import telethon.utils
from telethon.tl import functions
from telethon.tl import types
from telethon.utils import get_display_name
from telethon.tl.functions.users import GetFullUserRequest
from youtubesearchpython import VideosSearch

 
fotoplay = "https://telegra.ph/file/987e34d64fdc702689e81.jpg"
ngantri = "https://telegra.ph/file/987e34d64fdc702689e81.jpg"
from NIXA import call_py, NIXA, client as Client
owner = "5576613955, 5417532619"
from NIXA.helpers.yt_dlp import bash
from NIXA.helpers.chattitle import CHAT_TITLE
from NIXA.helpers.queues import (
    QUEUE,
    add_to_queue,
    clear_queue,
    get_queue,
    pop_an_item,
)
from telethon import Button, events

from NIXA.helpers.thumbnail import gen_thumb


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


async def skip_item(chat_id: int, x: int):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    try:
        songname = chat_queue[x][0]
        chat_queue.pop(x)
        return songname
    except Exception as e:
        print(e)
        return 0


async def skip_current_song(chat_id: int):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    if len(chat_queue) == 1:
        await call_py.leave_group_call(chat_id)
        clear_queue(chat_id)
        return 1
    songname = chat_queue[1][0]
    url = chat_queue[1][1]
    link = chat_queue[1][2]
    type = chat_queue[1][3]
    RESOLUSI = chat_queue[1][4]
    if type == "Audio":
        await call_py.change_stream(
            chat_id,
            AudioPiped(
                url,
            ),
        )
    elif type == "Video":
        if RESOLUSI == 720:
            hm = HighQualityVideo()
        elif RESOLUSI == 480:
            hm = MediumQualityVideo()
        elif RESOLUSI == 360:
            hm = LowQualityVideo()
        await call_py.change_stream(
            chat_id, AudioVideoPiped(url, HighQualityAudio(), hm)
        )
    pop_an_item(chat_id)
    return [songname, link, type]


@NIXA.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):

     await event.delete()

btnn =[
    [Button.url("• sᴜᴘᴘᴏʀᴛ •", url="https://t.me/TechQuardSupport"), Button.url("• ᴜᴘᴅᴀᴛᴇs •", url="https://t.me/TechQuard")],
    [Button.inline("» ᴄʟᴏsᴇ «", data="cls")]]


#play
@NIXA.on(events.NewMessage(pattern="^/play"))
async def play(event):
    title = ' '.join(event.text[5:])
    replied = await event.get_reply_message()
    sender = await event.get_sender()
    chat = await event.get_chat()
    chat_id = event.chat_id
    from_user = vcmention(event.sender) 
    public = event.chat_id
    if (
        replied
        and not replied.audio
        and not replied.voice
        and not title
        or not replied
        and not title
    ):
        return await event.reply("**» ɢɪᴠᴇ ᴍᴇ ʏᴏᴜʀ ǫᴜᴇʀʏ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ...**")
    elif replied and not replied.audio and not replied.voice or not replied:
        botman = await event.reply("`ᴘʀᴏᴄᴇssɪɴɢ...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        if search == 0:
            await botman.edit(
                "**ᴄᴀɴ'ᴛ ғɪɴᴅ sᴏɴɢ** ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ ᴍᴏʀᴇ sᴘᴇᴄɪғɪᴄ ᴛɪᴛʟᴇ..."
            ) 
    if event.is_group:
        try:
            await Client(functions.channels.JoinChannelRequest(channel=public))
        except Exception as e:
            print(e)
            pass    
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            userid = sender.id
            titlegc = chat.title
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, userid, ctitle)
            format = "best[height<=?720][width<=?1280]"
            hm, ytlink = await ytdl(format, url)
            if hm == 0:
                await botman.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                caption = f"» **sᴏɴɢ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ »** `#{pos}`\n\n**🏷 ɴᴀᴍᴇ:** [{songname}]({url})\n**⏱ ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛᴇʀ:** {from_user}"
                await botman.delete()
                await event.client.send_file(chat_id, thumb, caption=caption, buttons=btnn)
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            ytlink,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                    caption = f"🏷 **ɴᴀᴍᴇ:** [{songname}]({url})\n**⏱ ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n📹 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇǫᴜᴇsᴛᴇʀ:** {from_user}"
                    await botman.delete()
                    await event.client.send_file(chat_id, thumb, caption=caption, buttons=btnn)
                except Exception as ep:
                    clear_queue(chat_id)
                    await botman.edit(f"`{ep}`")

    else:
        botman = await edit_or_reply(event, "📥 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if replied.audio:
            songname = "NixaMusicBot"
        elif replied.voice:
            songname = "Voice Note"
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
            caption = f"» **sᴏɴɢ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ »** `#{pos}`\n\n**🏷 ᴛɪᴛʟᴇ:** [{songname}]({link})\n**👥 ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`\n🎧 **ʀᴇǫᴜᴇsᴛᴇʀ:** {from_user}"
            await event.client.send_file(chat_id, ngantri, caption=caption, buttons=btnn)
            await botman.delete()
        else:
            try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                caption = f"🏷 **ᴛɪᴛʟᴇ:** [{songname}]({link})\n**👥 ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`\n📹 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇǫᴜᴇsᴛᴇʀ:** {from_user}"
                await event.client.send_file(chat_id, fotoplay, caption=caption, buttons=btnn)
                await botman.delete()
            except Exception as ep:
                clear_queue(chat_id)
                await botman.edit(f"`{ep}`")





#end
@NIXA.on(events.NewMessage(pattern="^/end"))
@is_admin
async def vc_end(event, perm):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await event.reply("**» sᴛʀᴇᴀᴍɪɴɢ ᴇɴᴅ....**")
        except Exception as e:
            await event.reply(f"**ᴇʀʀᴏʀ:** `{e}`")
    else:
        await event.reply("**» ɴᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ...**")





@NIXA.on(events.NewMessage(pattern="^/vplay"))
async def vplay(event):
    title = ' '.join(event.text[6:])
    replied = await event.get_reply_message()
    sender = await event.get_sender()
    userid = sender.id
    chat = await event.get_chat()
    titlegc = chat.title
    chat_id = event.chat_id
    public = event.chat_id
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.video
        and not replied.document
        and not title
        or not replied
        and not title
    ):
        return await event.reply("**» ɢɪᴠᴇ ᴍᴇ ʏᴏᴜʀ ǫᴜᴇʀʏ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛʀᴇᴀᴍ...**")
    if replied and not replied.video and not replied.document:
        xnxx = await event.reply("`sᴇᴀʀᴄʜɪɴɢ...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit(
                "**» ɢɪᴠᴇ ᴍᴇ ᴠᴀʟɪᴅ ɪɴᴘᴜᴛs...**"
            )
        else:
            query = event.text.split(maxsplit=1)[1]
            search = ytsearch(query)
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, userid, ctitle)
            format = "best[height<=?720][width<=?1280]"
            hm, ytlink = await ytdl(format, url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(
                    chat_id, songname, ytlink, url, "Video", RESOLUSI)
                caption = f"» **ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍɪɴɢ ɪɴ ǫᴜᴇᴜᴇ »** `#{pos}`\n\n**🏷 ᴛɪᴛʟᴇ:** [{songname}]({url})\n**⏱ ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛᴇᴅ:** {from_user}"
                await xnxx.delete()
                await event.client.send_file(chat_id, thumb, caption=caption, buttons=btnn)
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(
                        chat_id,
                        songname,
                        ytlink,
                        url,
                        "Video",
                        RESOLUSI)
                    await xnxx.delete()
                    await event.client.send_file(event.chat_id,
                        f"**🏷 **__ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍɪɴɢ sᴛᴀʀᴛᴇᴅ__**:** [{songname}]({url})\n**⏱ ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n📹 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇǫᴜᴇsᴛᴇᴅ:** {from_user}, buttons=btnn",
                        link_preview=False,
                    )
                except Exception as ep:
                    clear_queue(chat_id)
                    await xnxx.edit(f"`{ep}`")

    elif replied:
        xnxx = await event.reply("📥 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if len(event.text.split()) < 2:
            RESOLUSI = 720
        else:
            pq = event.text.split(maxsplit=1)[1]
            RESOLUSI = int(pq)
        if replied.video or replied.document:
            songname = "NixaMusicBot"
        if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
            caption = f"» **ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍɪɴɢ sᴛᴀʀᴛᴇᴅ »** `#{pos}`\n\n**🏷 ᴛɪᴛʟᴇ:** [{songname}]({link})\n**👥 ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`\n🎧 **ʀᴇǫᴜᴇsᴛᴇᴅ:** {from_user}"
            await event.client.send_file(chat_id, ngantri, caption=caption, buttons=btnn)
            await xnxx.delete()
        else:
            if RESOLUSI == 360:
                hmmm = LowQualityVideo()
            elif RESOLUSI == 480:
                hmmm = MediumQualityVideo()
            elif RESOLUSI == 720:
                hmmm = HighQualityVideo()
            try:
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", RESOLUSI)
                caption = f"🏷 **ᴛɪᴛʟᴇ:** [{songname}]({link})\n**👥 ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`\n📹 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇǫᴜᴇsᴛᴇᴅ:** {from_user}"
                await xnxx.delete()
                await event.client.send_file(chat_id, fotoplay, caption=caption, buttons=btnn)
            except Exception as ep:
                clear_queue(chat_id)
                await xnxx.edit(f"`{ep}`")
    else:
        xnxx = await event.reply("`sᴇᴀʀᴄʜɪɴɢ...`")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        RESOLUSI = 720
        hmmm = HighQualityVideo()
        if search == 0:
            await xnxx.edit("**ᴜɴᴀʙʟᴇ ғᴇᴀᴛᴄʜ ʏᴏᴜʀ ǫᴜᴇʀʏ...**")
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            thumbnail = search[3]
            ctitle = await CHAT_TITLE(titlegc)
            thumb = await gen_thumb(thumbnail, title, userid, ctitle)
            format = "best[height<=?720][width<=?1280]"
            hm, ytlink = await ytdl(format, url)
            if hm == 0:
                await xnxx.edit(f"`{ytlink}`")
            elif chat_id in QUEUE:
                pos = add_to_queue(
                    chat_id, songname, ytlink, url, "Video", RESOLUSI)
                caption = f"» **ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍɪɴɢ ᴀᴅᴅᴇᴅ ɪɴ ǫᴜᴇᴜᴇ »** `#{pos}`\n\n🏷 **ᴛɪᴛʟᴇ:** [{songname}]({url})\n**⏱ ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛᴇᴅ:** {from_user}"
                await xnxx.delete()
                await event.client.send_file(chat_id, thumb, caption=caption, buttons=btnn)
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(
                        chat_id,
                        songname,
                        ytlink,
                        url,
                        "Video",
                        RESOLUSI)
                    caption = f"🏷 **ᴛɪᴛʟᴇ:** [{songname}]({url})\n**⏱ ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n📹 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`\n🎧 **ʀᴇǫᴜᴇsᴛᴇᴅ:** {from_user}"
                    await xnxx.delete()
                    await event.client.send_file(chat_id, thumb, caption=caption, buttons=btnn)
                except Exception as ep:
                    clear_queue(chat_id)
                    await xnxx.edit(f"`{ep}`")




#playlist
@NIXA.on(events.NewMessage(pattern="^/playlist"))
@is_admin
async def vc_playlist(event, perm):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await event.reply(
                f"**» ᴘʟᴀʏʟɪsᴛ:**\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                link_preview=False,
            )
        else:
            PLAYLIST = f"**🎧 ᴘʟᴀʏʟɪsᴛ:**\n**• [{chat_queue[0][0]}]({chat_queue[0][2]})** | `{chat_queue[0][3]}` \n\n**• ᴜᴘᴄᴏᴍɪɴɢ sᴛʀᴇᴀᴍɪɴɢ:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                PLAYLIST = PLAYLIST + "\n" + \
                    f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
            await event.reply(PLAYLIST, link_preview=False)
    else:
        await event.reply("**» ɴᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ...**")






#leavevc
@NIXA.on(events.NewMessage(pattern="^/leavevc"))
@is_admin
async def leavevc(event, perm):
    xnxx = await event.reply("ᴘʀᴏᴄᴇssɪɴɢ...")
    chat_id = event.chat_id
    from_user = vcmention(event.sender)
    if from_user:
        try:
            await call_py.leave_group_call(chat_id)
        except (NotInGroupCallError, NoActiveGroupCall):
            pass
        await xnxx.edit("**» ʟᴇғᴛ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ** `{}`".format(str(event.chat_id)))
    else:
        await xnxx.edit(f"**» sᴏʀʀʏ {owner} ɴᴏᴛ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.**")



@NIXA.on(events.NewMessage(pattern="^/skip"))
@is_admin
async def vc_skip(event, perm):
    chat_id = event.chat_id
    if len(event.text.split()) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await event.reply("**» ɴᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ**")
        elif op == 1:
            await event.reply("» ᴇᴍᴘᴛʏ ǫᴜᴇᴜᴇ, ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ", 10)
        else:
            await event.reply(
                f"**⏭ sᴋɪᴘᴘᴇᴅ**\n**🎧 ɴᴏᴡ ᴘʟᴀʏɪɴɢ** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = event.text.split(maxsplit=1)[1]
        DELQUE = "**» ʀᴇᴍᴏᴠɪɴɢ ғᴏʟʟᴏᴡɪɴɢ sᴏɴɢs ғʀᴏᴍ ǫᴜᴇᴜᴇ:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await skip_item(chat_id, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await event.reply(DELQUE)


@NIXA.on(events.NewMessage(pattern="^/pause"))
@is_admin
async def vc_pause(event, perm):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await event.reply("**» sᴛʀᴇᴀᴍɪɴɢ ᴘᴀᴜsᴇᴅ...**")
        except Exception as e:
            await event.reply(f"**ᴇʀʀᴏʀ:** `{e}`")
    else:
        await event.reply("**» ɴᴏᴛʜᴏɴɢ ɪs ᴘʟᴀʏɪɴɢ**")



@NIXA.on(events.NewMessage(pattern="^/resume"))
@is_admin
async def vc_resume(event, perm):
    chat_id = event.chat_id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await event.reply(event, "**» sᴛʀᴇᴀᴍɪɴɢ sᴛᴀʀᴛᴇᴅ...**")
        except Exception as e:
            await event.reply(event, f"**ᴇʀʀᴏʀ:** `{e}`")
    else:
        await event.reply(event, "**» ɴᴏᴛʜɪɴɢ ɪs sᴛʀᴇᴀᴍɪɴɢ...**")


@call_py.on_stream_end()
async def stream_end_handler(_, u: Update):
    chat_id = u.chat_id
    print(chat_id)
    await skip_current_song(chat_id)


@call_py.on_closed_voice_chat()
async def closedvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_left()
async def leftvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


@call_py.on_kicked()
async def kickedvc(_, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)

