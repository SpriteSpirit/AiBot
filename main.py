import requests
import telebot

from model import get_class

# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot("8610982848:AAH2Yp6urZAG0d2HrNVguCpne-3_AQNTQSg")


def get_duck_image_url():
    """
        Получает рандомную картинку с сайта
    """
    url = "https://random-d.uk/api/random"
    result = requests.get(url).json()

    return result


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я твой Telegram бот. Отправь мне изображение уток. Я проанализирую изображение. Используй команду /duck",
    )


@bot.message_handler(commands=["duck"])
def duck(message):
    """
        Возвращает фото утки
    """
    image_url = get_duck_image_url()
    bot.send_message(message.chat.id, image_url)


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    """
        Обрабатывает изображение и анализиует его
    """
    # Проверка, что фото есть
    if not message.photo:
        return bot.send_message(message.chat.id, "Нет изображения. Отправь в чат картинку с утками.")

    # Получам файл и сохраняем
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    # Получить файл и звгрузить
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Анализ изображения
    result = get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=file_name)
    bot.send_message(message.chat.id, result)


# Запускаем бота
bot.polling()
