import urllib.request
import lxml.html
from collections import defaultdict
import re
import time
import pickle

# Gather the webpages that will serve as a source for character lines

# to begin, we need a list of the urls for the scripts
connection = urllib.request.urlopen('http://www.seinology.com/scripts-english.shtml')
html = lxml.html.document_fromstring(connection.read())
links = []
for element, attribute, link, pos in html.iterlinks():
    links.append(link)
# not all of the links are relevant
links = [link for link in links if 'scripts/script-' in link]

# There were several sources to select from. After working through different websites,
# with different formatting rules, I selected the one with the most consistent formatting,
# as far as I could tell. So, the processing is specific to this website
def process_lines(text):
    """
    :param text: a set of lines consisting of raw html, representing a Seinfeld script
    :return: a dictionary consisting of {Character1: [line1, line2,...], Character2: [line1, line2,...], ...}
    """
    d = defaultdict(list)
    # find indices to subset html to relevant lines
    start_end = [i for i, line in enumerate(text) if '=====' in line or 'the end' in line.lower()]
    text = text[start_end[0] + 1: start_end[-1]]
    # do some processing (strip characters, remove non-spoken lines (lines appearing within brackets or parentheses)
    # and blank lines. additionally, there are some unicode formatting issues that we'll try to resolve.
    text = [re.sub('\n|\t', '', t) for t in text]
    text = [re.sub('\[.+?\]|\(.+?\)', '', t) for t in text]
    text = [t for t in text if t != '']
    text = [t.replace('\x92', '\'') for t in text]
    # generally speaking, single lines consist of an entire line by a character. however, in some cases,
    # a line bleeds over to a second line. this next bit corrects that issue, blending those types of lines together
    output = []
    for i in range(len(text)):
        if re.search('^[A-Z]+:', text[i]):
            output.append(text[i])
        else:
            if len(output) > 0 and re.search('[a-zA-Z]$', output[-1]):
                output.append(' '.join([output.pop(), text[i]]))
    # here is where the dictionary is built; the format is 'CHARACTER: Line.'
    # so the first part is extracted as a key and the rest is added to a list of lines
    for line in output:
        semi = line.index(':')
        d[line[:semi]].append(line[semi + 1:])
    return d

# after a few iterations of development, i figured it would be easiest to download all the documents to the
# local machine and process them later
for link in links:
    url = 'http://www.seinology.com/' + link.strip('/')
    urllib.request.urlretrieve(url, 'C:/Users/ben/Desktop/seinfeld/' + link.strip('/'))

# Create a data structure to store data;
# in this first one, create a dictionary where the first level keys are episodes
# and the second level keys are the characters
seinfeld_dic = {}
for link in links:
    url = 'file:///C:/Users/ben/Desktop/seinfeld/' + link.strip('/')
    print(url)
    connection = urllib.request.urlopen(url)
    dom = lxml.html.fromstring(connection.read())
    # extract text from the script area of the page
    text = dom.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "spacer2", " " ))]//p//text()')
    print(link)
    # find the title of the episode
    title_line = [i for i, _ in enumerate(text) if re.search('Episodes? ?-? ?\d+&?\d* - (.+)', _)]
    title = re.search('Episodes? ?-? ?\d+&?\d* - (.+)', text[title_line[0]]).group(1)
    seinfeld_dic[title] = process_lines(text)

# Rearrange the data structures for different uses:
# in this first, we'll reverse the keys, making the characters the primary key,
# and the episodes secondary key
character_episode_dic = defaultdict(lambda: defaultdict(list))
for key in seinfeld_dic:
    for key_2 in seinfeld_dic[key]:
        character_episode_dic[key_2][key].extend(seinfeld_dic[key][key_2])

# Finally, we'll just flatten the dictionary, so that keys are characters, and the values are just
# lists of lines
character_dic = defaultdict(list)
for key in character_episode_dic:
    for key_2 in character_episode_dic[key]:
        character_dic[key].extend(character_episode_dic[key][key_2])

# We'll take an interest in George for the moment... so sort the George entry,
# and dump the list to file
george_sort = sorted(character_dic['GEORGE'], key=lambda x: -len(x))
with open('C:/Users/ben/Desktop/seinfeld/george.pickle', 'wb') as p:
    pickle.dump(george_sort, p)

# We'll also dump the main dictionary
with open('C:/Users/ben/Desktop/seinfeld/seinfeld.pickle', 'wb') as p:
    pickle.dump(seinfeld_dic, p)


