import html
import re
import os
import requests

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events

from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_html

from zerotwobot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    MEMBERS,
    INFOPIC,
    dispatcher,
    sw,
)
from zerotwobot.__main__ import STATS, TOKEN, USER_INFO
import zerotwobot.modules.sql.userinfo_sql as sql
from zerotwobot.modules.disable import DisableAbleCommandHandler
from zerotwobot.modules.sql.global_bans_sql import is_user_gbanned
from zerotwobot.modules.sql.afk_sql import is_afk, check_afk_status
from zerotwobot.modules.sql.users_sql import get_user_num_chats
from zerotwobot.modules.helper_funcs.chat_status import sudo_plus
from zerotwobot.modules.helper_funcs.extraction import extract_user
from zerotwobot import telethn as ZerotwoTelethonClient


def no_by_per(totalhp, percentage):
    """
    rtype: num of `percentage` from total
    eg: 1000, 10 -> 10% of 1000 (100)
    """
    return totalhp * percentage / 100


def get_percentage(totalhp, earnedhp):
    """
    rtype: percentage of `totalhp` num
    eg: (1000, 100) will return 10%
    """

    matched_less = totalhp - earnedhp
    per_of_totalhp = 100 - matched_less * 100.0 / totalhp
    per_of_totalhp = str(int(per_of_totalhp))
    return per_of_totalhp


def hpmanager(user):
    total_hp = (get_user_num_chats(user.id) + 10) * 10

    if not is_user_gbanned(user.id):

        # Assign new var `new_hp` since we need `total_hp` in
        # end to calculate percentage.
        new_hp = total_hp

        # if no username decrease 25% of hp.
        if not user.username:
            new_hp -= no_by_per(total_hp, 25)
        try:
            dispatcher.bot.get_user_profile_photos(user.id).photos[0][-1]
        except IndexError:
            # no profile photo ==> -25% of hp
            new_hp -= no_by_per(total_hp, 25)
        # if no /setme exist ==> -20% of hp
        if not sql.get_user_me_info(user.id):
            new_hp -= no_by_per(total_hp, 20)
        # if no bio exsit ==> -10% of hp
        if not sql.get_user_bio(user.id):
            new_hp -= no_by_per(total_hp, 10)

        if is_afk(user.id):
            afkst = check_afk_status(user.id)
            # if user is afk and no reason then decrease 7%
            # else if reason exist decrease 5%
            if not afkst.reason:
                new_hp -= no_by_per(total_hp, 7)
            else:
                new_hp -= no_by_per(total_hp, 5)

        # fbanned users will have (2*number of fbans) less from max HP
        # Example: if HP is 100 but user has 5 diff fbans
        # Available HP is (2*5) = 10% less than Max HP
        # So.. 10% of 100HP = 90HP

    # Commenting out fban health decrease cause it wasnt working and isnt needed ig.
    # _, fbanlist = get_user_fbanlist(user.id)
    # new_hp -= no_by_per(total_hp, 2 * len(fbanlist))

    # Bad status effects:
    # gbanned users will always have 5% HP from max HP
    # Example: If HP is 100 but gbanned
    # Available HP is 5% of 100 = 5HP

    else:
        new_hp = no_by_per(total_hp, 5)

    return {
        "earnedhp": int(new_hp),
        "totalhp": int(total_hp),
        "percentage": get_percentage(total_hp, new_hp),
    }


def make_bar(per):
    done = min(round(per / 10), 10)
    return "■" * done + "□" * (10 - done)



def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    user_id = extract_user(msg, args)

    if user_id:

        if msg.reply_to_message and msg.reply_to_message.forward_from:

            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"<b>Telegram ID:</b>,"
                f"• {html.escape(user2.first_name)} - <code>{user2.id}</code>.\n"
                f"• {html.escape(user1.first_name)} - <code>{user1.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

        else:

            user = bot.get_chat(user_id)
            msg.reply_text(
                f"{html.escape(user.first_name)}'s id is <code>{user.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

    else:

        if chat.type == "private":
            msg.reply_text(
                f"Your id is <code>{chat.id}</code>.", parse_mode=ParseMode.HTML,
            )

        else:
            msg.reply_text(
                f"This group's id is <code>{chat.id}</code>.", parse_mode=ParseMode.HTML,
            )


@ZerotwoTelethonClient.on(
    events.NewMessage(
        pattern="/ginfo ", from_users=(TIGERS or []) + (DRAGONS or []) + (DEMONS or []),
    ),
)
async def group_info(event) -> None:
    chat = event.text.split(" ", 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity, filter=ChannelParticipantsAdmins,
        )
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except:
        await event.reply(
            "Can't for some reason, maybe it is a private one or that I am banned there.",
        )
        return
    msg = f"**ID**: `{entity.id}`"
    msg += f"\n**Title**: `{entity.title}`"
    msg += f"\n**Datacenter**: `{entity.photo.dc_id}`"
    msg += f"\n**Video PFP**: `{entity.photo.has_video}`"
    msg += f"\n**Supergroup**: `{entity.megagroup}`"
    msg += f"\n**Restricted**: `{entity.restricted}`"
    msg += f"\n**Scam**: `{entity.scam}`"
    msg += f"\n**Slowmode**: `{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**Username**: {entity.username}"
    msg += "\n\n**Member Stats:**"
    msg += f"\n`Admins:` `{len(totallist)}`"
    msg += f"\n`Users`: `{totallist.total}`"
    msg += "\n\n**Admins List:**"
    for x in totallist:
        msg += f"\n• [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**Description**:\n`{ch_full.full_chat.about}`"
    await event.reply(msg)



def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"Gif ID:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("Please reply to a gif to get its ID.")



def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("𝙸 𝚌𝚊𝚗'𝚝 𝚎𝚡𝚝𝚛𝚊𝚌𝚝 𝚊 𝚞𝚜𝚎𝚛 𝚏𝚛𝚘𝚖 𝚝𝚑𝚒𝚜.")
        return

    else:
        return

    rep = message.reply_text("<code>𝙶𝚊𝚝𝚑𝚎𝚛𝚒𝚗𝚐 𝚒𝚗𝚏𝚘 𝚏𝚛𝚘𝚖 VOID...</code>", parse_mode=ParseMode.HTML)

    text = (
        f"╒═══「<b> Appraisal results:</b> 」\n"
        f" ◐ 𝙸𝙳 | <code>{user.id}</code>\n"
        f" ◐ 𝙵𝙸𝚁𝚂𝚃 𝙽𝙰𝙼𝙴 | {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n◑ 𝙻𝙰𝚂𝚃 𝙽𝙰𝙼𝙴 | {html.escape(user.last_name)}"

    if user.username:
        text += f"\n◐ 𝚄𝚂𝙴𝚁𝙽𝙰𝙼𝙴 | @{html.escape(user.username)}"

    text += f"\n◑ 𝙿𝚁𝙾𝙵𝙸𝙻𝙴 𝙻𝙸𝙽𝙺 | {mention_html(user.id, '🖇️𝙷𝙴𝚁𝙴')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n ◐ 𝙿𝙾𝚂𝙸𝚃𝙸𝙾𝙽 | <code>{}</code>"

        afk_st = is_afk(user.id)
        if afk_st:
            text += _stext.format("AFK")
        else:
            status = status = bot.get_chat_member(chat.id, user.id).status
            if status:
                if status in {"𝙻𝙴𝙵𝚃", "𝙺𝙸𝙲𝙺𝙴𝙳"}:
                    text += _stext.format("Not here")
                elif status == "𝙼𝙴𝙼𝙱𝙴𝚁":
                    text += _stext.format("𝙳𝙴𝚃𝙴𝙲𝚃𝙴𝙳")
                elif status in {"𝙰𝙳𝙼𝙸𝙽𝙸𝚂𝚃𝚁𝙰𝚃𝙾𝚁", "𝙲𝚁𝙴𝙰𝚃𝙾𝚁"}:
                    text += _stext.format("𝙰𝙳𝙼𝙸𝙽")
    if user_id not in [bot.id, 777000, 1087968824]:
        userhp = hpmanager(user)
        text += f"\n\n<b>Health:</b> <code>{userhp['earnedhp']}/{userhp['totalhp']}</code>\n[<i>{make_bar(int(userhp['percentage']))} </i>{userhp['percentage']}%]"
        text += ' [<a href="https://t.me/genshinbotsupport/3">‼️</a>]'.format(
            bot.username,

         ) 

    try:
        spamwtc = sw.get_ban(int(user.id))
        if spamwtc:
            text += "\n\n<b>𝚃𝚑𝚒𝚜 𝚙𝚎𝚛𝚜𝚘𝚗 𝚒𝚜 𝚂𝚙𝚊𝚖𝚠𝚊𝚝𝚌𝚑𝚎𝚍!</b>"
            text += f"\nReason: <pre>{spamwtc.reason}</pre>"
            text += "\nAppeal at @genshinvoid"
        else:
            pass
    except:
        pass  # don't crash if api is down somehow...

    disaster_level_present = False

    if user.id == OWNER_ID:
        text += "\n\n❏ 𝙿𝙾𝚆𝙴𝚁𝚂"
        text += "\n\n◐ 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙼𝙴𝙼𝙱𝙴𝚁 𝙾𝙵 • 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 👥."

        text += "\n\n• 𝚁𝙰𝙽𝙺𝙴𝙳 𝙰𝚂 | 𝚄𝙽𝙺𝙽𝙾𝚆𝙽 𝙶𝙾𝙳."
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += "\n\n❏ 𝙿𝙾𝚆𝙴𝚁𝚂"
        text += "\n\n◐ 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙼𝙴𝙼𝙱𝙴𝚁 𝙾𝙵 • 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 👥."

        text += "\n\n• 𝚁𝙰𝙽𝙺𝙴𝙳 𝙰𝚂 | 𝙰𝚁𝙲𝙷𝙾𝙽𝚂 🚩."
        disaster_level_present = True
    elif user.id in DRAGONS:
        text += "\n\n❏ 𝙿𝙾𝚆𝙴𝚁𝚂"
        text += "\n\n◐ 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙼𝙴𝙼𝙱𝙴𝚁 𝙾𝙵 • 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 👥."

        text += "\n\n• 𝚁𝙰𝙽𝙺𝙴𝙳 𝙰𝚂 | 𝙻𝙴𝚂𝚂𝙴𝚁 𝙶𝙾𝙳  🚩."
        disaster_level_present = True
    elif user.id in DEMONS:
        text += "\n\n❏ 𝙿𝙾𝚆𝙴𝚁𝚂"
        text += "\n\n◐ 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙼𝙴𝙼𝙱𝙴𝚁 𝙾𝙵 • 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 👥."

        text += "\n\n• 𝚁𝙰𝙽𝙺𝙴𝙳 𝙰𝚂 | 𝙳𝙴𝙼𝙸𝙶𝙾𝙳  🚩."
        disaster_level_present = True

    elif user.id in TIGERS:
        text += "\n\n❏ 𝙿𝙾𝚆𝙴𝚁𝚂"
        text += "\n\n◐ 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙼𝙴𝙼𝙱𝙴𝚁 𝙾𝙵 • 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 👥."
        
        text += "\n\n• 𝚁𝙰𝙽𝙺𝙴𝙳 𝙰𝚂 | 5⭐ 𝙲𝙷𝙰𝚁𝙰𝙲𝚃𝙴𝚁𝚂  🚩."
        disaster_level_present = True
    
    elif user.id in WOLVES:
        text += "\n\n❏ 𝙿𝙾𝚆𝙴𝚁𝚂"
        text += "\n\n◐ 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙼𝙴𝙼𝙱𝙴𝚁 𝙾𝙵 • 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 👥."
        
        text += "\n\n• 𝚁𝙰𝙽𝙺𝙴𝙳 𝙰𝚂 | 4⭐ 𝙲𝙷𝙰𝚁𝙰𝙲𝚃𝙴𝚁𝚂  🚩."
        disaster_level_present = True
    
    elif user.id in MEMBERS:
        text += "\n\n❏ 𝙿𝙾𝚆𝙴𝚁𝚂"
        text += "\n\n◐ 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙼𝙴𝙼𝙱𝙴𝚁 𝙾𝙵 • 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 👥."
        
        text += "\n\n• 𝚁𝙰𝙽𝙺𝙴𝙳 𝙰𝚂 | 𝚅𝙸𝚂𝙸𝙾𝙽 𝙷𝙾𝙻𝙳𝙴𝚁𝚂  🚩."
        disaster_level_present = True
        

    if disaster_level_present:
        text += ' [<a href="https://t.me/genshinbotsupport/4">‼️</a>]'.format(
            bot.username,

        )


    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}",
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\nTitle:\n<b>{custom_title}</b>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            context.bot.sendChatAction(chat.id, "upload_photo")
            context.bot.send_photo(
                chat.id,
                photo=profile,
                caption=(text), 
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "𝙷𝙴𝙰𝙻𝚃𝙷", url="https://t.me/genshinbotsupport/3"
                            ),
                            InlineKeyboardButton(
                                "𝙳𝙸𝚂𝙰𝚂𝚃𝙴𝚁𝚂", url="https://t.me/genshinbotsupport/4"
                            ),
                        ],
                    ]
                ),
            
                parse_mode=ParseMode.HTML,
            )

            os.remove(f"{user.id}.png")
        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text, parse_mode=ParseMode.HTML, disable_web_page_preview=True,
            )

    else:
        message.reply_text(
            text, parse_mode=ParseMode.HTML, disable_web_page_preview=True,
        )

    rep.delete()



def about_me(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(message, args)

    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text(
            f"*{user.first_name}*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"{username} hasn't set an info message about themselves yet!",
        )
    else:
        update.effective_message.reply_text("There isnt one, use /setme to set one.")



def set_about_me(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in [777000, 1087968824]:
        message.reply_text("𝙴𝚛𝚛𝚘𝚛! 𝚄𝚗𝚊𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍")
        return
    bot = context.bot
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id in [bot.id, 777000, 1087968824] and (user_id in DEV_USERS):
            user_id = repl_user_id
    text = message.text
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id in [777000, 1087968824]:
                message.reply_text("𝙰𝚞𝚝𝚑𝚘𝚛𝚒𝚣𝚎𝚍...𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗 𝚞𝚙𝚍𝚊𝚝𝚎𝚍!")
            elif user_id == bot.id:
                message.reply_text("𝙸 𝚑𝚊𝚟𝚎 𝚞𝚙𝚍𝚊𝚝𝚎𝚍 𝚖𝚢 𝚒𝚗𝚏𝚘 𝚠𝚒𝚝𝚑 𝚝𝚑𝚎 𝚘𝚗𝚎 𝚢𝚘𝚞 𝚙𝚛𝚘𝚟𝚒𝚍𝚎𝚍!")
            else:
                message.reply_text("𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗 𝚞𝚙𝚍𝚊𝚝𝚎𝚍!")
        else:
            message.reply_text(
                "The info needs to be under {} characters! You have {}.".format(
                    MAX_MESSAGE_LENGTH // 4, len(info[1]),
                ),
            )



@sudo_plus
def stats(update: Update, context: CallbackContext):
    stats = "<b>📊 Current stats:</b>\n" + "\n".join([mod.__stats__() for mod in STATS])
    result = re.sub(r"(\d+)", r"<code>\1</code>", stats)
    update.effective_message.reply_text(result, parse_mode=ParseMode.HTML)



def about_bio(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text(
            "*{}*:\n{}".format(user.first_name, escape_markdown(info)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"{username} hasn't had a message set about themselves yet!\nSet one using /setbio",
        )
    else:
        update.effective_message.reply_text(
            "𝚈𝚘𝚞 𝚑𝚊𝚟𝚎𝚗'𝚝 𝚑𝚊𝚍 𝚊 𝚋𝚒𝚘 𝚜𝚎𝚝 𝚊𝚋𝚘𝚞𝚝 𝚢𝚘𝚞𝚛𝚜𝚎𝚕𝚏 𝚢𝚎𝚝!",
        )



def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "𝙷𝚊, 𝚢𝚘𝚞 𝚌𝚊𝚗'𝚝 𝚜𝚎𝚝 𝚢𝚘𝚞𝚛 𝚘𝚠𝚗 𝚋𝚒𝚘! 𝚈𝚘𝚞'𝚛𝚎 𝚊𝚝 𝚝𝚑𝚎 𝚖𝚎𝚛𝚌𝚢 𝚘𝚏 𝚘𝚝𝚑𝚎𝚛𝚜 𝚑𝚎𝚛𝚎...",
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("You are not authorised")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text(
                "𝙴𝚛𝚖... 𝚢𝚎𝚊𝚑, 𝙸 𝚘𝚗𝚕𝚢 𝚝𝚛𝚞𝚜𝚝 𝚅𝙾𝙸𝙳 𝙽𝙴𝚃𝚆𝙾𝚁𝙺 𝚝𝚘 𝚜𝚎𝚝 𝚖𝚢 𝚋𝚒𝚘.",
            )
            return

        text = message.text
        bio = text.split(
            None, 1,
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "Updated {}'s bio!".format(repl_message.from_user.first_name),
                )
            else:
                message.reply_text(
                    "Bio needs to be under {} characters! You tried to set {}.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1]),
                    ),
                )
    else:
        message.reply_text("Reply to someone to set their bio!")


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"<b>About user:</b>\n{me}\n"
    if bio:
        result += f"<b>What others say:</b>\n{bio}\n"
    result = result.strip("\n")
    return result


__help__ = """
*ID:*
 • `/id`*:* get the current group id. If used by replying to a message, gets that user's id.
 • `/gifid`*:* reply to a gif to me to tell you its file ID.

*Self addded information:*
 • `/setme <text>`*:* will set your info
 • `/me`*:* will get your or another user's info.
Examples:
 `/setme I am a wolf.`
 `/me @username(defaults to yours if no user specified)`

*Information others add on you:*
 • `/bio`*:* will get your or another user's bio. This cannot be set by yourself.
• `/setbio <text>`*:* while replying, will save another user's bio
Examples:
 `/bio @username(defaults to yours if not specified).`
 `/setbio This user is a wolf` (reply to the user)

*Overall Information about you:*
 • `/info`*:* get information about a user.

*What is that health thingy?*
 Come and see [HP System explained](https://t.me/OnePunchUpdates/192)
"""

SET_BIO_HANDLER = DisableAbleCommandHandler("setbio", set_about_bio, run_async=True)
GET_BIO_HANDLER = DisableAbleCommandHandler("bio", about_bio, run_async=True)

STATS_HANDLER = CommandHandler("stats", stats, run_async=True)
ID_HANDLER = DisableAbleCommandHandler("id", get_id, run_async=True)
GIFID_HANDLER = DisableAbleCommandHandler("gifid", gifid, run_async=True)
INFO_HANDLER = DisableAbleCommandHandler(("info", "ignite"), info, run_async=True)

SET_ABOUT_HANDLER = DisableAbleCommandHandler("setme", set_about_me, run_async=True)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("me", about_me, run_async=True)

dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)

__mod_name__ = "Info"
__command_list__ = ["setbio", "bio", "setme", "me", "info"]
__handlers__ = [
    ID_HANDLER,
    GIFID_HANDLER,
    INFO_HANDLER,
    SET_BIO_HANDLER,
    GET_BIO_HANDLER,
    SET_ABOUT_HANDLER,
    GET_ABOUT_HANDLER,
    STATS_HANDLER,
]
