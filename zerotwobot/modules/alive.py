import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from zerotwobot.events import register
from zerotwobot import telethn as tbot


PHOTO = "https://telegra.ph/file/4c3a19a6a18fc8caf4cca.jpg"

@register(pattern=("/alive"))
async def awake(event):
  TEXT = f"**Kon'nichiwa [{event.sender.first_name}](tg://user?id={event.sender.id}), Boku Wa Izumi Miyamura Desu.** \n\n"
  TEXT += "❍ **𝐼'𝓂 𝒲𝑜𝓇𝓀𝒾𝓃𝑔 𝒫𝓇𝑜𝓅𝑒𝓇𝓁𝓎y** \n\n"
  TEXT += f"❍ **𝑀𝓎 𝑀𝒶𝓈𝓉𝑒𝓇 : [Hanako](https://t.me/itadorihanako_08)** \n\n"
  TEXT += f"❍ **𝐿𝒾𝒷𝓇𝒶𝓇𝓎 𝒱𝑒𝓇𝓈𝒾𝑜𝓃 :** `{telever}` \n\n"
  TEXT += f"❍ **𝒯𝑒𝓁𝑒𝓉𝒽𝑜𝓃 𝒱𝑒𝓇𝓈𝒾𝑜𝓃 :** `{tlhver}` \n\n"
  TEXT += f"❍ **𝒫𝓎𝓇𝑜𝑔𝓇𝒶𝓂 𝒱𝑒𝓇𝓈𝒾𝑜𝓃 :** `{pyrover}` \n\n"
  TEXT += "**𝒯𝒽𝒶𝓃𝓀𝓈 𝐹𝑜𝓇 𝒜𝒹𝒹𝒾𝓃𝑔 𝑀𝑒 𝐻𝑒𝓇𝑒 ❤️**"
  BUTTON = [[Button.url("ꜱᴜᴘᴘᴏʀᴛ ✉️", "https://t.me/itadori_bot_suport"), Button.url("ɴᴇᴛᴡᴏʀᴋ 📡", "https://t.me/frostxnetwork")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
