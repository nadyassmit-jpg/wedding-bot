import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "СЮДА_ТОКЕН_БОТА"
ADMIN_ID = 123456789
ADMIN_USERNAME = "naivaen"

# Обложки
START_PHOTO = "FILE_ID_ФОТО_СТАРТ"
JOURNAL_PHOTO = "FILE_ID_ФОТО_ЖУРНАЛА"
CHANNEL_ANIMATION = "FILE_ID_ГИФ_КАНАЛА"

JOURNAL_PRICE = "2 600 ₽"
CHANNEL_PRICE = "390 ₽"

CARD = "89503091950 Т-Банк"
HOLDER = "Надежда И."
# =============================================

logging.basicConfig(level=logging.INFO)
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# ---------------- КЛАВИАТУРЫ ----------------
def kb_main():
    kb = InlineKeyboardBuilder()
    kb.button(text="📖 Журнал для невесты", callback_data="about:journal")
    kb.button(text="💌 Канал с полезностями", callback_data="about:channel")
    kb.adjust(1)
    return kb.as_markup()


def kb_about(p):
    kb = InlineKeyboardBuilder()
    kb.button(text="Получить доступ", callback_data=f"pay:{p}")
    kb.button(text="← Назад", callback_data="back")
    kb.adjust(1)
    return kb.as_markup()


def kb_send_receipt():
    kb = InlineKeyboardBuilder()
    kb.button(
        text=f"📩 Отправить чек @{ADMIN_USERNAME}",
        url=f"https://t.me/{ADMIN_USERNAME}",
    )
    return kb.as_markup()


# ---------------- ТЕКСТЫ ----------------
START_TEXT = (
    "Привет 🤍\n\n"
    "Вы меня знаете как <b>@nadyaivukova</b>, "
    "а для своих — просто Надя.\n\n"
    "Я собрала здесь свой опыт, насмотренность, "
    "полезные контакты и вдохновение, "
    "а точнее всё, что обычно остаётся за кадром.\n\n"
    "📖 <b>Журнал для невесты</b>\n"
    "Больше 100 страниц с идеями, локациями Казани, "
    "сценариями дня и полезными контактами — "
    "от организаторов до визажиста и поиска референсов. "
    "Без воды, только все самое главное.\n"
    "Это закрытое издание, которое я полностью создала с нуля, "
    "раньше я его отправляла только своим парам, "
    "чтобы облегчить подготовку и поиски, "
    "также добавила сейчас фотографов из Казани "
    "с близким мне видением.\n\n"
    "💌 <b>Канал с полезностями и вдохновением</b>\n"
    "Мое личное хранилище визуального свадебного вдохновения, "
    "вообщем отрываю от сердца (также раньше доступ открывала "
    "только своим невестам), а сейчас вход как чашка кофе. "
    "Это личное пространство, с моим видением. "
    "Здесь собираю то, что не гуглится и не публикуется "
    "в открытых подборках, потихоньку вылавливаю "
    "и подсматриваю в разных источниках.\n\n"
    "Оба продукта — закрытые.\n"
    "Эта информация собиралась годами и собирается по сей день. "
    "Она остаётся у тех, кто ценит своё время "
    "и хочет подготовиться спокойно, красиво и без хаоса.\n\n"
    "Про что рассказать подробнее?"
)

JOURNAL_TEXT = (
    "📖 <b>Журнал для невесты</b>\n\n"
    "На подготовку к свадьбе уходят сотни решений. "
    "Образ, букет, локации, детали, тайминг, подрядчики. "
    "И хорошо, если есть с кем посоветоваться.\n\n"
    "Я собрала журнал, который сама хотела бы получить "
    "в этот момент, чтобы не теряться, не гуглить ночами "
    "и не сомневаться в каждом выборе.\n\n"
    "Внутри — то, что действительно работает:\n\n"
    "01 · о чём я снимаю, как вижу этот день\n"
    "02 · про образы невесты и жениха\n"
    "03 · сборка букета и советы\n"
    "04 · локации Казани и за городом!\n"
    "05 · про сценарий дня (как сделать удобно)\n"
    "06 · почему плёнка не страшно?\n"
    "07 · полезные контакты "
    "(даже фотографы, которым я доверяю сама)\n\n"
    "Особенно люблю раздел о идейных вдохновителях, "
    "про то, что рекомендую и выбрала бы сама как фотограф."
)

CHANNEL_TEXT = (
    "💌 <b>Канал с полезностями и вдохновением</b>\n\n"
    "Закрытый канал для невест. "
    "То, что помогает готовиться к свадьбе спокойно и красиво.\n\n"
    "Это мое личное пространство: с вдохновением, "
    "находками и поддержкой, которых не найти "
    "в открытом доступе, своего рода эксклюзив!\n\n"
    "<b>Внутри:</b>\n\n"
    "— вдохновение и референсы\n"
    "— полезные находки\n"
    "— идеи для подготовки\n"
    "— поддержка и атмосфера"
)


# ---------------- ЭКРАН 1: /start ----------------
@dp.message(CommandStart())
async def start(m: Message):
    u = m.from_user
    await bot.send_message(
        ADMIN_ID,
        f"👤 Новый визит\n"
        f"{u.full_name} | <code>{u.id}</code> | @{u.username or '—'}"
    )
    await m.answer_photo(photo=START_PHOTO)
    await m.answer(START_TEXT, reply_markup=kb_main())


# ---------------- НАЗАД ----------------
@dp.callback_query(F.data == "back")
async def back(c: CallbackQuery):
    try:
        await c.message.delete()
    except Exception:
        pass
    await c.message.answer_photo(photo=START_PHOTO)
    await c.message.answer(
        "Про что рассказать подробнее?",
        reply_markup=kb_main(),
    )
    await c.answer()


# ---------------- ЭКРАН 2: О товаре ----------------
@dp.callback_query(F.data.startswith("about:"))
async def about(c: CallbackQuery):
    p = c.data.split(":")[1]

    try:
        await c.message.delete()
    except Exception:
        pass

    if p == "journal":
        await c.message.answer_photo(photo=JOURNAL_PHOTO)
        await c.message.answer(JOURNAL_TEXT, reply_markup=kb_about(p))
    else:
        await c.message.answer_animation(animation=CHANNEL_ANIMATION)
        await c.message.answer(CHANNEL_TEXT, reply_markup=kb_about(p))

    await c.answer()


# ---------------- ЭКРАН 3: Реквизиты ----------------
@dp.callback_query(F.data.startswith("pay:"))
async def pay(c: CallbackQuery):
    p = c.data.split(":")[1]
    title, price = (
        ("Журнал для невесты", JOURNAL_PRICE)
        if p == "journal"
        else ("Доступ в канал", CHANNEL_PRICE)
    )
    product_word = "журнал" if p == "journal" else "доступ в канал"

    try:
        await c.message.delete()
    except Exception:
        pass

    await c.message.answer(
        f"<b>{title} — {price}</b>\n\n"
        f"💳 {CARD}\n"
        f"Получатель: {HOLDER}\n\n"
        "⚠️ <b>Оплата невозвратная.</b>\n\n"
        "После перевода отправьте чек мне в личные сообщения "
        f"<b>@{ADMIN_USERNAME}</b> и напишите «оплачено».\n\n"
        f"Я подтвержу оплату и пришлю {product_word}. 🤍",
        reply_markup=kb_send_receipt(),
    )
    await c.answer()


# ---------------- СЛОВО «ОПЛАЧЕНО» ----------------
@dp.message(F.text.lower() == "оплачено")
async def paid_word(m: Message):
    await m.answer(
        "Спасибо 🤍\n\n"
        f"Если вы ещё не отправили чек — пришлите его "
        f"мне в личку: @{ADMIN_USERNAME}\n\n"
        "После проверки я пришлю ваш заказ."
    )


# ---------------- /myid ----------------
@dp.message(F.text == "/myid")
async def myid(m: Message):
    await m.answer(f"Ваш ID: <code>{m.from_user.id}</code>")


# ---------------- ЗАПУСК ----------------
async def main():
    print("Бот запущен.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
