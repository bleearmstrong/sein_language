import random
from twython import Twython
import time
import pickle

george_lines = pickle.load(open( 'C:/Users/ben/Desktop/seinfeld/george.pickle', 'rb'))
george_filter = [line.strip() for line in george_lines if 20 < len(line) <= 140]

auth_dic = pickle.load(open('C:/Users/ben/Desktop/seinfeld/auth.pickle', 'rb'))

gbot = Twython(auth_dic['APP_KEY']
               , auth_dic['APP_SECRET']
               , auth_dic['OAUTH_TOKEN']
               , auth_dic['OAUTH_TOKEN_SECRET'])

random_line = random.choice(george_filter)

gbot.update_status(status=random_line)