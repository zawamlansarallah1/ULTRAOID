# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from datetime import datetime

from pyUltroid.functions.asst_fns import *
from pyUltroid.misc import owner_and_sudos
from telethon import events
from telethon.utils import get_display_name

from plugins import *

from . import *

Owner_info_msg = f"""
**اسم المدير** - {OWNER_NAME}
**ايدي المدير** - `{OWNER_ID}`

**توجية الرسائل ** - {udB.get("PMBOT")}

__النسخة  {ultroid_version}, بواسطة  @zawamlansarallah__
"""

_settings = [
    [
        Button.inline("API توكنات", data="apiset"),
        Button.inline("بوت التواصل", data="chatbot"),
    ],
    [
        Button.inline("حالة البوت", data="alvcstm"),
        Button.inline("اعدادات الخاص", data="ppmset"),
    ],
    [Button.inline("المميزات", data="otvars")],
    [Button.inline("بوت  المكالمات الصوتية", data="vcb")],
    [Button.inline("« عودة", data="mainmenu")],
]

_start = [
    [
        Button.inline("اللغة 🌐", data="lang"),
        Button.inline("الاعدادات ⚙️", data="setter"),
    ],
    [
        Button.inline("حالة البوت ✨", data="stat"),
        Button.inline("اذاعه 📻", data="bcast"),
    ],
]


@callback("ownerinfo")
async def own(event):
    await event.edit(
        Owner_info_msg,
        buttons=[Button.inline("اغلاق", data=f"closeit")],
    )


@callback("closeit")
async def closet(lol):
    await lol.delete()


@asst_cmd("start ?(.*)")
async def ultroid(event):
    if event.is_group:
        if str(event.sender_id) in owner_and_sudos():
            return await event.reply(
                "`انا لا اعمل بالقروبات `",
                buttons=[
                    Button.url(
                        "⚙️الاعدادات⚙️", url=f"https://t.me/{asst.me.username}?start=set"
                    )
                ],
            )
    else:
        if (
            not is_added(event.sender_id)
            and str(event.sender_id) not in owner_and_sudos()
        ):
            add_user(event.sender_id)
        if str(event.sender_id) not in owner_and_sudos():
            ok = ""
            u = await event.client.get_entity(event.chat_id)
            if not udB.get("STARTMSG"):
                if udB.get("PMBOT") == "True":
                    ok = "تستطيع مراسلة المشرف عبر هذا البوت !!\n\nارسل رسالتك وسيتم الرد عليها قريبا ."
                await event.reply(
                    f"مرحبا  [{get_display_name(u)}](tg://user?id={u.id}), هذا البوت مساعد  [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.uid})!\n\n{ok}",
                    buttons=[Button.inline("Info.", data="ownerinfo")],
                )
            else:
                me = f"[{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.uid})"
                mention = f"[{get_display_name(u)}](tg://user?id={u.id})"
                await event.reply(
                    Redis("STARTMSG").format(me=me, mention=mention),
                    buttons=[Button.inline("معلومات المدير .", data="ownerinfo")],
                )
        else:
            name = get_display_name(event.sender_id)
            if event.pattern_match.group(1) == "set":
                await event.reply(
                    "اختر احد الخيارات بالاسفل  -",
                    buttons=_settings,
                )
            else:
                await event.reply(
                    get_string("ast_3").format(name),
                    buttons=_start,
                )


@callback("mainmenu")
@owner
async def ultroid(event):
    if event.is_group:
        return
    await event.edit(
        get_string("ast_3").format(OWNER_NAME),
        buttons=_start,
    )


@callback("stat")
@owner
async def botstat(event):
    ok = len(get_all_users())
    msg = """حالة البوت  - 
كامل المستخدمين  - {}""".format(
        ok,
    )
    await event.answer(msg, cache_time=0, alert=True)


@callback("bcast")
@owner
async def bdcast(event):
    ok = get_all_users()
    await event.edit(f" الارسال الى  {len(ok)} مستخدم.")
    async with event.client.conversation(OWNER_ID) as conv:
        await conv.send_message(
            "قم بادخال الرساله التي تريد نشرها .\nاو اضغط  /cancel لالغاء الطلب.",
        )
        response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message("Cancelled!!")
        else:
            success = 0
            fail = 0
            await conv.send_message(f"جاري الارسال الى  {len(ok)} مستخدم ...")
            start = datetime.now()
            for i in ok:
                try:
                    await asst.send_message(int(i), f"{themssg}")
                    success += 1
                except BaseException:
                    fail += 1
            end = datetime.now()
            time_taken = (end - start).seconds
            await conv.send_message(
                f"""
تم ارسال الرساله في  {time_taken} ثواني.
عدد المشتركين بالبوت  - {len(ok)}
تم الارسال ل  {success} مشترك.
فشل الارسال الى  {fail} مشترك .""",
            )


@callback("setter")
@owner
async def setting(event):
    await event.edit(
        "اختار احد الخيارات بالاسفل  -",
        buttons=_settings,
    )
