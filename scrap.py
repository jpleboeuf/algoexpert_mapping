"""scrap AlgoExpert.io to extract the list of questions"""

from collections import namedtuple
import pickle
from pprint import pprint
from requests_html import HTMLSession

BASE_URL = 'https://www.algoexpert.io/questions'
session = HTMLSession()
response = session.get(BASE_URL)
if response.status_code != 200:
    raise SystemExit(f"Unexpected status code: {response.status_code}.")

print("Rendering webpage...")
response.html.render(sleep=1)  # Sleep a bit after the initial render - for React to do its magic?
print("Done.")

print("Scraping started :)")

# QuestionPage_QuestionList_Elements
qp_ql_element = response.html.find('.QuestionsPage-questionsList', first=True)
if qp_ql_element is None:
    raise SystemExit("Incomplete rendering! Please try again later...")

# QuestionPage_QuestionList_CategoryColumn_Elements
qp_ql_cc_elements = qp_ql_element.find('.QuestionsPage-categoryCol:not(.QuestionsPage-categoryCol--empty)')

Category = namedtuple('Category', ['id', 'title'])
categories = dict()
Question = namedtuple('Question', ['title', 'url'])
questions = dict()

print("Scraping the list of questions:")
for qp_ql_cc_element in qp_ql_cc_elements:
    cat_id = qp_ql_cc_element.attrs['id']
    (cat_title, cat_progress) = qp_ql_cc_element.find('.QuestionPage-categoryTitle', first=True).text.split(" - ")
    cat_key = cat_title.lower().replace(' ', '_')
    categories[cat_key] = Category(cat_id, cat_title)
    print(f"+ {categories[cat_key].title} (id:{categories[cat_key].id})...")
    questions_for_cat = list()
    # QuestionPage_QuestionPlaceholder_Elements
    qp_qp_elements = qp_ql_cc_element.find('.QuestionPage-questionPlaceholder+div span:first-child')
    for qp_qp_element in qp_qp_elements:
        q_title = qp_qp_element.text
        q_url = BASE_URL + '/' + qp_qp_element.text
        question = Question(q_title, q_url)
        questions_for_cat.append(question)
    questions[cat_key] = questions_for_cat

print("Scraping finished :)")

print()
pprint(questions)

print()
print("Saving questions on file...")
with open('questions.pickle', 'wb') as f:
    pickle.dump(questions, f)
print("Saving done :)")
