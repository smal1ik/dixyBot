import os
from datetime import timedelta

from aiogram.filters.command import Command
from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext

from app import utils
from app.database.requests import *
from decouple import config
import app.keyboards as kb
from app.state import Admin

router_main = Router()
admin_id = 654557598

@router_main.message(Command("start"))
async def message(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    if user_id == admin_id:
        await message.answer("Админка", reply_markup=kb.menu_btn)

@router_main.callback_query(F.data == 'statistics')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    stats = await get_statistics()
    msg = f"""Всего комментариев по шаблону: {stats[0] + stats[1]}
Количество ответов: {stats[0]}
Количество ошибок: {stats[1]}
"""
    await callback.message.answer(msg)
    await callback.message.answer("Админка", reply_markup=kb.menu_btn)

@router_main.callback_query(F.data == 'menu')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Админка", reply_markup=kb.menu_btn)


@router_main.callback_query(F.data == 'chat')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Кидай", reply_markup=kb.back_btn)
    await state.set_state(Admin.CHAT)



@router_main.message(Admin.CHAT)
async def message(message: types.Message, bot: Bot, state: FSMContext):
    os.environ["ID_CHAT"] = message.text
    with open("settings.ini", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        lines[7] = f'ID_CHAT={message.text}\n'
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)
    await state.set_state(Admin.ADMIN)
    await message.answer("Админка", reply_markup=kb.menu_btn)

@router_main.callback_query(F.data == 'post')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Кидай", reply_markup=kb.back_btn)
    await state.set_state(Admin.POST)


@router_main.message(Admin.POST)
async def message(message: types.Message, bot: Bot, state: FSMContext):
    os.environ["ID_POST"] = message.text
    with open("settings.ini", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        lines[8] = f'ID_POST={message.text}\n'
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)
    await state.set_state(Admin.ADMIN)
    await message.answer("Админка", reply_markup=kb.menu_btn)


@router_main.callback_query(F.data == 'words')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Кидай", reply_markup=kb.back_btn)
    await state.set_state(Admin.WORDS)


@router_main.message(Admin.WORDS)
async def message(message: types.Message, bot: Bot, state: FSMContext):
    os.environ["WORDS"] = message.text
    with open("settings.ini", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        lines[11] = f'WORDS={message.text}\n'
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)
    await state.set_state(Admin.ADMIN)
    await message.answer("Админка", reply_markup=kb.menu_btn)

@router_main.callback_query(F.data == 'prompt')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Кидай", reply_markup=kb.back_btn)
    await state.set_state(Admin.PROMPT)


@router_main.message(Admin.PROMPT)
async def message(message: types.Message, bot: Bot, state: FSMContext):
    prompt = message.text.split("\n")
    prompt = [elem+"\n" for elem in prompt]

    os.environ["GPT_PROMPT"] = str(prompt)
    with open("settings.ini", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        lines[12] = f'GPT_PROMPT={prompt}\n'
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)
    await state.set_state(Admin.ADMIN)
    await message.answer("Админка", reply_markup=kb.menu_btn)

@router_main.callback_query(F.data == 'tokens')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Кидай", reply_markup=kb.back_btn)
    await state.set_state(Admin.TOKEN)

@router_main.message(Admin.TOKEN)
async def message(message: types.Message, bot: Bot, state: FSMContext):
    os.environ["MAX_TOKENS"] = message.text
    with open("settings.ini", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        lines[10] = f'MAX_TOKENS={message.text}'
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)
    await state.set_state(Admin.ADMIN)
    await message.answer("Админка", reply_markup=kb.menu_btn)

@router_main.callback_query(F.data == 'temperature')
async def callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Кидай", reply_markup=kb.back_btn)
    await state.set_state(Admin.TEMPERATURE)


@router_main.message(Admin.TEMPERATURE)
async def message(message: types.Message, bot: Bot, state: FSMContext):
    os.environ["TEMPERATURE"] = message.text
    with open("settings.ini", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        lines[9] = f'TEMPERATURE={message.text}\n'
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)
    await state.set_state(Admin.ADMIN)
    await message.answer("Админка", reply_markup=kb.menu_btn)


@router_main.message(F.text)
async def message(message: types.Message, bot: Bot):
    if message.chat.id == config("ID_CHAT", cast=int) and message.message_thread_id == config("ID_POST", cast=int):
        # print("ID чата:", message.chat.id)
        # print("ID поста:", message.message_thread_id)
        # print("ID сообщения:", message.message_id)
        text = message.text
        if config("WORDS").lower() in text.lower():
            answer = await utils.send_chatgpt(text)
            if answer is None:
                return
            link = utils.send_dixy(answer)
            if link is None:
                return
            await bot.send_message(text=link, reply_to_message_id=message.message_id, chat_id=message.chat.id, disable_web_page_preview=True)



