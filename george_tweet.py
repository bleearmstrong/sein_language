import random
from twython import Twython
import time
import pickle


def line_splitter(line):
    """
    :param line: a line that will be tweeted
    :return: a list of lines that are under 140 characters that may be tweeted;
             an attempt will be made so that each line is roughly equal in size
    """
    if len(line) <= 140:
        return [line]
    tweets = []
    chunks = len(line) // 140 + 2
    length = len(line) // chunks
    while len(line) > 130:
        indexes = [i for i, char in enumerate(line) if char == ' ' and i < length]
        tweets.append(line[0:indexes[-1]].strip() + ' (cont)')
        line = line[indexes[-1]:].strip()
    tweets.append(line)
    return tweets

george_lines = pickle.load(open('C:/Users/ben/Desktop/seinfeld/george.pickle', 'rb'))

auth_dic = pickle.load(open('C:/Users/ben/Desktop/seinfeld/auth.pickle', 'rb'))

gbot = Twython(auth_dic['APP_KEY']
               , auth_dic['APP_SECRET']
               , auth_dic['OAUTH_TOKEN']
               , auth_dic['OAUTH_TOKEN_SECRET'])

random_line = random.choice(george_lines)
tweets = line_splitter(random_line)

for tweet in tweets:
    gbot.update_status(status=tweet)
    time.sleep(5)
