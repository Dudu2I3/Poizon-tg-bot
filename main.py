import telebot
from telebot import types
import sqlite3
import course

bot = telebot.TeleBot("6537480455:AAEvOeILcTOkxj-BNJpRnn2sQ8AscWfd7AM")

# Словарь для стоимости доставки
delivery_costs = {
    "summer_shoes": 1800 + 2700,
    "winter_shoes": 2000 + 3000,
    "outerwear": 2000 + 2400,
    "hoodie": 1700 + 1500,
    "pants": 1700 + 1500,
    "jacket": 1750 + 1650,
    "shirt": 1500 + 1300,
    "underwear": 1200 + 900,
    "accessories": 1000 + 1500,
    "technic": 2200 + 3000,
}

# Глобальная переменная для хранения стоимости доставки
delivery_cost = 0
article = None
size = None
price = None
name = None
number = None
town = None


# Функция для расчета цены товара
def cost_order(message):
    # Глобальная переменная для хранения стоимости доставки
    global delivery_cost

    try:
        # Пробуем преобразовать введенное значение в целое число
        amount = int(message.text.strip())
    except ValueError:
        # Если не удалось преобразовать, сообщаем об ошибке и повторяем запрос
        bot.send_message(message.chat.id, "Неверный формат, попробуйте снова")
        bot.register_next_step_handler(message, cost_order)
        return

    # Проверка на неотрицательное значение суммы
    if amount >= 0:
        # Создание клавиатуры для ответа с кнопками "Меню" и "Рассчитать заново"
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Меню", callback_data="menu")
        button2 = types.InlineKeyboardButton("Рассчитать заново", callback_data="calculator")
        markup.row(button1, button2)

        # Расчет стоимости с учетом курса и доставки
        cost = round(amount * course.online_course() + 0.5) + delivery_cost

        # Отправка сообщения с итоговой стоимостью и кнопками
        bot.send_message(message.chat.id, f"💰 Итоговая стоимость <b>{cost}</b> рублей с доставкой до России.\n\n🚛 Доставка "
                                          f"<b>СДЭК</b>ом или <b>Почтой России</b> из Москвы до Вашего пункта выдачи "
                                          f"оплачивается отдельно! \nДоставка по Москве бесплатно!", reply_markup=markup,parse_mode='html')
    else:
        # Если введена отрицательная сумма, сообщаем об ошибке и повторяем запрос
        bot.send_message(message.chat.id, "Цена не должна быть отрицательной, попробуйте снова")
        bot.register_next_step_handler(message, cost_order)


# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру для сообщения с единственной кнопкой "Меню"
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Меню", callback_data="menu")
    markup.row(button1)

    # Отправляем приветственное сообщение с информацией о магазине и приглашением к использованию клавиатуры
    bot.send_message(message.chat.id,
                     "Добро пожаловать в <b>cloud.mаrket</b>! Меня зовут <b>Breezy</b>. Я персональный помощник данного "
                     "магазина.🤖😉\n\n"
                     "Мы занимаемся доставкой одежды, обуви и многого другого из Китая, а именно с площадки <b>POIZON</b>. "
                     "Мы гарантируем оригинальность доставляемых нами товаров, отличное качество и приятные цены.🩵🩵🩵\n\n"
                     "Если Вы давно хотели обновить свой гардероб, но не знали где, то Вы по адресу! Скорее "
                     "переходите в блок <b>«Меню»</b> и знакомьтесь с нашими разделами.🛍🤑", parse_mode='html',
                     reply_markup=markup)


# Обработчик команды "меню"
@bot.callback_query_handler(func=lambda callback: callback.data == 'menu')
def menu(callback):
    # Создаем клавиатуру с различными кнопками меню
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛍 Оформить заказ", callback_data="make_order"))
    markup.add(types.InlineKeyboardButton("💴 Калькулятор стоимости", callback_data="calculator"))
    markup.add(types.InlineKeyboardButton("🚚 Доставка", callback_data="delivery"))
    markup.add(types.InlineKeyboardButton("📚 Популярные вопросы", callback_data="questions"))
    markup.add(types.InlineKeyboardButton("👁️‍🗨️ Всё о POIZON", callback_data="about_poizon"))
    markup.add(types.InlineKeyboardButton("💬 Отзывы", url="https://t.me/cloudmrktfeedback"))
    markup.add(types.InlineKeyboardButton("☎️ Обратная связь", callback_data="feedback"))

    # Открываем изображение с логотипом и отправляем его вместе с клавиатурой
    try:
        file_path = "./logo.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file, reply_markup=markup)
    except Exception as e:
        print(f"Error sending photo: {e}")


# Код для обработки команды "make_order"
@bot.callback_query_handler(func=lambda callback: callback.data == 'make_order')
def make_order(callback):
    # Создаем клавиатуру с вариантами: "Калькулятор" и "Продолжить"
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Калькулятор", callback_data="calculator")
    button2 = types.InlineKeyboardButton("Продолжить", callback_data="continue_order")
    markup.row(button1, button2)

    # Отправляем сообщение с инструкцией и клавиатурой
    bot.send_message(callback.message.chat.id,
                     "💰 Перед оформлением заказа рассчитайте его стоимость. Для этого перейдите в <b>«Меню» → «Калькулятор "
                     "стоимости»</b>. Если это условие выполнено, то можете приступать к составлению карточки заказа.",
                     reply_markup=markup,parse_mode='html')


# Код для обработки команды "continue_order"
@bot.callback_query_handler(func=lambda callback: callback.data == 'continue_order')
def continue_order(callback):
    # Подключаемся к базе данных
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Создаем таблицу пользователей, если ее нет
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,article TEXT, size INTEGER, "
                "price INTEGER, name TEXT, number TEXT,town TEXT, telegram TEXT)")
    conn.commit()

    # Закрываем соединение
    cur.close()
    conn.close()

    # Отправляем сообщение с просьбой отправить артикул товара
    bot.send_message(callback.message.chat.id, "🏷 Укажите артикул товара:")
    bot.register_next_step_handler(callback.message, user_article)


# Функция обработки артикула товара
def user_article(message):
    global article
    article = message.text.strip()
    bot.send_message(message.chat.id, "👕 Укажите размер Вашей вещи: \n(при отсутствии поставьте '-' без скобок)")
    bot.register_next_step_handler(message, user_size)


# Функция обработки размера
def user_size(message):
    global size
    size = message.text.strip()
    bot.send_message(message.chat.id, "💷 Укажите цену товара в рублях, рассчитанную в <b>«Калькуляторе стоимости»</b>:",parse_mode='html')
    bot.register_next_step_handler(message, user_price)


# Функция обработки цены товара
def user_price(message):
    global price
    try:
        price = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте снова")
        bot.register_next_step_handler(message, user_price)
        return
    if price >= 0:
        bot.send_message(message.chat.id, "🙎 Укажите ФИО:")
        bot.register_next_step_handler(message, user_name)
    else:
        bot.send_message(message.chat.id, "Цена не должна быть отрицательной, попробуйте снова")
        bot.register_next_step_handler(message, user_price)


# Функция обработки ФИО
def user_name(message):
    global name
    name = message.text.strip()
    if not(any(symbol.isdigit() for symbol in name)):
        bot.send_message(message.chat.id, "📱 Укажите номер телефона:")
        bot.register_next_step_handler(message, user_number)
        return
    else:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте снова")
        bot.register_next_step_handler(message, user_name)


# Функция обработки номера телефона
def user_number(message):
    global number
    try:
        number = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте снова")
        bot.register_next_step_handler(message, user_number)
        return
    if len(str(number)) == 11:
        bot.send_message(message.chat.id, "🏙 Укажите город доставки:")
        bot.register_next_step_handler(message, user_city)
    else:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте снова")
        bot.register_next_step_handler(message, user_number)


# Функция обработки города доставки
def user_city(message):
    global town
    town = message.text.strip()
    if not(any(symbol.isdigit() for symbol in town)):
        bot.send_message(message.chat.id, "📨 Укажите ссылку на Ваш Telegram:")
        bot.register_next_step_handler(message, user_telegram)
        return
    else:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте снова")
        bot.register_next_step_handler(message, user_city)


# Функция для регистрации пользователя и отправки информации о регистрации
def user_telegram(message):
    # Извлекаем текст из сообщения и очищаем от лишних пробелов
    if message.text.strip()[0] == "@":
        telegram = message.text.strip()
    else:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте снова")
        bot.register_next_step_handler(message, user_telegram)
        return
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Вставляем данные в базу
    cur.execute(
        "INSERT INTO users (article, size, price, name, number, town, telegram) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (article, size, price, name, number, town, telegram))
    conn.commit()

    # Закрываем курсор и соединение
    cur.close()
    conn.close()

    # Подключаемся к базе данных для получения информации о последнем заказе
    conn = sqlite3.connect('base.sql')
    cursor = conn.cursor()

    try:
        # Выполнение SQL-запроса для получения последней записи
        cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")

        # Извлечение результатов запроса
        last_record = cursor.fetchone()

        # Если есть запись, создайте строку с информацией
        if last_record:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Меню", callback_data="menu"))
            info = (
                f'<b>🏷 Артикул товара</b>: {last_record[1]}\n<b>👕Размер</b>: {last_record[2]}\n<b>💷Цена</b>: {last_record[3]}\n<b>🙎ФИО</b>: {last_record[4]}\n'
                f'<b>📱 Номер телефона</b>: {last_record[5]}\n<b>🏙 Город</b>: {last_record[6]}\n<b>📨 Telegram</b>: {last_record[7]}')
            bot.send_message(message.chat.id, info,parse_mode='html')
            # Поздравляем с успешной регистрацией
            bot.send_message(message.chat.id,
                             "Ваша карточка составлена!😉 \nСкопируйте сообщение выше и отправьте его "
                             "любому администратору нашего магазина. Он уточнит всю информацию и подтвердит "
                             "Ваш заказ. Оплата производится в переписке с администратором. \n<b>Контакты для "
                             "связи</b>: @givenchy2417 @thunderx14:",reply_markup=markup,parse_mode='html')
        else:
            bot.send_message(message.chat.id, "В базе данных нет записей.")

    finally:
        # закрываем соединение, чтобы избежать утечек
        cursor.close()
        conn.close()


# Обработка команды "calculator"
@bot.callback_query_handler(func=lambda callback: callback.data == 'calculator')
def calculator(callback):
    # Создаем клавиатуру с категориями товаров
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👟 Летняя обувь", callback_data="summer_shoes"))
    markup.add(types.InlineKeyboardButton("🥾 Зимняя обувь", callback_data="winter_shoes"))
    markup.add(types.InlineKeyboardButton("🧥 Верхняя одежда", callback_data="outerwear"))
    markup.add(types.InlineKeyboardButton("🙋‍ Свитшоты / Худи / Джемперы", callback_data="hoodie"))
    markup.add(types.InlineKeyboardButton("👖 Штаны/ Джинсы/ Брюки", callback_data="pants"))
    markup.add(types.InlineKeyboardButton("👔 Пиджаки / Костюмы / Рубашки", callback_data="jacket"))
    markup.add(types.InlineKeyboardButton("👕 Футболки и поло", callback_data="T-shirt"))
    markup.add(types.InlineKeyboardButton("🧦 Нижнее белье и носки", callback_data="underwear"))
    markup.add(types.InlineKeyboardButton("💍 Аксессуары / Сумки / Украшения", callback_data="accessories"))
    markup.add(types.InlineKeyboardButton("💻 Техника", callback_data="technic"))
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Открываем файл с изображением калькулятора
    try:
        file_path = "./calculator.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file,
                           caption="💰 В нашем калькуляторе Вы можете произвести расчет стоимости "
                                   "товара с  доставкой до России (Москва). В калькуляторе "
                                   "указывайте цену в юанях по зачеркнутому ценнику в "
                                   "бирюзовой кнопке (если он имеется). Товары с ≈ не "
                                   "выкупаем!", reply_markup=markup)
    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработчик запроса калькулятора для сухопутной доставки
@bot.callback_query_handler(func=lambda callback: callback.data == 'land')
def land(callback):
    # Открываем изображение с инструкцией к калькулятору
    try:
        file_path = "./calculator.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file, caption="💳 Введите стоимость товара в юанях:")
    except Exception as e:
        print(f"Error sending photo: {e}")

    # Регистрируем следующий шаг обработки, который будет вызван после ввода стоимости
    bot.register_next_step_handler(callback.message, cost_order)


# Обработчик запроса калькулятора для суперавиа доставки
@bot.callback_query_handler(func=lambda callback: callback.data == 'air')
def air(callback):
    # Глобальная переменная для хранения стоимости доставки
    global delivery_cost

    # Увеличиваем стоимость доставки на 800, указывая, что это суперавиа
    delivery_cost += 800

    # Открываем изображение с инструкцией к калькулятору
    try:
        file_path = "./calculator.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file, caption="Введите стоимость товара в юанях:")
    except Exception as e:
        print(f"Error sending photo: {e}")

    # Регистрируем следующий шаг обработки, который будет вызван после ввода стоимости
    bot.register_next_step_handler(callback.message, cost_order)


# Код для обработки команды "delivery"
@bot.callback_query_handler(func=lambda callback: callback.data == 'delivery')
def delivery(callback):
    # Создаем клавиатуру
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Открываем файл с изображением
    try:
        file_path = "./delivery.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file, caption="📦 Для наших клиентов предоставляются на выбор следующие виды доставки "
                                                                "из Китая в Россию: <b>сухопутная</b> и <b>супер-авиа</b> (подробнее о сроках вы "
                                                                "можете узнать, перейдя в раздел <b>«Меню» → «Популярные вопросы» → "
                                                                "«Сколько по времени занимает доставка?»</b>). \n\n💸 Стоимость доставки зависит "
                                                                "от ее вида, количества вещей, заказанных клиентом, и их веса. Она "
                                                                "включена в итоговую цену заказа и высчитывается в <b>«Калькуляторе "
                                                                "стоимости»</b>. \n\n🚚 Доставка по России для жителей регионов и МО оплачивается "
                                                                "отдельно перед отправлением из Москвы.", reply_markup=markup, parse_mode='html')
    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработчик команды "вопросы"
@bot.callback_query_handler(func=lambda callback: callback.data == 'questions')
def questions(callback):
    # Создаем клавиатуру с различными кнопками для вопросов и ответов
    markup = types.InlineKeyboardMarkup()
    questions_and_answers = [
        ("Где найти артикул товара?", "article_number"),
        ("Как осуществляется заказ товара?", "how_make_order"),
        ("Из чего складывается итоговая стоимость?", "finish_cost"),
        ("В каком городе базируется склад в России?", "warehouse"),
        ("В какие города производится доставка?", "city"),
        ("Можно ли отслеживать передвижение посылки?", "tracking"),
        ("Сколько по времени занимает доставка?", "delivery_time"),
        ("Можно ли обменять или вернуть товар?", "refund"),
        ("Другой вопрос", "another"),
        ("Назад", "back")
    ]
    for question, data in questions_and_answers:
        markup.add(types.InlineKeyboardButton(question, callback_data=data))

    # Открываем изображение с часто задаваемыми вопросами и отправляем его вместе с клавиатурой
    try:
        file_path = "./questions.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file, reply_markup=markup)

    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработчик запроса для вопроса "Где найти артикул товара?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'article_number')
def article_number(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Открываем изображение с инструкцией и отправляем его вместе с клавиатурой
    try:
        file_path = "./article.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file,
                           caption="🏷 Для начала необходимо открыть карточку товара. Находите под ней табличку "
                                   "с характеристиками, раскрываете их и удерживаете палец на первом пункте, "
                                   "чтобы скопировать артикул.", reply_markup=markup)

    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработчик запроса для вопроса "Как осуществляется заказ товара?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'how_make_order')
def how_make_order(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с подробным описанием процесса заказа
    bot.send_message(callback.message.chat.id, "🧾 Оформление заказа состоит из двух частей: 1. Составление карточки заказа "
                                               "с помощью бота. 2. Подтверждение и оплата заказа у "
                                               "администраторов. Перед оформлением заказа рассчитайте его стоимость в "
                                               "«Калькуляторе стоимости».\n\n😊 Рассмотрим подробнее каждую часть:\n\n📕 1. Сначала "
                                               "Вы указываете артикул (<b>«Меню» → «Популярные вопросы» → «Где найти артикул товара и ссылку на него?»</b>). Далее "
                                               "отправляете размер вашей вещи (при наличии). Затем указываете цену в "
                                               "рублях, рассчитанную в «Калькуляторе стоимости». После сообщаете "
                                               "немного контактной информации: ФИО, номер телефона, город проживания "
                                               "и ссылку на Telegram (@xxxxx), чтобы мы понимали, как к Вам можно "
                                               "обращаться, как с Вами связаться, если Вы не отвечаете в Telegram и "
                                               "необходима ли доставка в пункт выдачи? \n\n📘 2. После составления карточки "
                                               "заказа Вы копируете ее и пересылаете любому администратору магазина "
                                               "для модерации. Все контакты Вы найдете уже при оформлении заказа. "
                                               "Администраторы уточняют всю информацию, высылают реквизиты, "
                                               "Вы проводите оплату и Вам сообщают, что заказ подтвержден. Вы "
                                               "заноситесь в клиентскую базу и все, что остается Вам делать, "
                                               "так это ждать, пока посылка придет в Москву и магазин с Вами свяжется.",
                     reply_markup=markup, parse_mode='html')


# Обработчик запроса для вопроса "Из чего складывается итоговая стоимость?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'finish_cost')
def finish_cost(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с объяснением того, из чего складывается итоговая стоимость
    bot.send_message(callback.message.chat.id, "💰 Итоговая стоимость складывается из следующих параметров: цена товара, "
                                               "стоимость доставки из Китая до России, комиссия магазина и стоимость "
                                               "доставки в регионы РФ (при необходимости). К сожалению, сами цифры и "
                                               "формулы, по которым мы работаем, не раскрываются.", reply_markup=markup)


# Обработчик запроса для вопроса "В каком городе базируется склад в России?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'warehouse')
def warehouse(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с информацией о том, в каком городе базируется склад магазина
    bot.send_message(callback.message.chat.id, "🇷🇺 Склад магазина базируется в Москве.", reply_markup=markup)


# Обработчик запроса для вопроса "В какие города производится доставка?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'city')
def city(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с информацией о том, в какие города производится доставка
    bot.send_message(callback.message.chat.id, "🇷🇺 Доставка производится во все регионы РФ.", reply_markup=markup)


# Обработчик запроса для вопроса "Можно ли отслеживать передвижение посылки?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'tracking')
def tracking(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с информацией о трек-номере и способе отслеживания
    bot.send_message(callback.message.chat.id, "🚚 Посредник магазина сотрудничает с транспортной компанией, "
                                               "не предоставляющей трек-номер посылки, поэтому наши клиенты не могут "
                                               "в любое время узнать местонахождение заказа, пока посылка не дойдет "
                                               "до России. \nПосле поступления товара на склад в столице мы отправляем "
                                               "его <b>Почтой России</b> или <b>СДЕК</b>ом и предоставляем трек-номер доставки. Вы "
                                               "всегда можете обратиться к администраторам магазина, "
                                               "которые подскажут примерное местоположение посылки и ее статус. ("
                                               "<b>«Меню» → «Обратная связь»</b>)", reply_markup=markup,parse_mode='html')


# Обработчик запроса для вопроса "Сколько по времени занимает доставка?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'delivery_time')
def delivery_time(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с информацией о времени доставки
    bot.send_message(callback.message.chat.id, "Для наших клиентов предоставляются на выбор следующие виды доставки:\n\n"
                                               "1. 🚛 <b>Сухопутная</b>: доставка в регионы занимает от 25 до 49 дней, "
                                               "для жителей Москвы и МО от 22 до 30 дней. \n\n2. 🛩 <b>Супер-авиа</b>: доставка в "
                                               "регионы занимает от 19 до 27 дней, для жителей Москвы и МО от 16 до "
                                               "22 дней.", reply_markup=markup,parse_mode='html')


# Обработчик запроса для вопроса "Можно ли обменять или вернуть товар?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'refund')
def refund(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с информацией о возврате товара
    bot.send_message(callback.message.chat.id, "✅ Магазин может предоставить возврат денежных средств в полном объеме в "
                                               "случае повреждения или получения не того товара. Возврат производится "
                                               "на банковскую карту, с которой происходила оплата.\n\n❌ С целью избежания "
                                               "мошенничества со стороны покупателей сотрудники магазина проводят "
                                               "фото и видеофиксацию целостности товара перед отправкой покупателю "
                                               "или перед передачей в случае личной встречи. \n\n🤔 Внимательно подходите к "
                                               "выбору размера и других параметров одежды, кроссовок и пр., "
                                               "так как магазин <b>не возвращает</b> денежные средства, если вещь не подошла "
                                               "или "
                                               "не понравилась!!! Если у Вас остались вопросы по возврату и обмену "
                                               "или Вы хотите вернуть товар, обращайтесь к администраторам магазина: "
                                               "@givenchy2417 @thunderx14", reply_markup=markup,parse_mode='html')


# Обработчик запроса для вопроса "Другой вопрос"
@bot.callback_query_handler(func=lambda callback: callback.data == 'another')
def another(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем сообщение с предложением обратиться к администраторам магазина
    bot.send_message(callback.message.chat.id, "😓 Если вы не нашли свой вопрос в списке предложенных - обратитесь к "
                                               "администраторам магазина. Они с радостью "
                                               "ответят на них.\n<b>Контакты</b>: @givenchy2417 @thunderx14", reply_markup=markup, parse_mode='html')


# Обработчик запроса для вопроса "Всё о POIZON"
@bot.callback_query_handler(func=lambda callback: callback.data == 'about_poizon')
def about_poizon(callback):
    # Создаем клавиатуру с вариантами вопросов о POIZON
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Как установить POIZON?", callback_data="how_download_poizon"))
    markup.add(types.InlineKeyboardButton("Как зарегистрироваться на POIZON?", callback_data="how_to_register"))
    markup.add(types.InlineKeyboardButton("Как пользоваться интерфейсом POIZON?", callback_data="how_to_use"))
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем фото и информацию о POIZON
    try:
        file_path = "./about poizon.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file, reply_markup=markup)

    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработчик запроса для вопроса "Как установить POIZON?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'how_download_poizon')
def how_download_poizon(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем фото и информацию о том, как скачать POIZON
    try:
        file_path = "./download.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file,
                           caption="<b>📱IOS</b> - Если у Вас телефон на базе IOS, то просто введите в поисковик "
                                   "App Store слово «pozion» или «dewu» \n\n📱<b>Android</b> - Если у Вас телефон на "
                                   "базе Android, то скачайте приложение, перейдя на сайт dеwu.cоm, по QR-коду, "
                                   "так как в Play Market оно не представлено", reply_markup=markup,parse_mode='html')

    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработчик запроса для вопроса "Как зарегистрироваться на POIZON?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'how_to_register')
def how_to_register(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем фото и информацию о том, как зарегистрироваться на POIZON
    # Отправляем файл с изображением
    try:
        file_path = "./registration.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file,
                           caption="1)Запустив приложение, нажмите бирюзовую кнопку, которая означает, "
                                   "что Вы согласны с политикой магазина. \n\n2,3)После этого выбери код страны ("
                                   "+7) из списка предложенных и введите свой номер телефона. \n\n4)Снова "
                                   "нажмите на бирюзовую кнопку и впишите в квадратики код, который придет "
                                   "Вам на телефон. \n\n5)На этом все! Теперь Вы можете пользоваться "
                                   "приложением!", reply_markup=markup)

    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработчик запроса для вопроса "Как пользоваться интерфейсом POIZON?"
@bot.callback_query_handler(func=lambda callback: callback.data == 'how_to_use')
def how_to_use(callback):
    # Создаем клавиатуру для возможности вернуться назад
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Отправляем файл с изображением
    try:
        file_path = "./poizon.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file,
                           caption="🔎 Попав на главную страницу POIZON, Вы можете перейти к поиску "
                                   "интересующих Вас вещей через поисковую строку или через разделы, "
                                   "представленные чуть ниже нее.\n\n🧐 Переключаясь между разделами, "
                                   "можно их раскрывать, нажимая кнопку «More». В выпадающей таблице будут "
                                   "представлены разные категории и подразделы. Заходите в каждый из них и "
                                   "находите то, что Вам по душе! \n\n🇨🇳 К сожалению, приложение не поддерживает "
                                   "русский язык, поэтому первое время придется пользоваться переводчиком. "
                                   "Но мы уверены, что Вы быстро привыкните к интерфейсу и сможете "
                                   "прекрасно ориентироваться в разделах магазина!", reply_markup=markup)

    except Exception as e:
        print(f"Error sending photo: {e}")


# Обработка команды "feedback"
@bot.callback_query_handler(func=lambda callback: callback.data == 'feedback')
def feedback(callback):
    # Создаем клавиатуру
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back"))

    # Открываем файл с изображением
    try:
        file_path = "./feedback.PNG"
        with open(file_path, "rb") as file:
            # Отправляем фото с подписью и клавиатурой
            bot.send_photo(callback.message.chat.id, file,
                           caption="🔍 Если у Вас возникли вопросы или Вы нуждаетесь в помощи, "
                                   "не стесняйтесь обращаться к администраторам. Они всегда готовы помочь "
                                   "и ответить на все вопросы. Просто напишите им сообщение с описанием "
                                   "своей проблемы или темы, которая интересует. Администраторы сделают "
                                   "все возможное, чтобы помочь Вам! \n<b>Контакты</b>: @givenchy2417 "
                                   "@thunderx14", reply_markup=markup, parse_mode="html")

    except Exception as e:
        print(f"Error sending photo: {e}")


# функция для перехода к предыдущей вкладке
@bot.callback_query_handler(func=lambda callback: callback.data == "back")
def delete_last_message(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


# Обработка команды "type_items"
@bot.callback_query_handler(func=lambda callback: True)
def type_items(callback):
    # Используем глобальную переменную для хранения стоимости доставки
    global delivery_cost

    # Получение стоимости доставки из словаря
    delivery_cost = delivery_costs.get(callback.data, 0)

    # Создание клавиатуры для выбора типа доставки
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("🚛 Сухопутная", callback_data="land")
    button2 = types.InlineKeyboardButton("🛩 Супер-авиа", callback_data="air")
    markup.row(button1, button2)

    # Отправка сообщения с просьбой выбрать тип доставки
    bot.send_message(callback.message.chat.id, "Выберите тип доставки:", reply_markup=markup)


# Обработчик для неизвестных команд
@bot.message_handler()
def main(message):
    bot.send_message(message.chat.id, "Мы пока не знаем такой команды")


# Запуск бота с параметром none_stop для непрерывного выполнения
bot.polling(none_stop=True)

# @bot.callback_query_handler(func=lambda callback: True)
# def type_items(callback):
#     global delivery_cost
#     if callback.data == "summer_shoes":
#         delivery_cost = 1800 + 2700
#     elif callback.data == "winter_shoes":
#         delivery_cost = 2000 + 3000
#     elif callback.data == "outerwear":
#         delivery_cost = 2000 + 2400
#     elif callback.data == "hoodie":
#         delivery_cost = 1700 + 1500
#     elif callback.data == "pants":
#         delivery_cost = 1700 + 1500
#     elif callback.data == "jacket":
#         delivery_cost = 1750 + 1650
#     elif callback.data == "shirt":
#         delivery_cost = 1500 + 1300
#     elif callback.data == "underwear":
#         delivery_cost = 1200 + 900
#     elif callback.data == "accessories":
#         delivery_cost = 1000 + 1500
#     elif callback.data == "technic":
#         delivery_cost = 2200 + 3000
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton("Сухопутная", callback_data="land")
#     button2 = types.InlineKeyboardButton("Супер-авиа", callback_data="air")
#     markup.row(button1, button2)
#     bot.send_message(callback.message.chat.id, "Выберите тип доставки:", reply_markup=markup)

