import requests
import config
import telebot
import datetime
import re
from bs4 import BeautifulSoup


telebot.apihelper.proxy = {'https': '129.146.181.251:3128'}

bot = telebot.TeleBot(config.access_token)

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    if week == '0/':
        week = ''
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    resp = requests.get(url)
    web_page = resp.text
    return web_page


def get_schedule(web_page: str, day: str):
    soup = BeautifulSoup(web_page, "html5lib")
    date = str(days.index(day) + 1) + "day"

    # Получаем таблицу с расписанием
    schedule_table = soup.find("table", attrs={"id": date})
    if schedule_table is None:
        return "error"

    # Время проведения занятий
    times_lst = schedule_table.find_all("td", attrs={"class": "time"})
    times_lst = [time.span.text for time in times_lst]

    # Место проведения занятий
    locations_lst = schedule_table.find_all("td", attrs={"class": "room"})
    locations_lst = [room.span.text for room in locations_lst]

    rooms_lst = schedule_table.find_all("td", attrs={"class": "room"})
    rooms_lst = [room.dd.text for room in rooms_lst]

    # Название дисциплин и имена преподавателей
    lessons_lst = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_lst = [lesson.text.split('\n\n') for lesson in lessons_lst]
    lessons_lst = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_lst]
    return times_lst, locations_lst, rooms_lst, lessons_lst


def get_study_day(web_page: str, day: str, week: str, group: str):
    if days.index(day) >= 6:
        day = 'monday'
        if week == 2:
            week = 1
        else:
            week = 2
        web_page = get_page(group, week)
    schedule = get_schedule(web_page, day)
    cur_day = days.index(day) + 1
    i = 0
    while schedule is "error" and i != 14:
        if cur_day == 6:
            cur_day = 0
            if week == 2:
                week = 1
            else:
                week = 2
            web_page = get_page(group, week)
        schedule = get_schedule(web_page, days[cur_day])
        cur_day += 1
        i += 1
    return schedule


def is_group_exist(group):
    web_page = get_page(group)
    soup = BeautifulSoup(web_page, "html5lib")
    pattern = re.compile(r"Расписание не найдено")
    existence = soup.find(text=pattern)
    if existence is not None:
        return False
    else:
        return True


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_day(message):
    """ Получить расписание на указанный день """
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите номер группы после /day')
        return None
    elif len(message.text.split()) == 2:
        week = 0
        day, group = message.text.split()
    elif len(message.text.split()) == 3:
        day, week, group = message.text.split()
        if week != "1" and week != "2":
            bot.send_message(message.chat.id, 'Такой недели не существует\nВведите:\n1 - для четной\n2 - для нечетной')
            return None
    day = day[1:]
    group = group.upper()
    if not is_group_exist(group):
        bot.send_message(message.chat.id, 'Такой группы не существует')
        return None
    web_page = get_page(group, week)
    schedule = get_schedule(web_page, day)
    if schedule == "error":
        resp = "Отдыхайте :)"
    else:
        times_lst, locations_lst, rooms_lst, lessons_lst = schedule
        resp = ''
        for time, location, room, lesson in zip(times_lst, locations_lst, rooms_lst, lessons_lst):
            resp += 'В <b>{}</b> {} на {}, в {}\n\n'.format(time, lesson, location, room)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите номер группы после /near')
        return None
    _, group = message.text.split()
    group = group.upper()
    if not is_group_exist(group):
        bot.send_message(message.chat.id, 'Такой группы не существует')
        return None
    today = datetime.datetime.now()
    week = int(today.isocalendar()[1]) % 2 + 1
    if week == 1:
        week = 2
    else:
        week = 1
    if today.weekday() != 6:
        day = days[today.weekday()]
    else:
        day = 'monday'
        if week == 1:
            week = 2
        else:
            week = 1
        web_page = get_page(group, week)
        schedule = get_study_day(web_page, day, week, group)
        times_lst, locations_lst, rooms_lst, lessons_lst = schedule
        resp = 'В <b>{}</b> {} на {}, в {}'.format(times_lst[0], lessons_lst[0], locations_lst[0], rooms_lst[0])
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        return None
    web_page = get_page(group, week)
    schedule = get_study_day(web_page, day, week, group)
    times_lst, locations_lst, rooms_lst, lessons_lst = schedule
    count = 0
    for i in times_lst:
        t_start, _ = i.split('-')
        t_start = '{} {} {} {}'.format(today.year, today.day, today.month, t_start)
        t_start = datetime.datetime.strptime(t_start, '%Y %d %m %H:%M')
        if today < t_start:
            resp = 'В <b>{}</b> {} на {}, в {}'.format(times_lst[count], lessons_lst[count], locations_lst[count], rooms_lst[count])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            return None
        count += 1
    day = days[days.index(day) + 1]
    schedule = get_study_day(web_page, day, week, group)
    times_lst, locations_lst, rooms_lst, lessons_lst = schedule
    resp = 'В <b>{}</b> {} на {}, в {}'.format(times_lst[0], lessons_lst[0], locations_lst[0], rooms_lst[0])
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    return None


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите номер группы после /tommorow')
        return None
    _, group = message.text.split()
    group = group.upper()
    if not is_group_exist(group):
        bot.send_message(message.chat.id, 'Такой группы не существует')
        return None
    dt = datetime.datetime.now()
    week = int(dt.isocalendar()[1]) % 2 + 1
    if week == 1:
        week = 2
    else:
        week = 1
    if dt.weekday() == 6:
        day = "monday"
        if week == 1:
            week = 2
        else:
            week = 1
    else:
        day = days[dt.weekday() + 1]
    web_page = get_page(group, week)
    schedule = get_schedule(web_page, day)
    if schedule == "error":
        resp = "Отдыхайте :)"
    else:
        times_lst, locations_lst, rooms_lst, lessons_lst = schedule
        resp = ''
        for time, location, room, lesson in zip(times_lst, locations_lst, rooms_lst, lessons_lst):
            resp += 'В <b>{}</b> {} на {}, в {}\n\n'.format(time, lesson, location, room)
    if dt.weekday() == 5:
        resp = "Отдыхайте :)"
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите номер группы после /all')
        return None
    if len(message.text.split()) == 2:
        dt = datetime.datetime.now()
        week = int(dt.isocalendar()[1]) % 2 + 1
        if week == 1:
            week = 2
        else:
            week = 1
        day, group = message.text.split()
    elif len(message.text.split()) == 3:
        day, week, group = message.text.split()
        if week != "1" and week != "2":
            bot.send_message(message.chat.id, 'Такой недели не существует\nВведите:\n1 - для четной\n2 - для нечетной')
            return None
    group = group.upper()
    if not is_group_exist(group):
        bot.send_message(message.chat.id, 'Такой группы не существует')
        return None
    web_page = get_page(group, week)
    resp = ''
    for day in days:
        schedule = get_schedule(web_page, day)
        if schedule == "error":
            resp += '<b>{}</b>\n {}\n\n'.format(day, "День самоподготовки")
        else:
            times_lst, locations_lst, rooms_lst, lessons_lst = schedule
            resp += '<b>{}</b>\n'.format(day)
            for time, location, room, lesson in zip(times_lst, locations_lst, rooms_lst, lessons_lst):
                resp += 'В <b>{}</b> {} на {}, в {}\n\n'.format(time, lesson, location, room)
        resp += '\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def help(message: telebot.types.Message):
    resp = "Вот что я могу:\n/day (week) group - Получить расписание на этот день недели\n/near" + \
        " group - Получить ближайшее занятие\n/tommorow group - Получить расписание на следующий" + \
        " день\n/all (week) group - Получить расписание на всю неделю"
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    return None


if __name__ == '__main__':
    bot.polling(none_stop=True)
