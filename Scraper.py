import requests
import csv
from bs4 import BeautifulSoup

CSV = "vacancy.csv"
URL = "https://career.habr.com/vacancies?page=1&q=python&sort=date&type=all"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;"
    "q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu;"
    " Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
}


def get_html(urs, params: dict = ""):
    r = requests.get(urs, headers=HEADERS, params=params)
    return r


def get_vacancy(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="vacancy-card")
    vacancy = []

    for item in items:
        vacancy.append(
            {
                "company": item.find(
                    "div", class_="vacancy-card__company-title"
                ).get_text("href"),
                "vacancy": item.find(
                    "a", class_="vacancy-card__title-link").get_text(
                    strip=False
                ),
                "skills": item.find(
                    "div", class_="vacancy-card__skills").get_text(
                    strip=False
                ),
                "meta": item.find(
                    "div", class_="vacancy-card__meta").get_text(
                    strip=False
                ),
                "salary": item.find(
                    "div", class_="basic-salary").get_text(
                    strip=False
                    ),
                "date": item.find(
                    "time", class_="basic-date").get_text(
                    strip=False
                ),
                "link_vacancy": "https://career.habr.com"
                + item.find(
                    "a", class_="vacancy-card__title-link").get(
                    "href"
                ),
            }
        )

    return vacancy


def save_vacancy(items, path):
    with open(path, "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Название компании",
                "Вакансия",
                "Требования по вакансии",
                "Город, уловия",
                "Зарплата",
                "Дата публикации",
                "Ссылка на вакансию",
            ]
        )
        for item in items:
            writer.writerow(
                [
                    item["company"],
                    item["vacancy"],
                    item["skills"],
                    item["meta"],
                    item["salary"],
                    item["date"],
                    item["link_vacancy"],
                ]
            )


def parser():
    paginator = int(10)  # количество страниц для парсинга.
    html = get_html(URL)
    if html.status_code == 200:
        vacancy = []
        for page in range(1, paginator):
            print(f"идет парсинг страницы №{page}")
            html = get_html(URL, params={"page": page})
            vacancy.extend(get_vacancy(html.text))
            save_vacancy(vacancy, CSV)
        print("Парсинг окончен")
    else:
        print("Error")


parser()
