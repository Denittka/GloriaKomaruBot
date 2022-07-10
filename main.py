from telebot import TeleBot
import sqlite3

bot = TeleBot(open("token.txt", "r").read().strip())

def check_moder(id):
    con = sqlite3.connect("gloria.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM moders WHERE id = %i" % id).fetchall()
    result += cur.execute("SELECT * FROM admins WHERE id = %i" % id).fetchall()
    print(result)
    con.close()
    return not len(result) == 0

@bot.message_handler(commands=['add'])
def add_gloria(message):
    if not check_moder(message.from_user.id):
        bot.reply_to(message, "Только администраторы могут добавлять Глориа.")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Недостаточно аргументов. Укажите количество Глориа.")
        return
    if len(message.text.split()) > 2:
        bot.reply_to(message, "Слишком много аргументов.")
        return
    if message.text.split()[1].isdigit() is False:
        bot.reply_to(message, "Глориа некорректен, пожалуйста, введите число.")
        return
    if message.reply_to_message is None:
        bot.reply_to(message, "Команда должна быть ответом на сообщение.")
        return
    else:
        con = sqlite3.connect("gloria.db")
        cur = con.cursor()
        user = message.reply_to_message.from_user
        result = cur.execute("SELECT * FROM users WHERE id = %i" % user.id).fetchall()
        if len(result) == 0:
            cur.execute("INSERT INTO users VALUES (%i, 0)" % user.id)
            con.commit()
            gloria = int(message.text.split()[1])
        else:
            gloria = result[0][1] + int(message.text.split()[1])
        cur.execute("UPDATE users SET gloria = %i WHERE id = %i" % (gloria, user.id))
        con.commit()
        bot.reply_to(message, "Теперь у пользователя %i Глориа" % gloria)
        con.close()
        return

@bot.message_handler(commands=['change'])
def change_gloria(message):
    if not check_moder(message.from_user.id):
        bot.reply_to(message, "Только администраторы могут менять Глориа.")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Недостаточно аргументов, укажите количество Глориа.")
        return
    if len(message.text.split()) > 2:
        bot.reply_to(message, "Сликшом много аргументов.")
        return
    if message.text.split()[1].isdigit() is False:
        bot.reply_to(message, "Глориа некорректен, пожалуйста, введите число.")
        return
    if message.reply_to_message is None:
        bot.reply_to(message, "Команда должна быть ответом на сообщение.")
        return
    else:
        con = sqlite3.connect("gloria.db")
        cur = con.cursor()
        user = message.reply_to_message.from_user
        result = cur.execute("SELECT * FROM users WHERE id = %i" % user.id).fetchall()
        if len(result) == 0:
            cur.execute("INSERT INTO users VALUES (%i, 0)" % user.id)
            con.commit()
        gloria = int(message.text.split()[1])
        cur.execute("UPDATE users SET gloria = %i WHERE id = %i" % (gloria, user.id))
        con.commit()
        bot.reply_to(message, "Теперь у пользователя %i Глориа" % gloria)
        con.close()
        return

@bot.message_handler(commands=['get'])
def get_gloria(message):
    con = sqlite3.connect("gloria.db")
    cur = con.cursor()
    result = []
    if message.reply_to_message is None:
        result = cur.execute("SELECT * FROM users WHERE id = %i" % message.from_user.id).fetchall()
    else:
        result = cur.execute("SELECT * FROM users WHERE id = %i" % message.reply_to_message.from_user.id).fetchall()
    if len(result) == 0:
        cur.execute("INSERT INTO users VALUES (%i, 0)" % user.id)
        con.commit()
        bot.reply_to(message, "У пользователя 0 Глориа")
    else:
        bot.reply_to(message, "У пользователя %i Глориа" % result[0][1])
    con.close()
    return

@bot.message_handler(commands=['min'])
def min_gloria(message):
    if not check_moder(message.from_user.id):
        bot.reply_to(message, "Посторонись, челядь.")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Так сколько убавлять-то?")
        return
    if len(message.text.split()) > 2:
        bot.reply_to(message, "И что из этого убавлять?..")
        return
    if message.text.split()[1].isdigit() is False:
        bot.reply_to(message, "Мне текст убавлять?..")
        return
    if message.reply_to_message is None:
        bot.reply_to(message, "Должно быть ответом на сообщение пользователя")
        return
    else:
        con = sqlite3.connect("gloria.db")
        cur = con.cursor()
        user = message.reply_to_message.from_user
        result = cur.execute("SELECT * FROM users WHERE id = %i" % user.id).fetchall()
        if len(result) == 0:
            cur.execute("INSERT INTO users VALUES (%i, 0)" % user.id)
            con.commit()
            bot.reply_to(message, "У пользователя и так всё по нулям")
        else:
            gloria = result[0][1] - int(message.text.split()[1])
            if gloria < 0:
                gloria = 0
        cur.execute("UPDATE users SET gloria = %i WHERE id = %i" % (gloria, user.id))
        con.commit()
        bot.reply_to(message, "Теперь у пользователя %i очков чести" % gloria)
        con.close()
        return

@bot.message_handler(commands=['top'])
def top_gloria(message):
    con = sqlite3.connect("gloria.db")
    cur = con.cursor()
    result = list(filter(lambda x: x[1] != 0, cur.execute("SELECT * FROM users ORDER BY gloria").fetchall()[:5]))
    con.close()
    if len(result) == 0:
        bot.reply_to(message, "Нет никого")
        return
    to_reply = "ТОП 5 ПОЛЬЗОВАТЕЛЕЙ:\n"
    for i in range(len(result)):
        user = bot.get_chat(result[i][0])
        to_reply += "%i. %s %s: %i очков\n" % (i + 1, user.first_name, user.last_name, result[i][1])
    bot.reply_to(message, to_reply)
    return

@bot.message_handler(commands=['help'])
def help_gloria(message):
    to_reply = "Всё просто. /add - добавляет, /min - вычитает, /change - заменяет. Эти команды должны быть ответом на сообщение пользователя и содержать только число очков.\n\n/get работает или на себя (просто прописывается), или на другого пользователя (пересылается сообщение пользователя).\n\nЕсть также /top - топ 5 пользователей, /start - приветственное сообщение, /help - текущая справка. Всё, получается.\n\nДля админов: /new - добавляет нового админа, чьё сообщение пересылается. /del - удаляет текущего."
    bot.reply_to(message, to_reply)

@bot.message_handler(commands=['new'])
def new_admin(message):
    con = sqlite3.connect("gloria.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM admins WHERE id = %i" % message.from_user.id).fetchall()
    if len(result) == 0:
        bot.reply_to(message, "Вы не находитесь в списке администраторов.")
        con.close()
        return
    if message.reply_to_message is None:
        bot.reply_to(message, "Команда должна быть ответом на сообщение.")
        con.close()
        return
    result = cur.execute("SELECT * FROM moders WHERE id = %i" % message.reply_to_message.from_user.id).fetchall()
    if len(result) != 0:
        bot.reply_to(message, "Этот пользователь уже является администратором.")
        con.close()
        return
    cur.execute("INSERT INTO moders VALUES (%i);" % message.reply_to_message.from_user.id)
    con.commit()
    bot.reply_to(message, "Администратор успешно добавлен.")
    con.close()
    return

@bot.message_handler(commands=['del'])
def del_admin(message):
    con = sqlite3.connect("gloria.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM admins WHERE id = %i" % message.from_user.id).fetchall()
    if len(result) == 0:
        bot.reply_to(message, "Вы не находитесь в списке администраторов.")
        con.close()
        return
    if message.reply_to_message is None:
        bot.reply_to(message, "Команда должна быть ответом на сообщение.")
        con.close()
        return
    result = cur.execute("SELECT * FROM moders WHERE id = %i" % message.reply_to_message.from_user.id).fetchall()
    if len(result) == 0:
        bot.reply_to(message, "Этот пользователь не является администратором.")
        con.close()
        return
    cur.execute("DELETE FROM moders WHERE id = %i;" % message.reply_to_message.from_user.id)
    con.commit()
    bot.reply_to(message, "Администратор успешно удалён.")
    con.close()
    return

bot.infinity_polling()
