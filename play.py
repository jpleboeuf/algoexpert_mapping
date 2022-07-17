"""play with questions scraped from AlgoExpert.io"""

from collections import namedtuple
import pickle
from pprint import pprint

Category = namedtuple('Category', ['id', 'title'])
Question = namedtuple('Question', ['title', 'url'])

with open('questions.pickle', 'rb') as f:
    questions = pickle.load(f)

pprint(questions)

print()
cat_tot = {}
for c, qs in questions.items():
    cat_tot[c] = len(qs)
pprint(cat_tot)
print(f"Total number of questions: {sum(cat_tot.values())}.")
