import telebot
import datetime
import os
from decouple import config
import sys
from flask import Flask
# from telebot import types

app = Flask(__name__)
weekdays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}
final_date = ""
saved_dates = {}
current_users = []

TOKEN = os.environ.get("TOKEN") or config("TOKEN")
# chat_id = config("TeamChatId")
chat_id = os.environ.get("TeamChatId") or config("TeamChatId")


tb = telebot.TeleBot(TOKEN)	#create a new Telegram Bot object
types = telebot.types
print("Telegram Bot is running...")


@tb.message_handler(commands=["currentUsers"])
def get_current_users(message):
    result_str = "<b> Current Users Voting</b>\n"
    for user in current_users:
        result_str += f"<i>{user}</i>\n"
    tb.send_message(chat_id, text=result_str, parse_mode="html")


@tb.message_handler(commands=["help", "start"])
def send_help(message):
    try:
        result_str = f"<b>NOTIFICATION!</b>\n<b><i>{message.from_user.username}</i></b> has joined the voting! Don't leave them out. :)"
        personal_str = f"<b> Welcome to Team Calendar Bot, <i>{message.from_user.username}</i></b> \n Use /dates to choose dates.\nUse /remove to remove dates.\nUse /status to check everyone's availability\nUse /removeKB to remove keyboard symbol\nUse /finalise to view the best date for everyone.\nUse /currentUsers to view everyone in the votes."

        tb.send_message(chat_id, text=result_str, parse_mode="html")
        tb.send_message(message.from_user.id, text=personal_str, parse_mode="html")

        if message.from_user.username not in current_users:
            current_users.append(message.from_user.username)

    except Exception as e:
        print(f"Oops! There was an error', {e.__class__}")
        tb.send_message(chat_id, text="Go to https://t.me/team_calendar_bot and press 'start' in order for Bot to interact with you!", parse_mode="html")

@tb.message_handler(commands=["removeKB"])
def removeEverything(message):
    try:
        tb.send_message(message.from_user.id, text="The keyboard symbol has been removed now. Use /dates to choose dates again!",
                    reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        print(f"Oops! There was an error', {e.__class__}")
        tb.send_message(chat_id, text="Go to https://t.me/team_calendar_bot and press 'start' in order for Bot to interact with you!", parse_mode="html")

@tb.message_handler(commands=["finalise"])
def reply_final_date(message):
    highest_count = 0
    best_date = "None selected, friends!"
    for date, people in saved_dates.items():
        count = len(people)
        if count > highest_count:
            highest_count = count
            best_date = date

    tb.send_message(chat_id, "Everyone's best date: " + "<b>" + best_date + "</b>", parse_mode="html")

@tb.message_handler(commands=["status"])
def retrieve_status(message):
    try:
        result_str = "<b><i>VOTING STATUS</i></b>"
        result_str += "\n" + "\n"
        for date, people in saved_dates.items():
            result_str += f"<b><u>{date}</u></b>" + "\n"

            for person in people:
                result_str += f"<i>{person}</i>" + "\n"
            result_str += "\n"

        tb.send_message(chat_id, result_str, parse_mode="html")
        tb.send_message(message.from_user.id, result_str, parse_mode="html")

    except Exception as e:
        print(f"Oops! There was an error', {e.__class__}")
        tb.send_message(chat_id, text="Go to https://t.me/team_calendar_bot and press 'start' in order for Bot to interact with you!")

@tb.message_handler(commands=["remove"])
def remove_date(message):
    try:
        showRemove = False
        if message.text == "/remove":
            for date, people in saved_dates.items():
                if message.from_user.username in people:
                    showRemove = True
                    break 
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
            next_week_dates = []

            for date, people in saved_dates.items():
                if message.from_user.username in people:
                    final_str = date + " REMOVE"
                    next_week_dates.append(final_str)

            for date in next_week_dates:
                itembtn = types.KeyboardButton(date)
                markup.add(itembtn)

            if showRemove:
                tb.send_message(message.from_user.id, "Remove your previous appointed date.", reply_markup=markup)
            else:
                tb.send_message(message.from_user.id, "You have not selected any dates. Use /dates to select dates.", reply_markup=markup)
            
        return True

    except Exception as e:
        print(f"Oops! There was an error', {e.__class__}")
        tb.send_message(chat_id, text="Go to https://t.me/team_calendar_bot and press 'start' in order for Bot to interact with you!")


@tb.message_handler(commands=["dates"])
def get_dates(message):
    items_list = []
    try:
        if message.text == "/dates":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True, row_width=2)
            next_week_dates = []
            for i in range(1, 8):
                datetime_obj = datetime.datetime.now() + datetime.timedelta(days=i)

                day_number = datetime_obj.weekday()
                datetime_str = str(datetime_obj)
                date_only = datetime_str.split(" ")[0]
                final_str = date_only + " " + weekdays[day_number]
                next_week_dates.append(final_str)
            
            for date in next_week_dates:
                itembtn = types.KeyboardButton(date)
                items_list.append(itembtn)

            markup.row(items_list[0], items_list[1])
            markup.row(items_list[2], items_list[3])
            markup.row(items_list[4], items_list[5])
            markup.row(items_list[6])

            tb.send_message(message.from_user.id, "<b> Choose your dates: </b>", reply_markup=markup, parse_mode="html")
        else:
            remove_date(message)

        return True
    except Exception as e:
        print(f"Oops! There was an error', {e.__class__}")
        tb.send_message(chat_id, text="Go to https://t.me/team_calendar_bot and press 'start' in order for Bot to interact with you!")


@tb.message_handler(func=lambda m: True)
def echo_all(message):

    # If user wants to remove...
    if "REMOVE" in message.text:
        date_split = message.text.split(" ")[0:2]
        date = " ".join(date_split)

        # Show users only the dates he/she have choosen.
        for date, people in saved_dates.items():
            for i in range(len(people)):
                if people[i] == message.from_user.username:
                    people.pop(i)
                    if len(people) == 0:
                        saved_dates.pop(date, None)
                    tb.reply_to(message, "This date has been removed.")
                    return

    elif "/credentials" in message.text:
        pass 
    # retrieve calenderId 
    # sendToGoogleCalendar(calendarId)

    # If user wants to add new dates..
    else:
        for weekday in weekdays.values():
                if weekday in message.text:
                    reply = True 
                    break
                else:
                    reply = False
        if reply:
            date = message.text
            
            if date in saved_dates.keys():
                if message.from_user.username not in saved_dates[date]:
                    # saved_dates[date] += 1
                    saved_dates[date].append(message.from_user.username)
                else:
                    tb.reply_to(message, f"You have selected {date} before. Use /remove to remove the date.")
                    return
            else:
                saved_dates[date] = [message.from_user.username]
            
            tb.reply_to(message, "Your date has been successfully added into the selection. Use /status to check.")


tb.polling()
if __name__ == "__main__":
    app.run(debug=True, port=8051, host="0.0.0.0")