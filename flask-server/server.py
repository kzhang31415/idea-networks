<<<<<<< HEAD
=======
from flask import Flask, request
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


app = Flask(__name__)

# @app.route("/members")
# def members():
#     return {"members": ["Member1", "Member2", "Member3"]}

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

with open("moby1.csv", "r") as moby_file:
    csv_reader = csv.reader(moby_file)
    next(csv_reader)
    data_words = [line[1] for line in csv_reader]
    # print(random.choice([line[1] for line in csv_reader]))
    
def random_word():
    return random.choice(data_words)

def simplify(s):
    p = "Can you summarize the most important concept of the phrase \""
    q = "\"? Please respond with one word."
    count = len(s.split())
    if count == 1:
        s_chat = s
    else:
        s_chat = genresponse(p + s + q)
    return ''.join([c.lower() for c in s_chat if c.isalnum()])
    
def get_graph(s1, s2):
    wG = nx.Graph()
    si = simplify(s1)
    target = simplify(s2)
    # print(si)
    # print(target)
    threshold = 0.05
    
    wG.add_nodes_from([
        (0, {'word' : si, 'synset' : wn.synsets(si)[0]}),
        (1, {'word' : target, 'synset' : wn.synsets(target)[0]})
    ])
    i = 2
    
    while not nx.is_connected(wG):
        w = random_word()
        connect = False
        # you want to check w's similarity against each word in the graph wG
        print(w)
        if len(wn.synsets(w)) == 0:
            continue
        w_set = wn.synsets(w)[0]
        wG.add_node(i, word=w, synset=w_set)
        i += 1
        
        for idx in wG.nodes():
            score = w_set.path_similarity(wG.nodes[idx]['synset'])
            if score > threshold:
                connect = True
                wG.add_edge(i-1, idx)
        
        if not connect:
            i -= 1
            wG.remove_node(i)
        else:
            wG.remove_edge(i-1, i-1)
    
    return wG

# wG.nodes[idx]['word'] gives the word itself (node.name)
# idx is the word's index in the graph (node.index)
# wG.edges[i] is a tuple (i,j) where i and j are the indices of the nodes connected by the edge

@app.route("/make_graph")
def make_graph():
    args = request.args
    s1 = args.get("s1")
    s2 = args.get("s2")
    nodes, edges = [], []
    graph = get_graph(s1, s2)
    for idx in range(0, len(graph.nodes)):
        if(graph.nodes[idx]['word'] != s1 and graph.nodes[idx]['word'] != s2):
            nodes.append({"id": idx, "name" : graph.nodes[idx]['word'], "type": "interior"})
    for edge in graph.edges:
        edges.append({"source": edge[0], "target": edge[1]})
    for node in nodes:
        print(node)
    return {"nodes": list(nodes), "links": list(edges)}

# prompt = "What's the most popular ski resort in Europe?"
# sample = genresponse("What's the most popular ski resort in Europe?")
# print(sample.choices[0].message.content)


# print(gen_response("Write a summary of the benefits of exercise."))



# r = RandomWords()
# Return a single random word
# print(r.get_random_word())

# moby = set(nltk.Text(gutenberg.words('melville-moby_dick.txt')))
# moby = [word.lower() for word in moby if len(word) >2]
# moby_df = pd.DataFrame(moby)

# moby_df.to_csv('moby1.csv')


if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 2f82e530e3195d0ccf165baf431d52741ac7aecf
