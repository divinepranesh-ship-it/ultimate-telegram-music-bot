from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio

async def stream(call, chat_id, file):

    await call.join_group_call(
        chat_id,
        InputAudioStream(file, HighQualityAudio())
    )
