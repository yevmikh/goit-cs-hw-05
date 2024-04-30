import string
import asyncio
from collections import defaultdict, Counter

import httpx
import nltk
from nltk.corpus import stopwords
from matplotlib import pyplot as plt

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

async def get_text(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

async def map_function(word) -> tuple:
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

async def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

async def map_reduce(text, search_words=None):
    text = remove_punctuation(text).lower()
    words = text.split()


    words = [word for word in words if word not in stop_words and word.strip()]


    if search_words:
        words = [word for word in words if word in search_words]


    mapped_values = await asyncio.gather(*[map_function(word) for word in words])

    shuffled_values = shuffle_function(mapped_values)


    reduced_values = await asyncio.gather(*[reduce_function(key_values) for key_values in shuffled_values])

    return dict(reduced_values)

def visual_result(result, search_words=None):
    if search_words:
        title = 'Amount of searched words in text:'
    else:
        title = '10 Most Popular Words'

    top_10 = Counter(result).most_common(10)
    labels, values = zip(*top_10) if result else ([], [])
    plt.figure(figsize=(10, 5))
    plt.barh(labels, values, color='g')
    plt.xlabel('Amount')
    plt.ylabel('Word')
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = asyncio.run(get_text(url))

    if text:
        search_option = input("Would you like search the words in text? (y/n): ").strip().lower()
        search_words = None
        if search_option == 'y':
            search_words_input = input("Enter the words separated by commas for which to perform the search: ")
            search_words = [word.strip().lower() for word in search_words_input.split(',')]
            result = asyncio.run(map_reduce(text, search_words))
            visual_result(result, search_words)
        else:
            result = asyncio.run(map_reduce(text))
            visual_result(result)
    else:
        print("Faild to load text")

