import telebot
from telebot import types
from datetime import datetime
import pickle

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('6819371147:AAF2nHhkshkODKPg8ui15oj_tjrC0exDnYs')

# Загрузка данных из файла
try:
    with open('user_data.pkl', 'rb') as file:
        user_data = pickle.load(file)
except FileNotFoundError:
    user_data = {}

# Функция отображения меню с действиями
def show_actions_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    actions = ["Пришел на работу", "Ушел с работы", "Пошел на перекур", "Вернулся с перекура"]
    markup.add(*[types.KeyboardButton(action) for action in actions])

    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)

# Функция сохранения данных пользователя
def save_user_data(user_id, username, last_action):
    user_data[user_id] = {'username': username, 'last_action': last_action}

    # Сохранение данных в файл
    with open('user_data.pkl', 'wb') as file:
        pickle.dump(user_data, file)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id in user_data:
        bot.send_message(message.chat.id, f"Привет! Ты уже зарегистрирован(а) как {user_data[user_id]['username']}.")
        show_actions_menu(message)
    else:
        # Если имя пользователя из профиля не доступно, используем 'Нет имени'
        username = f"@{message.from_user.username}" if message.from_user.username else "Нет имени"
        save_user_data(user_id, username, None)
        bot.send_message(message.chat.id, f"Привет! Теперь ты зарегистрирован(а) как {username}.")
        show_actions_menu(message)

# Обработка выбора действия в личном чате
@bot.message_handler(func=lambda message: message.text in ["Пришел на работу", "Ушел с работы", "Пошел на перекур", "Вернулся с перекура"])
def handle_action(message):
    user_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь
    if user_id in user_data:
        last_action = message.text

        # Получаем время сообщения в UTC и преобразуем в формат времени Телеграма
        message_time_utc = datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')

        # Отправляем информацию в канал (замените 'YOUR_CHANNEL_NAME' на имя вашего канала)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message_text = f"Имя пользователя: {user_data[user_id]['username']}\nДействие: {last_action}\nВремя: {current_time}"
        bot.send_message(chat_id='@kto_gde_i_kogda', text=message_text, parse_mode='Markdown')

        # Отправляем благодарность пользователю
        bot.send_message(message.chat.id, "Спасибо! Штрафа не будет 😄")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован. Напиши /start для регистрации.")

# Запуск бота
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка: {e}")
