from requests_html import HTMLSession
from collections import namedtuple
from pprint import pprint

BASE_URL = 'https://www.algoexpert.io/questions'
session = HTMLSession()
response = session.get(BASE_URL)
if response.status_code != 200:
    raise SystemExit(f"Unexpected status code: {response.status_code}.")

print("Rendering webpage...")
response.html.render(sleep=1)  # Sleep a bit after the initial render - for React to do its magic?
print("Done.")

qp_ql_element = response.html.find('.QuestionsPage-questionsList', first=True)
if qp_ql_element == None:
    raise SystemExit("Incomplete rendering! Please try again later...")

qp_ql_cc_elements = qp_ql_element.find('.QuestionsPage-categoryCol:not(.QuestionsPage-categoryCol--empty)')
Category = namedtuple('Category', ['id', 'title'])
categories = dict()
Question = namedtuple('Question', ['title', 'url'])
questions = dict()
print("Scraping the list of questions:")
for qp_ql_cc_element in qp_ql_cc_elements:
    id = qp_ql_cc_element.attrs['id']
    title = qp_ql_cc_element.find('.QuestionPage-categoryTitle', first=True).text.split(" - ")[0]
    cat = title.lower().replace(' ', '_')
    categories[cat] = Category(id, title)
    print(f"+ {categories[cat].title} (id:{categories[cat].id})...")
    questions_for_cat = list()
    qp_qp_elements = qp_ql_cc_element.find('.QuestionPage-questionPlaceholder+div span:first-child')
    for qp_qp_element in qp_qp_elements:
        title = qp_qp_element.text
        url = BASE_URL + '/' + qp_qp_element.text
        question = Question(title, url)
        questions_for_cat.append(question)
    questions[cat] = questions_for_cat
print("Scraping finished :)")

print()
pprint(questions)
