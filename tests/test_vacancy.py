import pytest

from src.vacancy import Vacancy


def test_vacancy_creation():
    vacancy = Vacancy("Moscow", "Developer", "http://example.com", 100000, "Development", "No experience", "Full-time")
    assert vacancy.city == "Moscow"
    assert vacancy.title == "Developer"
    assert vacancy.url == "http://example.com"
    assert vacancy.salary == 100000
    assert vacancy.description == "Development"
    assert vacancy.experience == "No experience"
    assert vacancy.schedule == "Full-time"


def test_vacancy_salary_comparison():
    vacancy_low = Vacancy("City", "Title1", "Link1", 50000, "Desc1", "Exp1", "Schedule1")
    vacancy_high = Vacancy("City", "Title2", "Link2", 100000, "Desc2", "Exp2", "Schedule2")

    assert vacancy_low < vacancy_high
    assert not vacancy_high < vacancy_low
    assert vacancy_low <= vacancy_high
    assert not vacancy_high <= vacancy_low


def test_vacancy_to_json():
    vacancy = Vacancy("City", "Title", "Link", 70000, "Desc", "Exp", "Schedule")
    expected_json = {
        "city": "City",
        "title": "Title",
        "url": "Link",
        "salary": 70000,
        "description": "Desc",
        "experience": "Exp",
        "schedule": "Schedule",
    }

    assert vacancy.cast_to_json_format() == expected_json


def test_to_parent_dict():
    vacancies_list = [Vacancy("City1", "Title1", "Link1", 50000, "Desc1", "Exp1", "Schedule1").cast_to_json_format(),
                      Vacancy("City2", "Title2", "Link2", 100000, "Desc2", "Exp2", "Schedule2").cast_to_json_format()]

    parent_dict = Vacancy.cast_to_parent_dict(vacancies_list)
    assert parent_dict == {"items": vacancies_list}


def test_get_founded_vacancies():
    vacancies_list = [Vacancy("City1", "Title1", "Link1", 50000, "Desc1", "Exp1", "Schedule1"),
                      Vacancy("City2", "Title2", "Link2", 100000, "Desc2", "Exp2", "Schedule2")]

    result_str = Vacancy.get_founded_vacancies(vacancies_list)
    assert result_str == "\nНайдено вакансий по запросу: 2\n"
