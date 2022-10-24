from bs4 import BeautifulSoup
import json


def parse(exam_filename):
    with open(exam_filename, 'r', encoding='utf-8') as file:
        dom = BeautifulSoup(file, 'lxml')

    all_elements = dom.find('form', class_="questionflagsaveform").find("div").find_all('div', recursive=False, limit=40)

    questions = {}

    for element in all_elements:
        grade = element.find("div", class_="grade").text

        if grade != "Баллов: 1,00 из 1,00":
            continue

        qtext = element.find('div', class_='qtext').text.strip().replace('\n', ' ')

        ans = {}
        answers = element.find('div', class_="answer").find_all('div', recursive=False)

        for answer in answers:
            txt = answer.find('div').text.strip().replace('\n', ' ')
            val = 'correct' if answer.find('input').attrs.setdefault('checked', '') else 'incorrect'
            ans[txt] = val

        questions[qtext] = ans

    with open('answers.json', 'w', encoding='utf-8') as file:
        json.dump(questions, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    parse("bjhd.html")
