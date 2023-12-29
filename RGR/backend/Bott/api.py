import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#from main import States
API_BASE_URL = 'http://localhost:8000/api/'

async def profile_exists(bot,external_id):
    response = requests.get(f'{API_BASE_URL}profiles/')
    profiles_data = response.json()
    user_exist = False

    for profile_data in profiles_data:
        if profile_data['external_id'] == external_id:
            # Если нашел по айди, то существует
            user_exist = True
            await bot.send_message(external_id, "Пользователь уже существует, так что можно продолжать")
            break

    if not user_exist:
        await bot.send_message(external_id, "Пользователь не найден")
        return False
        
async def create_profile(bot, external_id, name,user_answer):
    if user_answer.lower() in ['левый', 'правый']:
        residence_mapping = {'левый': 'left', 'правый': 'right'}
        residence_value = residence_mapping[user_answer.lower()]
        response=requests.post(API_BASE_URL + 'profiles/', data={'external_id': external_id, 'name': name, 'residence': residence_value})
        if response.status_code == 201:
            await bot.send_message(external_id, f"Профиль создан с проживанием: {user_answer}. Теперь можно перейти к следующему этапу.")
            
        else:
            await bot.send_message(
                external_id,
                f"Ошибка при создании профиля: {response.status_code} - {response.text}"
            )    
    else:
        await bot.send_message(external_id, "Неверное значение. Выберите 'Левый' или 'Правый'.")

async def ask_question1(bot,external_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Рядом"))
    markup.add(KeyboardButton("Без разницы"))
    await bot.send_message(external_id, "Вы хотите учиться рядом с домом или без разницы?", reply_markup=markup)

async def ask_question2(bot,external_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Технический"))
    markup.add(KeyboardButton("Гуманитарный"))
    await bot.send_message(external_id, "Какая вуз вас интересует: Технический или Гуманитарный?", reply_markup=markup)

async def ask_question3(bot,external_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Конечно!"))
    markup.add(KeyboardButton("Без разницы...."))
    await bot.send_message(external_id, "Вы хотите учиться в лучшем вузе города?", reply_markup=markup)

async def send_answers(bot,external_id,state):
    # Получаем все сохраненные ответы из контекста состояния
    data = await state.get_data()
    answer1 = data.get('answer1', '')
    answer2 = data.get('answer2', '')
    answer3 = data.get('answer3', '')
    response = requests.get(f'{API_BASE_URL}profiles/')
    profiles_data = response.json()
    if response.status_code == 200:
        for profile_data in profiles_data:
            if profile_data['external_id'] == external_id:
                profile_id = profile_data['id']
                residence = profile_data['residence']
        response_universities = requests.get(f'{API_BASE_URL}universities/') #Получение списка всех вузов
        universities = response_universities.json()
        if answer1.lower() == 'рядом':
            universities = [uni for uni in universities if uni['location'] == residence]
        if answer2.lower() == 'технический':
            universities = [uni for uni in universities if uni['specialization'] == 'technical']
        elif answer2.lower() == 'гуманитарный':
            universities = [uni for uni in universities if uni['specialization'] == 'humanitarian']
        if answer3.lower() == 'конечно!':
            await bot.send_message(external_id, "Извините, но я знаю только один такой вуз - НГУЭУ")
        elif answer3.lower() == 'без разницы....':
            if universities:
                message_text = "Вот что вам подходит:\n"
                for uni in universities:
                    location = 'Правый берег' if uni['location'] == 'right' else 'Левый берег'
                    specialization = 'Технический вуз' if uni['specialization'] == 'technical' else 'Гуманитарный вуз'
                    message_text += f"{uni['name']} ({location}, {specialization})\n"
                await bot.send_message(external_id, message_text)
            else:
                await bot.send_message(external_id, "По вашим критериям не найдено подходящих вузов.")

        # Записываем ответ пользователя в API
        response_create_answer = requests.post(
            API_BASE_URL + 'messages/',
            data={'profile': profile_id, 'answer1': answer1,'answer2': answer2,'answer3': answer3}
        )
        
        if response_create_answer.status_code == 201:
            print("Ответы на вопросы сохранены.")
            await bot.send_message(external_id, "Ответы на вопросы сохранены.")
            await state.finish()
        else:
            print(f"Ошибка при сохранении ответов : {response_create_answer.text}")
    else:
        print("Профиль не найден. Создайте профиль с командой /start.")



async def ask_subscription(bot,external_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Да"))
    markup.add(KeyboardButton("Нет"))
    await bot.send_message(external_id, "Хотите подписаться на рассылку?", reply_markup=markup)
async def set_subscription(bot,external_id, subscribe):
    # Получаем профиль пользователя
    response = requests.get(f'{API_BASE_URL}profiles/')
    profiles_data = response.json()
    if response.status_code == 200:
        for profile_data in profiles_data:
            if profile_data['external_id'] == external_id:
                profile_id = profile_data['id']
        
        # Обновляем подписку в API
        response_update_subscription = requests.patch(
            f'{API_BASE_URL}profiles/{profile_id}/',
            data={'subscription': subscribe}
        )
        
        if response_update_subscription.status_code == 200:
            print(f"Подписка обновлена: {subscribe}")
            if subscribe==True:
                await bot.send_message(external_id, "Вы подписались на рассылку")
            elif subscribe==False:
                await bot.send_message(external_id, "Вы отказались от рассылки")
        else:
            print(f"Ошибка при обновлении подписки в API: {response_update_subscription.text}")
    else:
        print("Профиль не найден. Создайте профиль с командой /start.")

