
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.filters import Command
from aiogram.enums import ChatMemberStatus
from aiogram.client.default import DefaultBotProperties

# ==========================
# ДАННЫЕ БЕРУТСЯ ИЗ ENV
# ==========================

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
FILE_NAME = "Дьявол.1_merged.pdf"   # Замени на название своего файла

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
    ]
)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        f"👋 <b>Чтобы получить файл:</b>\n\n"
        f"1️⃣ Подпишитесь на канал:\n"
        f"https://t.me/{CHANNEL_USERNAME[1:]}\n\n"
        f"2️⃣ Нажмите кнопку ниже 👇"
    )
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"[LOG] Статус пользователя {user_id}: {member.status}")  # Логируем статус

        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]:
            file = InputFile(FILE_NAME)
            await callback.message.answer_document(file)
            await callback.answer("Файл отправлен ✅")
        else:
            await callback.answer("Вы не подписаны ❌", show_alert=True)

    except Exception as e:
        await callback.answer("Ошибка проверки ❌", show_alert=True)
        print(f"[ERROR] Ошибка проверки подписки для пользователя {user_id}: {e}")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
