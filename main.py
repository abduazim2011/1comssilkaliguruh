from telethon import TelegramClient, events
from time import sleep

# =======================
# Настройки Telethon
# =======================
api_id = 28846045
api_hash = '2bfabb13674fe7ecb587937f026db5e6'
session_name = '977838293'  # имя .session файла

client = TelegramClient(session_name, api_id, api_hash)

# =======================
# Переменные бота
# =======================
reply_enabled = True
reply_text = '9860176619018904'  # текст ответа по умолчанию
target_group = None  # username группы без @

# =======================
# Команды из Избранного
# =======================
@client.on(events.NewMessage(chats='me'))
async def favorites_handler(event):
    global reply_enabled, reply_text, target_group
    text = event.message.message.strip()

    try:
        if text.startswith('/gr '):
            target_group = text.split('/gr ')[1].strip()
            await event.reply(f"✅ Группа установлена: {target_group}")

        elif text.startswith('/set_text '):
            reply_text = text.split('/set_text ')[1].strip()
            await event.reply(f"✅ Текст для ответа установлен: {reply_text}")

        elif text == '/off':
            reply_enabled = False
            await event.reply("❌ Авто-ответ отключен")

        elif text == '/on':
            reply_enabled = True
            await event.reply("✅ Авто-ответ включен")

        elif text == '/help':
            help_text = (
                "📌 Команды бота:\n"
                "/gr username — установить группу для отслеживания\n"
                "/set_text текст — установить текст ответа\n"
                "/off — выключить автоответ\n"
                "/on — включить автоответ\n"
                "/info — показать текущие настройки\n"
                "/help — показать это сообщение"
            )
            await event.reply(help_text)

        elif text == '/info':
            status = "включен" if reply_enabled else "выключен"
            info_text = (
                f"ℹ️ Авто-ответ: {status}\n"
                f"Текст ответа: {reply_text}\n"
                f"Группа: {target_group if target_group else 'не установлена'}"
            )
            await event.reply(info_text)
    except Exception as e:
        print(f"⚠️ Ошибка в favorites_handler: {e}")

# =======================
# Автоответ на сообщения из канала
# =======================
@client.on(events.NewMessage)
async def channel_handler(event):
    global reply_enabled, reply_text, target_group

    if not reply_enabled or not target_group:
        return

    try:
        chat_username = getattr(event.chat, 'username', None)
        if chat_username != target_group:
            return

        msg = event.message
        # Проверка, что сообщение — форвард из канала
        if not getattr(msg, 'forward', None) or not getattr(msg.forward, 'original_fwd', None):
            return

        for attempt in range(3):
            try:
                await msg.reply(reply_text)
                print(f"✅ Ответ отправлен в {target_group}")
                break
            except Exception as e:
                print(f"❌ Ошибка попытки {attempt + 1}: {e}")
                sleep(0.5)

    except Exception as e:
        print(f"⚠️ Ошибка в channel_handler: {e}")

# =======================
# Старт бота
# =======================
print("🚀 Бот запущен. Управляй через Избранное...")

try:
    client.start()  # старт через .session, без интерактивного ввода
except Exception as e:
    print("❌ Ошибка запуска клиента:", e)
    exit()

client.run_until_disconnected()
