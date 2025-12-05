import os
import random
import re
import string

import lyricsgenius as lg
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from SANYAMUSIC import app
from SANYAMUSIC.utils.decorators.language import language

from config import BANNED_USERS, lyrical

# --- MODIFIED SECTION ---

# Use os.getenv() to securely retrieve the API key from the environment.
api_key = os.getenv("GENIUS_ACCESS_TOKEN")

# Add a check to ensure the key is present
if not api_key:
    # Raise an error to prevent the app from starting with a hardcoded or missing key
    raise ValueError("GENIUS_ACCESS_TOKEN environment variable not set. Please set your Genius API key.")

y = lg.Genius(
    api_key,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
)
y.verbose = False

# --- END MODIFIED SECTION ---

@app.on_message(filters.command(["lyrics"]) & ~BANNED_USERS)
async def lrsearch(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(_["lyrics_1"])

    title = message.text.split(None, 1)[1]
    m = await message.reply_text(_["lyrics_2"])
    
    S = y.search_song(title, get_full_info=False)
    if S is None:
        return await m.edit(_["lyrics_3"].format(title))

    ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    lyric = S.lyrics
    if "Embed" in lyric:
        lyric = re.sub(r"\d*Embed", "", lyric)
    lyrical[ran_hash] = lyric

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["L_B_1"],
                    url=f"https://t.me/{app.username}?start=lyrics_{ran_hash}",
                ),
            ]
        ]
    )
    
    await m.edit(_["lyrics_4"], reply_markup=upl)
