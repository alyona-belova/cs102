from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    row_id = request.query.id
    row = s.query(News).filter(News.id == row_id).first()
    row.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/", 3)
    for n in news:
        row = News(title=n["title"],
                   author=n["author"],
                   url=n["url"],
                   comments=n["comments"],
                   points=n["points"])
        if s.query(News).filter(News.title == row.title and News.author == row.author).all():
            continue
        s.add(row)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    X_train, y = [], []
    for i in range(1000):
        for item in s.query(News).filter(News.id == i).all():
            X_train.append(item.title)
            y.append(item.label)
    X_train = [x.translate(str.maketrans("", "", string.punctuation)).lower() for x in X_train]

    X_test, infos = [], []
    for i in range(1000, len(s.query(News).all()) + 1):
        for item in s.query(News).filter(News.id == i).all():
            X_test.append(item.title)
            infos.append(News(author=item.author,
                              points=item.points,
                              comments=item.comments,
                              url=item.url))
    X_cleared = [x.translate(str.maketrans("", "", string.punctuation)).lower() for x in X_test]

    model = NaiveBayesClassifier(alpha=0.01)
    model.fit(X_train, y)
    print(model.score(X_train, y))
    predicted_news = model.predict(X_cleared)

    data = []
    for i in range(len(predicted_news)):
        data.append([y[i], X_test[i], infos[i]])

    classified_news = sorted(data, key=lambda item: item[0])
    return template('news_recommendations', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
