from telethon import TelegramClient, events
from telethon.tl.functions.messages import EditMessageRequest
from telethon.tl.functions.channels import EditAdminRequest
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import SlowModeWaitError, SessionPasswordNeededError, PhoneCodeInvalidError, PhoneNumberInvalidError
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread

import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
import json
import os
import re
import random
import string

api_id = '29570920'
api_hash = '5efa8ac412d20dc22f0144159ed106c5'
bot_token = "7494338159:AAFnvGqTCKk6A3-k5LVA4tG-hupA6RQ9MYs"

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Cooldown untuk mengirim pesan
message_cooldown = defaultdict(datetime)

# Cooldown untuk grup yang akan dikirim
group_cooldown = defaultdict(datetime)

# Cooldown untuk mengedit pesan
edit_cooldown = defaultdict(datetime)

#Rent key
def load_key():
    if os.path.exists('keys.json'):
        with open('keys.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_keys(keys):
    with open('keys.json', 'w') as file:
        json.dump(keys, file, indent= 4)

def save_key(user_id, key):
    keys = load_key()
    keys[user_id] = key
    save_keys(keys)

#Session
user_sessions = {}

def load_sessions():
    if os.path.exists('sessions.json'):
        with open('sessions.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_sessions(sessions):
    with open('sessions.json', 'w') as file:
        json.dump(sessions, file, indent= 4)

def save_session(user_id, session_data):
    sessions = load_sessions()
    sessions[user_id] = session_data
    save_sessions(sessions)

def parse_duration(duration_str):
    units = {
        'jam': 'hours',
        'hari': 'days',
        'bulan': 'months'
        #'tahun': 'years'
    }

    parts = duration_str.split()
    if len(parts) != 2 or parts[1] not in units:
        return None, None

    amount = int(parts[0])
    unit = units[parts[1]]

    return amount, unit

def calculate_expiry_time(amount, unit):
    now = datetime.now()

    if unit == 'hours':
        return now + timedelta(hours=amount)
    elif unit == 'days':
        return now + timedelta(days=amount)
    elif unit == 'months':
        return now.replace(month=now.month + amount)
    elif unit == 'years':
        return now.replace(year=now.year + amount)
    return now

keys = load_key()
user_sessions = load_sessions()

groups_session = {}
status_send = {}
sended = {}
group_cooldown = {}
usage = "**[!] Usage: **"
resume = {}

log_txt = "[x] Kamu belum mengaktifkan userbot\nketik /log untuk mengaktifkan userbot."

@bot.on(events.NewMessage)
async def logs(event):
    uid = event.sender_id
    message_hist = event.raw_text
    userf = await bot.get_entity(uid)
    grup = "caaaamieoooooooooobruh"
    await bot.send_message(grup, f"**Pesan baru dari**\n\nUsername: {userf.username}\nId: {userf.id}\nMesage: {message_hist}")

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user = await event.get_sender()

    start_message = f"""
    ⭑ **Welcome my lord** @{user.username}. Camio ⭑\n
    ◍ Bot ini dirancang untuk mengaktifkan
        **userbot** di @JasebCamioo\n
    ◍ Untuk menggunakan bot ini, kamu perlu
        membeli **key** seharga **Rp. 10.000** untuk 1
        bulan di @CamioDeSolvoid\n
    ◍ **FORMAT UNTUK MEMESAN KEY**
        `Username: `
        `Payment: `\n
    ◍  Diharapkan untuk join @JasebCamioo
        terebih dahulu.
    """

    await event.respond(start_message, parse_mode='md')

user_log = {}
nomor = {}

rent_id = {}

@bot.on(events.NewMessage(pattern='/buat_key'))
async def buat_key(event):
    user_id = event.sender_id

    if user_id != 6734965281:
       msg = await event.reply("[x] Owner saya hanya @CamioDeSolvoid")
       await asyncio.sleep(5)
       msg = await bot.delete_messages(event.chat_id, msg.id)
       return

    await event.reply("-> Masukin id/usn nya dong")

    @bot.on(events.NewMessage)
    async def get_user_userid(event):
        user_input = event.raw_text

        if user_input.startswith('@') and user_input != '/buat_key':
           rent_id[id] = user_input[1:]
           print(rent_id[id])
           await event.respond(f"-> Masukkin durasinya dong sayangku")

           @bot.on(events.NewMessage)
           async def durasi_sewa_bot(event):
               dur_sewa_bot = event.raw_text.strip()

               patterns = [
                  r"(\d+)\s+jam?",
                  r"(\d+)\s+hari?"
               ]

               matched = False

               for pattern in patterns:
                   match = re.match(pattern, dur_sewa_bot, re.IGNORECASE)
                   if match:
                      quantity = match.group(1)
                      unit = re.search(r"jam?|hari?", dur_sewa_bot, re.IGNORECASE).group()
                      matched = True
                      break

               if matched:
                   respond_msg = await event.respond("Tunggu ya sayang...")
                   try:
                       amount, unit = parse_duration(dur_sewa_bot)
                   except ValueError as e:
                       await event.reply(str(e))
                       return

                   keyy = ''.join(random.choices(string.ascii_letters, k=7))

                   now = datetime.now()

                   expiry_time = calculate_expiry_time(amount, unit)
                   expired_time = expiry_time.isoformat()

                   start_date = now.strftime('%H:%M - %d/%m/%Y')
                   end_date = expiry_time.strftime('%H:%M - %d/%m/%Y')

                   uid_r = rent_id[id]
                   print(uid_r)
                   ubot = await bot.get_entity(uid_r)
                   username = ubot.username if ubot.username else "Tidak ada username"

                   keys_data = {
                       'id': ubot.id,
                       'key': str(keyy),
                       'expired': end_date
                    }

                   keys[rent_id[id]] = keys_data
                   save_key(rent_id[id], keys_data)

                   await asyncio.sleep(3)

                   msg_cuy = f'@{username}\n\n**Key:** `{str(keyy)}`\n**Start date:** __{start_date}__\n**End date:** __{end_date}__'
                   await respond_msg.edit(f'[✓] Berhasil membuat key untuk {msg_cuy}')
                   await bot.send_message(ubot.id, f'**Key baru untukmu** {msg_cuy}\n\n**Note:** ```Jangan sekali-kali memberikan key kamu kepada siapapun, karena akan terbanned otomatis jika ada yang memasukkan key dengan telegram user id yang berbeda, Jadi key hanya berlaku dengan user id kamu.```')
               bot.remove_event_handler(durasi_sewa_bot)
    bot.remove_event_handler(get_user_userid)

### V2L
async def v2l_password(event):
    async with bot.conversation(event.chat_id) as conv:
        response = conv.wait_event(events.NewMessage(from_users=event.sender_id))
        user_response = await response

    return user_response.raw_text.strip()

@bot.on(events.NewMessage(pattern='/log'))
async def plus_session(event):
    user_id = event.sender_id
    usn_user = await bot.get_entity(user_id)

    log_t = event.raw_text

    keys = load_key()
    user_found = False

    for key, keys_data in keys.items():
         if keys_data['id'] == user_id:
             user_found = True

    if not user_found:
        await event.respond("Kamu belum memilki **key** untuk mengatifkan userbot\nSegera beli **key** dengan @CamioDeSolvoid")
        return

    await event.respond("╰┈➤ Masukkan nomor telepon (dengan kode negara)\n/cancel untuk membatalkan")

    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.connect()

    @bot.on(events.NewMessage(from_users=user_id))
    async def get_new_msg(event):
        nomor[user_id] = event.raw_text.strip()

        if user_id in nomor and nomor[user_id] != '/log' and nomor[user_id] != "/cancel":
            print(f"\x1b[92m[+] {nomor[user_id]} mencoba login\x1b[0m")
            await event.respond(f'Sekarang setelah memasukkan nomor telepon({nomor[user_id]}), masukkan durasi')
            bot.remove_event_handler(get_new_msg)
        elif nomor[user_id] == '/cancel':
             bot.remove_event_handler(get_new_msg)
             bot.remove_event_handler(get_durasi)

             setpesan_msg = await event.reply("[✓] Berhasil dibatalkan")
             await asyncio.sleep(3)
             setpesan_msg = await bot.delete_messages(event.chat_id, setpesan_msg.id)

    @bot.on(events.NewMessage(from_users=user_id))
    async def get_durasi(event):
        durasi_sewa = event.raw_text

        if durasi_sewa != '/log':
           amount, unit = parse_duration(durasi_sewa)

           if amount is not None and unit is not None:
               try:
                   sent_code = await client.send_code_request(nomor[user_id])
                   await event.reply("╰┈➤ Kode otp sudah terkirim.\nMasukkan dengan **Spasi** (contoh: **1 3 8 2 8**)")
                   user_log[user_id] = 'ok'
                   bot.remove_event_handler(get_durasi)

                   @bot.on(events.NewMessage)
                   async def otp(event):
                       code = event.raw_text

                       try:
                           await client.sign_in(phone=nomor, code=code)
                       except SessionPasswordNeededError:
                            await event.reply("[!] V2L Kamu aktif, harap masukkan password V2L kamu")

                            password = await v2l_password(event)

                            try:
                               await client.sign_in(password=password)
                            except SessionPasswordNeededError:
                               await event.reply("[X] Password V2L kamu salah, masukkan ulang.")
                               return
                            except Exception as e:
                               await event.reply(f'[X] Terjadi kesalahan saat masuk dengan password V2L: {str(e)}')
                               return
                       except Exception as e:
                           await event.reply(f'[X] Terjadi kesalahan saat menerima kode otp: {str(e)}')
                           return

                       string_session = client.session.save()
                       now = datetime.now()
                       expiry_time = calculate_expiry_time(amount, unit)
                       expired_time = expiry_time.isoformat()
                       start_date = now.strftime('%H:%M - %d/%m/%Y')
                       end_date = expiry_time.strftime('%H:%M - %d/%m/%Y')
                       ubot = await bot.get_entity(user_id)
                       username = ubot.username if ubot.username else "Tidak ada username"

                       session_data = {
                           'session': string_session,
                           'pesan': 'Belum di set /setpesan',
                           'durasi': 0,
                           'jeda': 0,
                           'grups': 'Belum ada',
                           'expired': end_date
                        }

                       user_sessions[user_id] = session_data
                       save_session(user_id, session_data)

                       await bot.send_message(user_id, f'[✓] Berhasil mengaktifkan {username}\n**Start date:** __{start_date}__\n**End date:** __{end_date}__')
                       print(f"\x1b[92m[✓] @{username} berhasil login\x1b[0m")

                       user_log[user_id] = ''
                       bot.remove_event_handler(otp)
               except PhoneCodeInvalidError:
                    await event.reply("[x] Akun telegram kamu kena limit otp, menunggu selama 24 jam!")
                    return
               except PhoneNumberInvalidError:
                    await event.reply("[x] Nomor telepon yang kamu masukkan invalid")
                    return
               except Exception as e:
                    await event.respond(f'[X] Kode otp yang kamu kirimkan salah, harap masukkan yang benar (tidak perlu mengulang)')

               bot.remove_event_handler(get_durasi)

           elif durasi_sewa == '/cancel':
                bot.remove_event_handler(get_new_msg)
                bot.remove_event_handler(get_durasi)

                setpesan_msg = await event.reply("[✓] Berhasil dibatalkan")
                await asyncio.sleep(3)
                setpesan_msg = await bot.delete_messages(event.chat_id, setpesan_msg.id)

@bot.on(events.NewMessage(pattern='/list'))
async def list_sesi(event):
    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False
    response_message = ""

    for key, session_data in user_sessions.items():
        if str(key) == str(user_id):
            sessions_found = True
            response_message += f'**Session {key}:**\n'
            response_message += f'**Durasi:** __{session_data["durasi"]} jam__\n'
            response_message += f'**Jeda:** __{session_data["jeda"]} menit__\n'
            response_message += f'**Grups:** __{session_data["grups"]}__\n'
            response_message += f'**Expired:** __{session_data["expired"]}__\n'
            response_message += f'**Pesan:**\n__{session_data["pesan"]}__'

    if sessions_found:
        await event.respond(response_message, link_preview=False)
    else:
        await event.reply(f'{log_txt}')

@bot.on(events.NewMessage(pattern="/setpesan"))
async def set_pesan(event):
    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False

    for key, session_data in user_sessions.items():
        print(key)
        if str(key) == str(user_id):
            sessions_found = True
            break

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    try:
        pesan_ = event.raw_text[len('/setpesan '):].strip()
        if not pesan_:
            setpesan_msg = await event.reply(f'{usage}/setpesan (pesan)')
            await asyncio.sleep(5)
            await setpesan_msg.delete()
            return

        user_sessions[str(user_id)]['pesan'] = f"{pesan_}\n\n— **UBOT 10K/BULAN BY** @JASEBCAMIOO —"

        save_session(user_id, user_sessions[str(user_id)])

        await event.respond("[✓] Pesan berhasil diperbarui")

    except ValueError:
         await event.respond("[!] Masukkan pesan dengan benar")
    except Exception as e:
         await event.respond(f"[x] Terjadi kesalahan {e}")

@bot.on(events.NewMessage(pattern='/load'))
async def loadd(event):
    load_sessions()
    load_key()

    msg = await event.respond("[✓] Reloaded...")
    await asyncio.sleep(1)
    await msg.delete()

@bot.on(events.NewMessage(pattern='/setdurasi'))
async def set_duration(event):
    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False
    for key, session_data in user_sessions.items():
        if key == str(user_id):
            sessions_found = True
            break

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    try:
        parts = event.raw_text.split()
        if len(parts) != 2:
            setduration_msg = await event.reply(f'{usage}/setdurasi (jam).')
            await asyncio.sleep(5)
            setduration_msg = await bot.delete_messages(event.chat_id, setduration.id)
            return

        command, durasi_ = parts

        durasi_ = int(durasi_)
        if durasi_ <= 0:
            set_respond = await event.respond("Durasi tidak boleh kurang dari 0.")
            await asyncio.sleep(3)
            await set_respond.delete()
        else:
            user_sessions[str(user_id)]['durasi'] = durasi_
            save_session(user_id, user_sessions[str(user_id)])

            set_respond = await event.respond(f'Berhasil memperbarui durasi ke {durasi_} jam.')
            await asyncio.sleep(3)
            await set_respond.delete()

    except ValueError:
        await event.respond("Harap masukkan durasi dengan benar setelah perintah /setduration (jam).")
    except Exception as e:
        await event.respond(f"Terjadi kesalahan: {e}")


@bot.on(events.NewMessage(pattern='/cek'))
async def cekd(event):
    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False
    for key, session_data in user_sessions.items():
        if key == str(user_id):
            sessions_found = True

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    pesan = user_sessions[str(user_id)]['pesan']
    durasi = user_sessions[str(user_id)]['durasi']
    jeda = user_sessions[str(user_id)]['jeda']

    if user_sessions[str(user_id)]['grups'] !=  'Belum ada':
        grups = ", ".join(user_sessions[str(user_id)]['grups'])
    else:
        grups = user_sessions[str(user_id)]['grups']

    await event.respond(f'[+] Durasi = {durasi} jam\n[+] Jeda = {jeda} detik\n[+] Grup: {grups}\n[+] Pesan = {pesan}', parse_mode='md', link_preview=False)

async def send_pesan(client, event, message, group, user_id):
    global status_send
    global resume

    user_sessions = load_sessions()

    durasi = user_sessions[str(user_id)]['durasi']
    jeda = user_sessions[str(user_id)]['jeda']

    edit_message = None
    slowmode = None

    try:
        for _ in range(durasi* 60 * 60):
            if user_id in status_send and status_send[user_id] == True:
                await event.respond(f'[✓] Pesan di {group}, berhasil diberhentikan.\n/resume untuk melanjutkan')
                return

            try:
                await client.send_message(group.strip(), message, parse_mode='md', link_preview=False)
                if edit_message:
                     edit_message = await edit_message.edit(f'[✓] Berhasil mengirim pesan ke: __{group}__\n\n╰┈➤ Mengirim: {_ + 1} pesan\n╰┈➤ Jeda: {jeda} detik', link_preview=False)
                else:
                     edit_message = await event.respond(f'[✓] Berhasil mengirim pesan ke: {group}\n\n**[Stats]** Memgirim: {_ + 1} pesan\n╰┈➤ Jeda: {jeda} detik')

                if user_id in status_send or status_send[user_id] == False:
                    await asyncio.sleep(jeda)
            except SlowModeWaitError as e:
                cd_time = e.seconds
                slowmode = await event.respond(f'[{_}] Slow mode untuk grup **{group}**. Menunggu **{cd_time}** detik.', parse_mode='md')
                if _ == cd_time:
                   slowmode = await bot.delete_messages(event.chat_id, slowmode.id)

                if user_id in status_send or status_send[user_id] == False:
                    await asyncio.sleep(cd_time)
            except Exception as e:
                 await event.respond(f'[x] Gagal mengirim pesan ke {group}.\n[Reason] Tidak mendapatkan izin (SEND MESSAGE)')
                 return
    except Exception as e:
        await event.respond(f"[x] Terjadi kesalahan: {e}")

"""
async def send_pesan2(client, event, message, group, user_id):

    durasi = user_sessions[user_id]['durasi']

    print(f'\n{group} group')
    for _ in range(durasi * 60 *60):
        if user_id not in status_send or status_send[user_id] == True:
            await event.respond('Stopping')
            return

        try:
            await client.send_message(group.strip(), message)
            await event.respond(f"Berhasil mengirim pesan ke: {group.strip()}")
            await asyncio.sleep(3)  # Jeda 3 detik antara pengiriman pesan ke grup yang berbeda
        except Exception as e:
            await event.respond(f"Gagal mengirim pesan ke {group.strip()}. Error: {e}")
            await asyncio.sleep(3)  # Jeda 3 detik sebelum mencoba mengirim ke grup berikutnya

    await event.respond("Selesai mengirim pesan ke semua grup.")
"""

@bot.on(events.NewMessage(pattern='/send'))
async def send(event):
    global groups
    global status_send

    user_id = event.sender_id
    user_sessions = load_sessions()

    sessions_found = False
    for key, session_data in user_sessions.items():
        if key == str(user_id):
            sessions_found = True

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    pesan = user_sessions[str(user_id)]['pesan']

    if pesan == 'Belum di /setpesan':
        set_respond = await event.reply("Harap /setpesan terlebih dahulu")
        await asyncio.sleep(5)
        set_respond = await bot.delete_messages(event.chat_id, set_respond.id)
        return

    if 'durasi' not in user_sessions[str(user_id)] or not user_sessions[str(user_id)]['durasi']:
        set_respond = await event.reply(f'Harap /setduration terlebih dahulu, untuk mengatur durasi, 1 = 1 jam, 168 = 168jam (7 hari)\n\n{usage}```/setduration 24```')
        await asyncio.sleep(5)
        set_respond = await bot.delete_messages(event.chat_id, set_respond.id)
        return

    session = user_sessions[str(user_id)].get('session')
    if not session:
        set_respond = await event.reply("[x] Session tidak ditemukan, /login lagi sayangku")
        await asyncio.sleep(5)
        set_respond = await bot.delete_messages(event.chat_id, set_respond.id)
        return

    if event.raw_text == '/send':
           pontol = await event.respond(f'{usage}/send grup1 (1 grup)\n\n-- Multiple Group--\n{usage}/send grup1, grip2, grup3, dst..\n\nDiharuskan pakai tanda koma (,)')
           await asyncio.sleep(5)
           await pontol.delete()
           return

    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.start()

    try:
        parts = event.raw_text[len('/send'):].strip()

        message = user_sessions[str(user_id)]['pesan']

        groups = parts.split(',')
        status_send[user_id] = False
        sended[user_id] = True

        if user_id not in groups_session or not groups_session[user_id] == groups:
           groups_session[user_id] = groups
        else:
           groups_session[user_id] += groups

        grups = user_sessions[str(user_id)]['grups'] = groups_session[user_id]

        print(f'{groups_session[user_id]} group sesi uid')

        await asyncio.gather(*[send_pesan(client, event, pesan, group, user_id) for group in groups_session[user_id]])

        if not status_send[user_id]:
            await event.respond("[✓] Selesai mengirim pesan ke semua grup.")

    except Exception as e:
        await event.respond(f'[x] Terjadi kesalahan: {e}')

    finally:
        if not status_send[user_id]:
            await event.respond("[-] Durasi sudah habis, Jika ingin perpaniang silahkan dm @SamiodeSolvoid\nTerimakasih sudah order dengan kami :)\n\n- __Userbot by @CamiodeSolvoid__")
            await client.disconnect()

@bot.on(events.NewMessage(pattern='/remove'))
async def remove_pesan(event):
    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False
    for key, session_data in user_sessions.items():
        if key == str(user_id):
            sessions_found = True

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    if user_id not in sended or sended[user_id] == False:
        await event.respond("[x] Kamu belum mengirim pesan apapun, harap kirim dengan /send")
        return

    if user_id not in status_send or status_send[user_id] == False:
        await event.reply("[x] Untuk menjalankan command ini, harap /stop terlebih dahulu.")
        return

    try:
       remove_ = event.raw_text[len('/remove '):].strip()
       if not remove_:
           await event.respond(f'{usage}/remove (grup) atau /remove grup1, grup2, grup3')
           return

       removed_groups = remove_.split(',')

       if user_id in groups_session:
            current_groups = groups_session[user_id]
            for group in removed_groups:
                group = group.strip()
                if group in current_groups:
                    current_groups.remove(group)
                    await event.reply(f"[✓] Grup {group} berhasil diremove.")
                else:
                    await event.reply(f"[x] Grup {group} tidak ada dalam list.")
            groups_session[user_id] = current_groups
       else:
            await event.respond("[x] Kamu tidak memiliki daftar grup aktif.")

    except Exception as e:
        await event.respond(f'[x] Terjadi kesalahan: {e}')

@bot.on(events.NewMessage(pattern='/setjeda'))
async def stop_send(event):
    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False
    for key, session_data in user_sessions.items():
        if key == str(user_id):
            sessions_found = True

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    try:
        parts = event.raw_text.split()
        if len(parts) != 2:
            await event.reply(f'{usage}/setjeda (detik), default 120 detik')
            return

        command, jeda_ = parts

        jeda_ = int(jeda_)
        if jeda_ < 0:
            await event.respond("[x] jeda tidak boleh kurang dari 30 detik.")
        else:
            user_sessions[str(user_id)]['jeda'] = jeda_
            save_session(user_id, user_sessions[str(user_id)])

            await event.respond(f'[✓] Berhasil memperbarui jeda ke {jeda_} detik.')

    except ValueError:
        await event.respond(f'{usage}/setjeda (detik)')
    except Exception as e:
        await event.respond(f"[x] Terjadi kesalahan: {e}")

@bot.on(events.NewMessage(pattern='/stop'))
async def stop_send(event):
    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False
    for key, session_data in user_sessions.items():
        if key == str(user_id):
            sessions_found = True

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    if user_id not in sended or not sended[user_id]:
        await event.respond("[x] Kamu belum mengirim pesan apapun, harap kirim dengan /send")
        return

    status_send[user_id] = True
    stop_msg = await event.reply("[...] Loading... harap tunggu")
    if status_send[user_id] == True:
       await stop_msg.delete()

@bot.on(events.NewMessage(pattern='/resume'))
async def resume_send(event):
    global status_send

    user_id = event.sender_id

    user_sessions = load_sessions()
    sessions_found = False
    for key, session_data in user_sessions.items():
        if key == str(user_id):
            sessions_found = True

    if not sessions_found:
        await event.respond(f'{log_txt}')
        return

    if sended[user_id] == False:
        await event.respond("[x] Kamu belum mengirim pesan apapun, harap kirim dengan /send")
        return

    status_send[user_id] = False
    session = user_sessions[str(user_id)].get('session')
    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.start()

    wait_message = "[...] Loading... Harap tunggu"
    wait_messages = await event.respond(wait_message)

    pesan = user_sessions[str(user_id)]['pesan']

    await asyncio.sleep(2)
    await wait_messages.delete()
    await event.respond("[✓] Berhasil melanjutkan pengiriman pesan.\n/stop untuk menghentikan")

    await asyncio.gather(*[send_pesan(client, event, pesan, group, user_id) for group in groups])

    await event.respond("[✓] Berhasil melanjutkan pengiriman pesan, /stop untuk melanjutkan")

@bot.on(events.NewMessage(pattern='/edit_message'))
async def edit_message(event):
    params = event.raw_text.split(' ')
    if len(params) < 3:
        await event.respond("Usage: /edit_message <message_id> <new_message>")
        return

    try:
        message_id = int(params[1])
        new_message = ' '.join(params[2:])
        if datetime.now() - edit_cooldown[message_id] < timedelta(minutes=1):
            await event.respond("Cooldown for editing message. Wait for a while before editing again.")
            return
        await event.respond(f"Editing message {message_id} to: {new_message}")
        await client(EditMessageRequest(event.chat_id, message_id, message=new_message))
        edit_cooldown[message_id] = datetime.now()
    except ValueError:
        await event.respond("Invalid message ID. Usage: /edit_message <message_id> <new_message>")
    except Exception as e:
        await event.respond(f"Failed to edit message: {e}")

@bot.on(events.NewMessage(pattern='/edit_group_name'))
async def edit_group_name(event):
    params = event.raw_text.split(' ')
    if len(params) < 3:
        await event.respond("Usage: /edit_group_name <group_id> <new_name>")
        return

    try:
        group_id = int(params[1])
        new_name = ' '.join(params[2:])
        await event.respond(f"Editing group {group_id} name to: {new_name}")
        await client(EditAdminRequest(event.chat_id, 'me', title=new_name))
    except ValueError:
        await event.respond("Invalid group ID. Usage: /edit_group_name <group_id> <new_name>")
    except Exception as e:
        await event.respond(f"Failed to edit group name: {e}")

def run_server():
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(('0.0.0.0', 8000), handler)
    print("HTTP server is running on port 8000")
    httpd.serve_forever()

async def main():
    await bot.start()
    print("╰┈➤ Camio bot is up, made by @CamioDeSolvoid")
    await bot.run_until_disconnected()
if __name__ == "__main__":
    asyncio.run(main())
    #run_server()
