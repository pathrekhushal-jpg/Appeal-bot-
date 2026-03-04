import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 123456789
GROUP_ID = -1001234567890

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Agar aap mute ya ban hue ho to /appeal likho.")

@bot.message_handler(commands=['appeal'])
def ask_reason(message):
    msg = bot.reply_to(message, "Apni appeal ka reason likho:")
    bot.register_next_step_handler(msg, process_reason)

def process_reason(message):
    user_id = message.from_user.id
    username = message.from_user.username
    reason = message.text

    markup = InlineKeyboardMarkup()
    approve_btn = InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}")
    reject_btn = InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
    markup.add(approve_btn, reject_btn)

    bot.send_message(
        ADMIN_ID,
        f"📩 New Appeal\n\nUser: @{username}\nID: {user_id}\nReason: {reason}",
        reply_markup=markup
    )

    bot.reply_to(message, "✅ Aapki appeal admin ko bhej di gayi hai.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data.split("_")
    action = data[0]
    user_id = int(data[1])

    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Sirf admin use kar sakta hai.")
        return

    if action == "approve":
        bot.unban_chat_member(GROUP_ID, user_id)
        bot.send_message(user_id, "🎉 Aapki appeal approve ho gayi hai. Ab aap group join kar sakte ho.")
        bot.edit_message_text("✅ Appeal Approved", call.message.chat.id, call.message.message_id)

    elif action == "reject":
        bot.send_message(user_id, "❌ Aapki appeal reject ho gayi hai.")
        bot.edit_message_text("❌ Appeal Rejected", call.message.chat.id, call.message.message_id)

bot.polling()
