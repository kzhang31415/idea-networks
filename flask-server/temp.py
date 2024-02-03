# from flask import Flask
# from random_word import RandomWords
# import os
# nltk.download('gutenberg')
# nltk.download('wordnet')
import csv
import nltk
from nltk.corpus import gutenberg
from nltk.corpus import wordnet as wn
import random
import pandas as pd
from openai import OpenAI
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

client = OpenAI(
    # This is the default and can be omitted
    api_key = "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",
)
# client = OpenAI()
def genresponse(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

def related_words(root):
    p = "Can you give me a list of 10 "
    q = "things you would vaguely associate with the word "
    r = " across multiple contexts? Just the list and no explanations, please!"
    s_chat = genresponse(p + q + root + r).split(':')[-1]
    w_list = s_chat.split()
    return w_list
    

def simplify(s):
    p = "Can you summarize the most important concept of the phrase \""
    q = "\"? Please respond with one word."
    count = len(s.split())
    if count == 1:
        s_chat = s
    else:
        s_chat = genresponse(p + s + q)
    return ''.join([c.lower() for c in s_chat if c.isalpha()])
    
def get_graph(s1, s2):
    wG = nx.Graph()
    si = simplify(s1)
    target = simplify(s2)
    print(si)
    print(target)
    
    wG.add_nodes_from([
        (0, {'word' : target, 'synset' : wn.synsets(target)[0]}),
        (1, {'word' : si, 'synset' : wn.synsets(si)[0]})
    ])
    i = 1
    cur = wn.synsets(si)[0].path_similarity(wn.synsets(target)[0])
    
    w_queue = deque([(i, si)])
    seen_words = set()
    
    while not nx.is_connected(wG):
        w = w_queue.popleft()
        W_list = related_words(w[1])
        print(w[1])
        print(W_list)
        
        for r in W_list:
            r1 = ''.join([c.lower() for c in r if c.isalpha()])
            if r1 == target:
                wG.add_edge(w[0], 0)
                return wG
            elif r1 in seen_words or len(r1) <= 2 or len(wn.synsets(r1)) == 0:
                continue
            elif wn.synsets(r1)[0].path_similarity(wn.synsets(target)[0]) > cur:
                seen_words.add(r1)
                continue
            else:
                i += 1
                wG.add_node(i, word=r1, synset=wn.synsets(r1)[0])
                wG.add_edge(w[0], i)
                seen_words.add(r1)
                w_queue.append((i, r1))
        
        score = wn.synsets(w[1])[0].path_similarity(wG.nodes[0]['synset'])
        if score > 0.5:
            wG.add_edge(w[0], 0)
            return wG

    return wG


word_graph_test = get_graph('bush', 'tree')


# j = 0
# while j < len(wn.synsets(w[1])):
#     for t_set in wG.nodes[0]['synsets']:
#         score = wn.synsets(w[1])[j].path_similarity(t_set)
#         if score > 0.5:
#             wG.add_edge(w[0], 0)
#             nx.draw(wG)
#             plt.show()
#             return wG
#     j += 1        

# def gget_graph(s1, s2):
#     wG = nx.Graph()
#     si = simplify(s1)
#     target = simplify(s2)
#     print(si)
#     print(target)
    
#     wG.add_nodes_from([
#         (0, {'word' : si, 'synset' : wn.synsets(si)[0]}),
#         (1, {'word' : target, 'synset' : wn.synsets(target)[0]})
#     ])
#     i = 2
    
#     w_queue = deque([si])
#     seen_words = set()
    
#     while not nx.is_connected(wG):
#         w = w_queue.popleft()
#         if w in seen_words or len(w) <= 2 or len(wn.synsets(w)) == 0:
#             continue
#         else:
#             seen_words.add(w)
#         print(w)
#         W_list = related_words(si)
#         print(W_list)
#         for r in W_list:
#             r1 = ''.join([c.lower() for c in r if c.isalpha()])
#             if r1 == target:
#                 w_queue.appendleft(r1)
#             else:
#                 w_queue.append(r1)
#         connect_main = False
#         if len(wn.synsets(w)) == 0:
#             continue
#         w_set = wn.synsets(w)[0]
#         wG.add_node(i, word=w, synset=w_set)
#         i += 1
        
#         for idx in wG.nodes():
#             score = w_set.path_similarity(wG.nodes[idx]['synset'])
#             if 0.2 < score and score < 0.5:
#                 connect_main = True
#                 wG.add_edge(i-1, idx)
                    
#         if not connect_main:
#             i -= 1
#             wG.remove_node(i)
        
#     nx.draw(wG)
#     plt.show()
    
#     return wG


# prompt = "What's the most popular ski resort in Europe?"
# sample = genresponse("What's the most popular ski resort in Europe?")
# print(sample.choices[0].message.content)


# print(gen_response("Write a summary of the benefits of exercise."))

# app = Flask(__name__)

# Members API route
# @app.route("/members")
# def members():
#     return {"members": ["Member1", "Member2", "Member3"]}


# r = RandomWords()
# Return a single random word
# print(r.get_random_word())

# moby = set(nltk.Text(gutenberg.words('melville-moby_dick.txt')))
# moby = [word.lower() for word in moby if len(word) >2]
# moby_df = pd.DataFrame(moby)

# moby_df.to_csv('moby1.csv')

# if __name__ == "__main__":
#     app.run(debug=True)

# with open("moby1.csv", "r") as moby_file:
#     csv_reader = csv.reader(moby_file)
#     next(csv_reader)
#     data_words = [line[1] for line in csv_reader]
    # print(random.choice([line[1] for line in csv_reader]))
    
# def random_word():
#     return random.choice(data_words)