import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id, 'bdate')
    date_now = dt.datetime.now()
    year_now = date_now.year
    ages = []
    for friend in friends:
        try:
            date = friend['bdate']
            date = dt.datetime.strptime(date, "%d.%m.%Y")
            ages.append(year_now-date.year)
        except:
            pass

    return median(ages)

if __name__ == "__main__":
    print(age_predict(372097810))
