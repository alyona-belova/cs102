import config
import gensim
import nltk
import pandas as pd
import pymorphy2
import pyLDAvis.gensim
import re
import requests
import textwrap

from nltk.corpus import stopwords
from string import punctuation


def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """

    code = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "count": count,
        "filter": filter,
        "extended": extended,
        "fields": fields,
        "v": v
    }

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": f'return API.wall.get({code});',
            "access_token":  config.VK_CONFIG['access_token'],
            "v": v
            }
    )

    walls = []
    for i in range(count):
        try:
            walls.append(response.json()['response']['items'][i]['text'])
        except:
            break

    return walls


def del_stopwords(text):
    stop_words = []
    stop_words.append(stopwords.words('russian'))
    stop_words.append(stopwords.words('english'))
    n_text = [word for word in text if word not in stop_words]
    return n_text


def clean(text):
    n_article = []
    n_text = []
    for article in text:
        for word in article:
            word = ''.join(ch for ch in word if ch not in punctuation and ch != '«' and ch != '»')
            emoji = re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF"
                               u"\U00002702-\U000027B0"u"\U000024C2-\U0001F251"u"\U0001f926-\U0001f937"u"\U00010000-\U0010ffff"
                               u"\u200d"u"\u2640-\u2642"u"\u2600-\u2B55"u"\u23cf"u"\u23e9"u"\u231a"u"\u3030"u"\ufe0f""]+", flags=re.UNICODE)
            if not word.isalpha():
                continue
            n_article.append(emoji.sub(r'', word))
        n_text.append(n_article)
        n_article = []
    return n_text


def del_links(text):
    n_text = []
    n_article = []
    for article in text:
        for word in article:
            if word.find('http') == -1 and word.find('.ru') == -1 and word.find('.com') == -1:
                n_article.append(word)
        n_text.append(n_article)
        n_article = []
    return n_text


def normalize(text):
    n_article = []
    n_text = []
    morph = pymorphy2.MorphAnalyzer()
    for article in text:
        for word in article:
            if morph.parse(word)[0].tag.POS == 'NOUN':
                word = morph.parse(word)[0].normal_form
                n_article.append(word)
        n_text.append(n_article)
        n_article = []
    return n_text

if __name__ == "__main__":
    wall = []
    for group in ['itmostudents', 'itmoru', 'spb1724', 'overhearspbsu', 'pimunn', 'overheard_pimunn', 'sutru', 'pgpuspb', 'pgpuspb', 'otchisleno']:
        wall.extend(get_wall(domain=group, count=2500))
    texts = [[text.lower() for text in doc.split()] for doc in wall]
    texts = del_stopwords(texts)
    texts = del_links(texts)
    texts = clean(texts)
    texts = normalize(texts)
    dictionary = gensim.corpora.Dictionary(texts)
    full_text = []
    for i in range(len(texts)):
        full_text.extend(texts[i])
    corpus = [dictionary.doc2bow(full_text)]
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, per_word_topics=False)
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, 'topic model.html')
