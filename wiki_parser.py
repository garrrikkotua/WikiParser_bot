from bs4 import BeautifulSoup
import wikipedia
import requests
import train
import generate
import re

"""
This script parses text
from wikipedia articles
(only works for english segment of wikipedia for now)
"""


def get_title(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'lxml')
    title = bs.title.string
    return title


def make_texts(file, root, depth, visited):
    if depth < 1:
        return
    try:
        page = wikipedia.page(root)
    except wikipedia.exceptions.DisambiguationError as e:
        return
    except wikipedia.exceptions.PageError as e:
        return
    for sentence in page.content.split('. '):
        file.write(' '.join(re.findall('[\w]+', sentence)))
        file.write('\n')
    visited.add(page.title)
    if depth == 1:
        return
    for link in page.links:
        if link in visited:
            continue
        make_texts(file, link, depth - 1, visited)


def prepare_to_generate(url, chat_id, depth=1):
    root = get_title(url)
    visited = set()
    texts = 'texts{}.txt'.format(chat_id)
    with open(texts, 'w', encoding='utf-8') as file:
        make_texts(file, root, depth, visited)
    model = 'model{}.txt'.format(chat_id)
    train.train(texts, model, False)


def generate_text(length, chat_id):
    model = 'model{}.txt'.format(chat_id)
    output = 'output{}.txt'.format(chat_id)
    with open(model, 'rb') as file:
        with open(output, 'w', encoding='utf-8') as out:
            generate.generate(file, '',
                              length, out)
