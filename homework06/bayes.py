from numpy import argmax
from math import log
from collections import Counter


class NaiveBayesClassifier:

    def __init__(self, alpha=0.01):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.number_of_news = len(X)
        self.number_of_labels = len(dict(Counter(y)))
        self.y_counter = Counter(y)

        self.labels = []
        labeled_words = []
        for i in range(self.number_of_labels):
            self.labels.append(list(Counter(y))[i])
            labeled_words.append([])

        for i in range(len(X)):
            for word in X[i].split():
                j = 0
                while not y[i] in self.labels[j]:
                    j += 1
                labeled_words[j].append(word)

        labels_count = []
        number_of_words = []
        words = []
        self.P_words = []
        for i in range(self.number_of_labels):
            number_of_words.append(sum(Counter(labeled_words[i]).values()))
            labels_count.append(Counter(labeled_words[i]))
            words.extend(labeled_words[i])
            self.P_words.append(dict())
        words = Counter(words)

        for w in words:
            for i in range(self.number_of_labels):
                P = (labels_count[i][w] + self.alpha) / (number_of_words[i] + (self.alpha * len(words)))
                self.P_words[i].update({w: P})

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        news_predict = []
        P_class = []
        ln = []
        for i in range(self.number_of_labels):
            ln.append(0)
            P_class.append(self.y_counter[self.labels[i]]/self.number_of_news)

        for i in range(len(X)):
            for j in range(self.number_of_labels):
                ln[j] = log(P_class[j])
            for word in X[i].split():
                for j in range(self.number_of_labels):
                    if word in self.P_words[j]:
                        ln[j] += log(self.P_words[j][word])
            news_predict.append(self.labels[argmax(ln)])
        return news_predict

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        correct = 0
        y_predicted = self.predict(X_test)
        for i in range(len(y_predicted)):
            if y_predicted[i] == y_test[i]:
                correct += 1
        return correct/len(y_predicted)
