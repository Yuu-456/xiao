import html
import json
import os
from typing import Optional

from zerotwobot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    MEMBERS,
    dispatcher,
)
from zerotwobot.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from zerotwobot.modules.helper_funcs.extraction import extract_user
from zerotwobot.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "zerotwobot/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply




@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚊 𝙷𝙰𝚂𝙷𝙸𝚁𝙰. ")
        return ""

    if user_id in DEMONS:
        rt += "𝚁𝚎𝚚𝚞𝚎𝚜𝚝𝚎𝚍 𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘 𝚙𝚛𝚘𝚖𝚘𝚝𝚎 𝚊 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽 𝚝𝚘 𝙷𝙰𝚂𝙷𝙸𝚁𝙰 ."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "𝚁𝚎𝚚𝚞𝚎𝚜𝚝𝚎𝚍 𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘 𝚙𝚛𝚘𝚖𝚘𝚝𝚎 𝚊 𝙳𝙴𝙼𝙾𝙽 𝚝𝚘 𝙷𝙰𝚂𝙷𝙸𝚁𝙰. "
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["sudos"].append(user_id)
    DRAGONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt
        + "\nSuccessfully set Disaster level of {} to 𝙷𝙰𝚂𝙷𝙸𝚁𝙰!".format(
            user_member.first_name,
        ),
    )

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "𝚁𝚎𝚚𝚞𝚎𝚜𝚝𝚎𝚍 𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘 𝚍𝚎𝚖𝚘𝚝𝚎 𝚝𝚑𝚒𝚜 𝙷𝙰𝚂𝙷𝙸𝚁𝙰 𝚝𝚘 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽. "
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚊 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽. ")
        return ""

    if user_id in WOLVES:
        rt += "𝚁𝚎𝚚𝚞𝚎𝚜𝚝𝚎𝚍 𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘 𝚙𝚛𝚘𝚖𝚘𝚝𝚎 𝚝𝚑𝚒𝚜 DEMON to 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽. "
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["supports"].append(user_id)
    DEMONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽!",
    )

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  𝙷𝙰𝚂𝙷𝙸𝚁𝙰, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 DEMON."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 DEMON."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚊 DEMON.")
        return ""

    data["whitelists"].append(user_id)
    WOLVES.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a DEMON!",
    )

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  𝙷𝙰𝚂𝙷𝙸𝚁𝙰, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  DEMON, 𝙿𝚛𝚘𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁."
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    if user_id in TIGERS:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚊 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁.")
        return ""

    data["tigers"].append(user_id)
    TIGERS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁!",
    )

    log_message = (
        f"#TIGER\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@sudo_plus
@gloggable
def addmember(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  𝙷𝙰𝚂𝙷𝙸𝚁𝙰, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷."
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)
    
    if user_id in TIGERS:
        rt += "𝚃𝚑𝚒𝚜 𝚖𝚎𝚖𝚋𝚎𝚛 𝚒𝚜 𝚊  DEMON, 𝙳𝚎𝚖𝚘𝚝𝚒𝚗𝚐 𝚝𝚘 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷."
        data["tigers"].remove(user_id)
        Tigers.remove(user_id)
        
    if user_id in MEMBERS:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚊 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷.")
        return ""

    data["members"].append(user_id)
    MEMBERS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷!",
    )

    log_message = (
        f"#MEMBER\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("𝚁𝚎𝚚𝚞𝚎𝚜𝚝𝚎𝚍 𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘 𝚝𝚊𝚔𝚎 𝚊𝚠𝚊𝚢 𝚝𝚑𝚒𝚜 𝚑𝚊𝚜𝚑𝚒𝚛𝚊'𝚜 𝚋𝚛𝚎𝚊𝚝𝚑𝚒𝚗𝚐 𝚜𝚝𝚢𝚕𝚎.")
        DRAGONS.remove(user_id)
        data["sudos"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message

        return log_message

    else:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚗𝚘𝚝 𝚊 𝙷𝙰𝚂𝙷𝙸𝚁𝙰!")
        return ""


@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DEMONS:
        message.reply_text("𝚁𝚎𝚚𝚞𝚎𝚜𝚝𝚎𝚍 𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘 𝚝𝚊𝚔𝚎 𝚊𝚠𝚊𝚢 𝚝𝚑𝚒𝚜 𝚕𝚘𝚠𝚎𝚛𝚖𝚘𝚘𝚗'𝚜 𝚋𝚕𝚘𝚘𝚍 𝚍𝚎𝚖𝚘𝚗 𝚊𝚛𝚝")
        DEMONS.remove(user_id)
        data["supports"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚗𝚘𝚝 𝚊 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽!")
        return ""



@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in WOLVES:
        message.reply_text("𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘𝚘𝚔 𝚊𝚠𝚊𝚢 𝚝𝚑𝚒𝚜 𝚍𝚎𝚖𝚘𝚗'𝚜 𝚋𝚕𝚘𝚘𝚍 𝚍𝚎𝚖𝚘𝚗 𝚊𝚛𝚝𝚜.")
        WOLVES.remove(user_id)
        data["whitelists"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚗𝚘𝚝 𝚊 𝙳𝙴𝙼𝙾𝙽!")
        return ""



@sudo_plus
@gloggable
def removetiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in TIGERS:
        message.reply_text("𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚝𝚘𝚘𝚔 𝚊𝚠𝚊𝚢 𝚝𝚑𝚒𝚜 𝚍𝚎𝚖𝚘𝚗 𝚜𝚕𝚊𝚢𝚎𝚛'𝚜 𝚋𝚛𝚎𝚊𝚝𝚑𝚒𝚗𝚐 𝚜𝚝𝚢𝚕𝚎𝚜")
        TIGERS.remove(user_id)
        data["tigers"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNTIGER\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚗𝚘𝚝 𝚊 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁!")
        return ""



@sudo_plus
@gloggable
def removemember(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in MEMBERS:
        message.reply_text("𝙳𝙴𝙼𝙾𝙽 𝙺𝙸𝙽𝙶 𝚛𝚎𝚖𝚘𝚟𝚎𝚍 𝚝𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚊𝚜 𝚋𝚕𝚊𝚌𝚔𝚜𝚖𝚒𝚝𝚑.")
        MEMBER.remove(user_id)
        data["members"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNMEMBER\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("𝚃𝚑𝚒𝚜 𝚞𝚜𝚎𝚛 𝚒𝚜 𝚗𝚘𝚝 𝚊 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷")
        return ""    
    
    

    
@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>𝙺𝚗𝚘𝚠𝚗 𝙳𝙴𝙼𝙾𝙽:</b>\n"
    m = update.effective_message.reply_text(
        "<code>𝙶𝚊𝚝𝚑𝚎𝚛𝚒𝚗𝚐 𝚒𝚗𝚝𝚎𝚕 𝚏𝚛𝚘𝚖 VOID..</code>", parse_mode=ParseMode.HTML,
    )
    bot = context.bot
    for each_user in WOLVES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)



@whitelist_plus
def tigerlist(update: Update, context: CallbackContext):
    reply = "<b>𝙺𝚗𝚘𝚠𝚗 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁:</b>\n"
    m = update.effective_message.reply_text(
        "<code>𝙶𝚊𝚝𝚑𝚎𝚛𝚒𝚗𝚐 𝚒𝚗𝚝𝚎𝚕 𝚏𝚛𝚘𝚖 VOID..</code>", parse_mode=ParseMode.HTML,
    )
    bot = context.bot
    for each_user in TIGERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)



@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>𝙶𝚊𝚝𝚑𝚎𝚛𝚒𝚗𝚐 𝚒𝚗𝚝𝚎𝚕 𝚏𝚛𝚘𝚖 VOID..</code>", parse_mode=ParseMode.HTML,
    )
    reply = "<b>𝙺𝚗𝚘𝚠𝚗 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽:</b>\n"
    for each_user in DEMONS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)



@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>𝙶𝚊𝚝𝚑𝚎𝚛𝚒𝚗𝚐 𝚒𝚗𝚝𝚎𝚕 𝚏𝚛𝚘𝚖 VOID..</code>", parse_mode=ParseMode.HTML,
    )
    true_sudo = list(set(DRAGONS) - set(DEV_USERS))
    reply = "<b>𝙺𝚗𝚘𝚠𝚗 𝙷𝙰𝚂𝙷𝙸𝚁𝙰:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)





@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>𝙶𝚊𝚝𝚑𝚎𝚛𝚒𝚗𝚐 𝚒𝚗𝚝𝚎𝚕 𝚏𝚛𝚘𝚖 VOID..</code>", parse_mode=ParseMode.HTML,
    )
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>𝙺𝚗𝚘𝚠𝚗 𝚄𝙿𝙿𝙴𝚁𝙼𝙾𝙾𝙽:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)

    
    
    
    
@whitelist_plus   
def memberlist(update: Update, context: CallbackContext):
    reply = "<b>𝙺𝚗𝚘𝚠𝚗 𝙱𝙻𝙰𝙲𝙺𝚂𝙼𝙸𝚃𝙷 :</b>\n"
    m = update.effective_message.reply_text(
        "<code>𝙶𝚊𝚝𝚑𝚎𝚛𝚒𝚗𝚐 𝚒𝚗𝚝𝚎𝚕 𝚏𝚛𝚘𝚖 VOID..</code>", parse_mode=ParseMode.HTML,
    )
    bot = context.bot
    for each_user in MEMBERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)
    

__help__ = f"""
*⚠️ Notice:*
Commands listed here only work for users with special access and are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands.

 ╔ *List all special users:*
 ╠ `/hashiras`*:* 𝙻𝚒𝚜𝚝𝚜 𝚊𝚕𝚕 𝙷𝙰𝚂𝙷𝙸𝚁𝙰 
 ╠ `/lowermoons`*:* 𝙻𝚒𝚜𝚝𝚜 𝚊𝚕𝚕 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽
 ╠ `/blacksmiths`*:* 𝙻𝚒𝚜𝚝𝚜 𝚊𝚕𝚕 𝙺𝙽𝙸𝙶𝙷𝚃
 ╠ `/demonslayers`*:* 𝙻𝚒𝚜𝚝𝚜 𝚊𝚕𝚕 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁𝚂
 ╠ `/demons`*:* 𝙻𝚒𝚜𝚝𝚜 𝚊𝚕𝚕 𝙳𝙴𝙼𝙾𝙽
 ╠ `/uppermoons`*:* 𝙻𝚒𝚜𝚝𝚜 𝚊𝚕𝚕 𝙰𝚁𝙲𝙷𝙾𝙽
 ╠ `/addhashira`*:* 𝙰𝚍𝚍 𝚊 𝚞𝚜𝚎𝚛 𝚝𝚘 HASHIRA
 ╠ `/addlowermoon`*:* 𝙰𝚍𝚍 𝚊 𝚞𝚜𝚎𝚛 𝚝𝚘 𝙻𝙾𝚆𝙴𝚁𝙼𝙾𝙾𝙽
 ╠ `/adddemonslayer`*:* 𝙰𝚍𝚍 𝚊 𝚞𝚜𝚎𝚛 𝚝𝚘 𝙳𝙴𝙼𝙾𝙽 𝚂𝙻𝙰𝚈𝙴𝚁𝚂
 ╠ `/adddemons`*:* 𝙰𝚍𝚍 𝚊 𝚞𝚜𝚎𝚛 𝚝𝚘 𝙳𝙴𝙼𝙾𝙽
 ╠ `/addblacksmith`*:* 𝙰𝚍𝚍 𝚊 𝚞𝚜𝚎𝚛 𝚝𝚘 𝙺𝙽𝙸𝙶𝙷𝚃
 ╚ `Add dev doesnt exist, devs should know how to add themselves`

 ╔ *Ping:*
 ╠ `/ping`*:* gets ping time of bot to telegram server
 ╚ `/pingall`*:* gets all listed ping times

 ╔ *Broadcast: (Bot owner only)*
 ╠  *Note:* This supports basic markdown
 ╠ `/broadcastall`*:* Broadcasts everywhere
 ╠ `/broadcastusers`*:* Broadcasts too all users
 ╚ `/broadcastgroups`*:* Broadcasts too all groups

 ╔ *Groups Info:*
 ╠ `/groups`*:* List the groups with Name, ID, members count as a txt
 ╠ `/leave <ID>`*:* Leave the group, ID must have hyphen(-)
 ╠ `/stats`*:* Shows overall bot stats
 ╠ `/getchats`*:* Gets a list of group names the user has been seen in. Bot owner only
 ╚ `/ginfo username/link/ID`*:* Pulls info panel for entire group

 ╔ *Access control:*
 ╠ `/ignore`*:* Blacklists a user from
 ╠  using the bot entirely
 ╠ `/lockdown <off/on>`*:* Toggles bot adding to groups
 ╠ `/notice`*:* Removes user from blacklist
 ╚ `/ignoredlist`*:* Lists ignored users

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Prints modules and their names
 ╠ `/unload <name>`*:* Unloads module dynamically
 ╚ `/load <name>`*:* Loads module

 ╔ *Speedtest:*
 ╚ `/speedtest`*:* Runs a speedtest and gives you 2 options to choose from, text or image output

 ╔ *Global Bans:*
 ╠ `/gban user reason`*:* Globally bans a user
 ╚ `/ungban user reason`*:* Unbans the user from the global bans list

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Lists names of all modules
 ╠ `/load modulename`*:* Loads the said module to
 ╠   memory without restarting.
 ╠ `/unload modulename`*:* Loads the said module from
 ╚   memory without restarting.memory without restarting the bot

 ╔ *Remote commands:*
 ╠ `/rban user group`*:* Remote ban
 ╠ `/runban user group`*:* Remote un-ban
 ╠ `/rkick user group`*:* Remote kick
 ╠ `/rmute user group`*:* Remote mute
 ╚ `/runmute user group`*:* Remote un-mute

 ╔ *Windows self hosted only:*
 ╠ `/reboot`*:* Restarts the bots service
 ╚ `/gitpull`*:* Pulls the repo and then restarts the bots service

 ╔ *Chatbot:*
 ╚ `/listaichats`*:* Lists the chats the chatmode is enabled in

 ╔ *Debugging and Shell:*
 ╠ `/debug <on/off>`*:* Logs commands to updates.txt
 ╠ `/logs`*:* Run this in support group to get logs in pm
 ╠ `/eval`*:* Self explanatory
 ╠ `/sh`*:* Runs shell command
 ╠ `/shell`*:* Runs shell command
 ╠ `/clearlocals`*:* As the name goes
 ╠ `/dbcleanup`*:* Removes deleted accs and groups from db
 ╚ `/py`*:* Runs python code

 ╔ *Global Bans:*
 ╠ `/gban <id> <reason>`*:* Gbans the user, works by reply too
 ╠ `/ungban`*:* Ungbans the user, same usage as gban
 ╚ `/gbanlist`*:* Outputs a list of gbanned users

"""

SUDO_HANDLER = CommandHandler(("addsudo", "adddragon", "addhashira"), addsudo, run_async=True)

SUPPORT_HANDLER = CommandHandler(("addsupport", "adddemon", "addlowermoon"), addsupport, run_async=True)
TIGER_HANDLER = CommandHandler(("addtiger", "adddemonslayer", "adddemonslayers", "addslayers"), addtiger, run_async=True)
WHITELIST_HANDLER = CommandHandler(("addwhitelist", "addwolf", "adddemon", "adddemons"), addwhitelist, run_async=True)
UNSUDO_HANDLER = CommandHandler(("removesudo", "removedragon", "removehashira"), removesudo, run_async=True)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "removedemon", "removelowermoon"), removesupport, run_async=True)
UNTIGER_HANDLER = CommandHandler(("removetiger", "removedemonslayers", "removedemonslayer", "removeslayers"), removetiger, run_async=True)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "removewolf", "removedemons", "removedemon"), removewhitelist, run_async=True)
MEMBER_HANDLER = CommandHandler(("addmember", "addblacksmith", "addblacksmiths"), addmember, run_async=True)
UNMEMBER_HANDLER = CommandHandler(("removemember", "removeblacksmith", "removeblacksmiths"), removemember, run_async=True)
                                   
WHITELISTLIST_HANDLER = CommandHandler(["whitelistlist", "wolves", "demon", "demons"], whitelistlist, run_async=True) 
TIGERLIST_HANDLER = CommandHandler(["tigers", "demonslayers", "demonslayer", "slayers"], tigerlist, run_async=True)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "demons", "lowermoon", "lowermoons"], supportlist, run_async=True)
MEMBERLIST_HANDLER = CommandHandler(["members", "blacksmiths", "blacksmiths"], memberlist, run_async=True)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "dragons", "hashira", "hashiras"], sudolist, run_async=True)
DEVLIST_HANDLER = CommandHandler(["devlist", "heroes", "uppermoon", "uppermoons"], devlist, run_async=True)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(TIGER_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNTIGER_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)
dispatcher.add_handler(MEMBERLIST_HANDLER)
dispatcher.add_handler(MEMBER_HANDLER)
dispatcher.add_handler(UNMEMBER_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
 
dispatcher.add_handler(TIGERLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Disasters"
__handlers__ = [
    SUDO_HANDLER,
    SUPPORT_HANDLER,
    TIGER_HANDLER,
    WHITELIST_HANDLER,
    MEMBER_HANDLER,

    UNSUDO_HANDLER,
    UNSUPPORT_HANDLER,
    UNTIGER_HANDLER,
    UNWHITELIST_HANDLER,
    UNMEMBER_HANDLER,
    WHITELISTLIST_HANDLER,
    TIGERLIST_HANDLER,
    SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER,
    DEVLIST_HANDLER,
    MEMBERLIST_HANDLER,
]
