"""Парсинг hh-ru."""
import requests
import sqlite3

headers = {
    "User-agent": "MyHHParser/1.0 (nurbaevdaniar0@yandex.ru)"
}
PER_PAGE = 100
PAGES = 10


def parse_hh_ru():
    """Парсим hh-ru."""
    vacancies = []
    for page in range(0, PAGES):
        params = {
            "text": "",
            "page": page,
            "per_page": PER_PAGE,
        }
        response = requests.get(
            "https://api.hh.ru/vacancies",
            params=params,
            headers=headers
        )
        vacancies += response.json()["items"]

    return vacancies


def formdb(vacancies):
    """Заполняем базу данных вакансиями."""
    con = sqlite3.connect('hh_api/db.sqlite3')
    cur = con.cursor()
    for v in vacancies:
        try:
            # Добавляем отдельно соответсвующие города, категории и компании
            city = (
                v["area"]["id"],
                v["area"]["name"]
            )
            employer = (
                v["employer"]["id"],
                v["employer"]["name"]
            )
            category = (
                v["professional_roles"][0]["id"],
                v["professional_roles"][0]["name"]
            )

            # Парсим описание вакансии
            response = requests.get(
                f"https://api.hh.ru/vacancies/{v['id']}",
                headers=headers
            )
            vac = response.json()
            description = vac["description"] if "description" in vac.keys() else ""
            print(description)

            # Проверяем зарплату
            if v["salary"] is None:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = v["salary"]["from"]
                salary_to = v["salary"]["to"]

            vacancy = (
                int(v["id"]),
                v["name"],
                description,
                salary_from,
                salary_to,
                int(category[0]),
                int(city[0]),
                int(employer[0])
            )
            # Вставляем данные в базу
            cur.execute(
                'INSERT OR IGNORE INTO works_cities VALUES(?, ?);',
                city
            )
            cur.execute(
                'INSERT OR IGNORE INTO works_employers VALUES(?, ?);',
                employer
            )
            cur.execute(
                'INSERT OR IGNORE INTO works_categories VALUES(?, ?);',
                category
            )
            cur.execute(
                'INSERT OR IGNORE INTO works_vacancies VALUES(?, ?, ?, ?, ?, ?, ?, ?);',
                vacancy
            )
        except Exception as e:
            print(e)
    con.commit()
    con.close()


formdb(parse_hh_ru())
