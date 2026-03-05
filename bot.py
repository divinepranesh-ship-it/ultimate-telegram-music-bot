import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, BOT_TOKEN
from utils import download_audio
from queue import add, get, pop, clear
from player import stream

app = Client("ultimate-music-bot", API_ID, API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)


@app.on_message(filters.command("start"))
async def start(_, m: Message):

    await m.reply_text(
        "🎧 Ultimate Voice Chat Music Bot\n\n"
        "Commands:\n"
        "/play <link>\n"
        "/skip\n"
        "/pause\n"
        "/resume\n"
        "/stop\n"
        "/queue"
    )


@app.on_message(filters.command("play"))
async def play(_, m: Message):

    if len(m.command) < 2:
        return await m.reply_text("Send YouTube link")

    url = m.command[1]

    msg = await m.reply_text("⬇️ Downloading")

    file = download_audio(url)

    chat_id = m.chat.id

    add(chat_id, file)

    q = get(chat_id)

    if len(q) == 1:

        await stream(call, chat_id, file)

        await msg.edit("🎶 Playing")

    else:

        await msg.edit("➕ Added to Queue")


@app.on_message(filters.command("queue"))
async def queue_cmd(_, m: Message):

    q = get(m.chat.id)

    if not q:
        return await m.reply_text("Queue empty")

    text = "🎧 Queue:\n"

    for i, song in enumerate(q, 1):
        text += f"{i}. {song}\n"

    await m.reply_text(text)


@app.on_message(filters.command("skip"))
async def skip(_, m: Message):

    chat_id = m.chat.id

    pop(chat_id)

    q = get(chat_id)

    if not q:

        await call.leave_group_call(chat_id)

        return await m.reply_text("Queue finished")

    next_song = q[0]

    await stream(call, chat_id, next_song)

    await m.reply_text("⏭ Skipped")


@app.on_message(filters.command("pause"))
async def pause(_, m: Message):

    await call.pause_stream(m.chat.id)

    await m.reply_text("⏸ Paused")


@app.on_message(filters.command("resume"))
async def resume(_, m: Message):

    await call.resume_stream(m.chat.id)

    await m.reply_text("▶️ Resumed")


@app.on_message(filters.command("stop"))
async def stop(_, m: Message):

    clear(m.chat.id)

    await call.leave_group_call(m.chat.id)

    await m.reply_text("⏹ Stopped")


async def main():

    await app.start()
    await call.start()

    print("Ultimate Music Bot Started")

    await asyncio.Event().wait()


asyncio.run(main())
