from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
import os
import asyncio
from dotenv import load_dotenv
import math

load_dotenv()
key = os.getenv('KEY_BOT_API')
username = os.getenv('KEY_BOT_USERNAME')

TOKEN: Final = key
BOT_USERNAME: Final = username

import yfinance as yf

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    data = yf.Ticker("EURJPY=X")  
    rate = data.history(period="1d")['Close'].iloc[0]
    await context.bot.send_message(chat_id=user_id, text=f'Right now 1 EUR is equal to {rate} JPY, I will tell you when there is a variation of the yen rate.')
    context.user_data['task'] = asyncio.create_task(monitor_rate(update, context, rate))

async def monitor_rate(update: Update, context: ContextTypes.DEFAULT_TYPE, rate: float) -> None:
    user_id = update.message.from_user.id
    while True:
        await asyncio.sleep(90)
        data = yf.Ticker("EURJPY=X")
        newrate = data.history(period="1d")['Close'].iloc[0]
        if newrate - rate >= 1:
            rate = newrate
            await context.bot.send_message(chat_id=user_id, text=f'UPDATE!! Right now 1 EUR is equal to {rate} JPY.')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'task' in context.user_data:
        context.user_data['task'].cancel()
    await asyncio.sleep(0)
    

async def change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    data = yf.Ticker("EURJPY=X")  
    rate = data.history(period="1d")['Close'].iloc[0]
    await context.bot.send_message(chat_id=user_id, text=f'1 EUR is equal to {rate} JPY')


# async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # exec("pkill python3")



def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("change", change))
    app.add_handler(CommandHandler("stop", stop))
    # app.add_handler(CommandHandler("close", close))
    app.run_polling()

if __name__ == '__main__':
    main()

