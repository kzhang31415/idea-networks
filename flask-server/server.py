<<<<<<< HEAD
=======
from flask import Flask, request
import csv
import nltk
from nltk.corpus import gutenberg
from nltk.corpus import wordnet as wn
import random
import pandas as pd
from openai import OpenAI
import networkx as nx


app = Flask(__name__)


client = OpenAI(
    api_key = "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",
)

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

    


if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 2f82e530e3195d0ccf165baf431d52741ac7aecf
