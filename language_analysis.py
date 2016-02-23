import pickle
from collections import Counter, defaultdict
import urllib.request
import pandas as pd
import seaborn as sns

seinfeld_dic = pickle.load(open('C:/Users/ben/Desktop/seinfeld/seinfeld.pickle', 'rb'))

character_episode_dic = defaultdict(lambda: defaultdict(list))
for key in seinfeld_dic:
    for key_2 in seinfeld_dic[key]:
        character_episode_dic[key_2][key].extend(seinfeld_dic[key][key_2])


character_dic = defaultdict(list)
for key in character_episode_dic:
    for key_2 in character_episode_dic[key]:
        character_dic[key].extend(character_episode_dic[key][key_2])

# Who has the most lines?
character_line_count = [(key, len(value)) for key, value in character_dic.items()]

# There are a lot of ancillary characters, so we'll look at characters with at least 100 lines
for character, count in sorted(character_line_count, key=lambda c: -c[1]):
    if count > 100: print(character, ' ', count)

# MAN and WOMAN are most certainly composites, so let's remove them, and consider the others

main_characters = [pair[0] for pair in character_line_count if pair[1] > 100 and pair[0] not in ['MAN', 'WOMAN']]

# We've seen who has the highest number of lines, but how about word count?

for character in main_characters:
    word_count = sum([len(line.split()) for line in character_dic[character]])
    print(character, ': ', word_count)

# No surprises, about the same. Seinfeld is the star, and he does monologues,
# so it's not surprising he has the most amount of lines

# Let's consider n-grams for each character

# Here is a very clever approach to finding n-grams in base python by Scott Triglia
# (http://locallyoptimal.com/)


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

# We'll also use a short list of stopwords

stop_words = ['i', 'a', 'about', 'an', 'are', 'as', 'at', 'be'
              , 'by', 'com', 'for', 'from', 'how', 'in', 'is', 'it', 'of'
              , 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when'
              , 'where', 'who', 'will', 'with', 'the']

# Create a single list for each character consisting of lowercase words

flat_character_dic = {}
for character in main_characters:
    character_lines = ' '.join([re.sub('[^a-zA-Z ]', '', line).lower() for line in character_dic[character]]).split()
    flat_character_dic[character] = [word for word in character_lines if word not in stop_words]

top_10_ngrams = {}
for i in range(1, 4):
    top_10_ngrams[i] = {}
    for character in main_characters:
        ngrams = find_ngrams(flat_character_dic[character], i)
        top_10_ngrams[i][character] = Counter(ngrams).most_common(10)

for character in main_characters:
    print(character)
    for item in top_10_ngrams[3][character]:
        print(item)

# It turns out the main characters are pretty similar

# Let's examine 'positivity' and 'negativity' of each character
# We'll download a list of positive and negative words, and count how often
# each character uses a positive or negative word
# (this is fairly naive)

negative_words = (urllib.request.urlopen('http://www.unc.edu/~ncaren/haphazard/negative.txt')
                  .read().decode('utf-8').split('\n'))
positive_words = (urllib.request.urlopen('http://www.unc.edu/~ncaren/haphazard/positive.txt')
                  .read().decode('utf-8').split('\n'))

positive_negative_count_dic = {}
for character in main_characters:
    negative_count = sum(1 if word in negative_words else 0 for word in flat_character_dic[character])
    positive_count = sum(1 if word in positive_words else 0 for word in flat_character_dic[character])
    positive_negative_count_dic[character] = (round(negative_count / len(flat_character_dic[character]), 3),
                                              round(positive_count / len(flat_character_dic[character]), 3))
    print(character, ': ', positive_negative_count_dic[character])

# Convert to a pandas dataframe and plot

positive_negative_df = pd.DataFrame.from_dict(positive_negative_count_dic, orient='index')
positive_negative_df.rename(columns={0: 'Negative', 1: 'Positive'}, inplace=True)
positive_negative_df = positive_negative_df.unstack(level=0).reset_index().rename(columns={'level_0': 'Sentiment',
                                                                                           'level_1': 'Character',
                                                                                           0: 'percent'})
ax = sns.barplot(x='Character', y='percent', hue='Sentiment', data=positive_negative_df)

# Newman is unexpectedly positive, the most positive character, according to this basic analysis







