from telegram.ext import ContextTypes


async def send_hello(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id='470308069',
        text='Привет'
        # text=f'Привет {await context.job.interval}'
    )
    # context.job.interval += 5
    # if context.job.intrval > 15:
    #     await context.bot.send_message(
    #         chat_id='470308069',
    #         text='Выполнено'
    #     )
    #     await context.job.schedule_removal()
