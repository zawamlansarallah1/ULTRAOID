# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from . import *


@asst_cmd("ban")
@owner
async def banhammer(event):
    if not event.is_private:
        return
    x = await event.get_reply_message()
    if x is None:
        return await event.edit("الرجاء الرد على رسالة الشخص لحظرة .")
    target = get_who(x.id)
    if not is_blacklisted(target):
        blacklist_user(target)
        await asst.send_message(event.chat_id, f"#تم حظر \nالمستخدم  - {target}")
        await asst.send_message(
            target,
            "`مع السلامة ! لقد تم حظرك .`\n**لن نستقبل اي رساله منك فصاعدا .**",
        )
    else:
        return await asst.send_message(event.chat_id, f"المستخدم محظور بالفعل !")


@asst_cmd("unban")
@owner
async def banhammer(event):
    if not event.is_private:
        return
    x = await event.get_reply_message()
    if x is None:
        return await event.edit("يرجى الرد على رسالة الشخص لحظره.")
    target = get_who(x.id)
    if is_blacklisted(target):
        rem_blacklist(target)
        await asst.send_message(event.chat_id, f"#UNBAN\nUser - {target}")
        await asst.send_message(target, "`مبروووك! تم الغاء حظرك .`")
    else:
        return await asst.send_message(event.chat_id, f"المستخدم غير محظور أصلا!")
