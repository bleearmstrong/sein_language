import pickle
from collections import Counter

seinfeld_dic = pickle.load(open('C:/Users/ben/Desktop/seinfeld/seinfeld.pickle', 'rb'))

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
              , 'by'  , 'com', 'for', 'from', 'how', 'in', 'is', 'it', 'of'
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








