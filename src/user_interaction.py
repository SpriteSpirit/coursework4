from data.hh_api import HeadHunterAPI
from src.vacancy import Vacancy
from storage.json_saver import JSONSaver

user_data = JSONSaver()
user_list = user_data.user_list


def get_vacancies_by_user_query_with_salary() -> list:
    """ Принимает от пользователя город, запрос и зарплату для сортировки """

    city = input("Укажите город: ")
    query = input("Введите запрос поиска: ")
    salary = int(input("Минимальная зарплата: "))

    vacancies = get_vacancies_by_query(city, query)
    sort_by_salary = Vacancy.cast_to_object_list_by_salary(vacancies, salary)

    return sort_by_salary


def get_vacancies_by_user_query() -> list:
    """ Принимает от пользователя город и запрос для сортировки """

    city = input("Укажите город: ")
    query = input("Введите запрос поиска: ")

    vacancies = get_vacancies_by_query(city, query)
    sort_by_query = Vacancy.cast_to_object_list(vacancies)

    return sort_by_query


def get_vacancies_by_query(city: str, query: str) -> list:
    """ Возвращает список вакансий hh по запросу и городу, без зарплаты """

    hh_api = HeadHunterAPI()
    city_id = HeadHunterAPI.get_city_id_by_name(city_name=city)
    hh_vacancies = hh_api.get_vacancies(city_id, query)

    return hh_vacancies


def get_sorted_vacancies(vacancies: list, is_ascending_order: bool = True) -> list:
    """ Сортирует вакансии по возрастанию зарплаты """

    return sorted(vacancies, reverse=not is_ascending_order)


def info_template(counter: int, vacancy) -> None:
    """ Шаблон вывода информации по каждой вакансии """

    print('-' * 50)
    print(f'{" " * 18}Вакансия #{counter + 1}')
    print('-' * 50)
    print(f'Город: {vacancy.city}')
    print(f'Название: {vacancy.title}')
    if isinstance(vacancy.salary, list):
        print(f'Зарплата от {vacancy.salary[0]} до {vacancy.salary[1]} [RUB]')
    else:
        print(f'Зарплата от {vacancy.salary} [RUB]')
    print(f'Требования: {vacancy.description}', flush=True)
    print(f'Опыт работы: {vacancy.experience}')
    print(f'Ссылка на вакансию: {vacancy.url}\n')


def display_vacancies(vacancies: list, is_ask_to_save: bool = False) -> None:
    """ Вывод вакансий полностью и поштучно """

    print(Vacancy.get_founded_vacancies(vacancies))
    input(':: нажмите ENTER, чтобы продолжить ::')

    if not is_ask_to_save:
        for i, vacancy in enumerate(vacancies):
            info_template(i, vacancy)
    else:
        for i, vacancy in enumerate(vacancies):
            info_template(i, vacancy)

            if ask_to_save_vacancy():
                add_vacancy_to_list(vacancy)

    print(f'Показаны все {len(vacancies)} вакансии\n')


def ask_to_view_all() -> bool:
    """ Спрашивает у пользователя как показать вакансии: поштучно или все """

    while True:
        print('Как хотите посмотреть вакансии?')
        print('[1 : посмотреть все вакансии]')
        print('[2 : посмотреть вакансии поштучно]')
        print('[0 : вернуться в меню]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                return True
            elif user_choice == 2:
                return False
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


# !---------------------------------------------!
def search_vacancies() -> None:
    # формирует список вакансий в зависимости от того, что выбрал пользователь (с зп - False или без - True)
    # пользователь выбрал фильтр с зп
    create_filter = ask_to_create_filter()

    if not create_filter and create_filter is not None:
        # получаем вакансии с фильтром по зарплате
        result = get_vacancies_by_user_query_with_salary()
        # пользователь хочет посмотреть все вакансии
        if ask_to_view_all():
            # пользователь хочет отсортировать вакансии по возрастанию зп
            if ask_to_sort_vacancies():
                sort_vacancies = get_sorted_vacancies(result)
                display_vacancies(sort_vacancies)
                # пользователь хочет сохранить список вакансий
                if ask_to_save_vacancies():
                    save_all_vacancies(sort_vacancies, 'favourite_vacancies')
            # пользователь не хочет сортировать вакансии по возрастанию зп
            else:
                display_vacancies(result, True)
                if ask_to_save_vacancies():
                    save_all_vacancies(result, 'favourite_vacancies', True)
        # пользователь хочет посмотреть вакансии с зп поштучно
        else:
            # пользователь хочет отсортировать вакансии по возрастанию зп
            if ask_to_sort_vacancies():
                sorted_vacancies = get_sorted_vacancies(result)
                display_vacancies(sorted_vacancies, True)
                if ask_to_save_vacancies():
                    save_all_vacancies(sorted_vacancies, 'favourite_vacancies', True)
            else:
                display_vacancies(result, True)
                if ask_to_save_vacancies():
                    save_all_vacancies(result, 'favourite_vacancies', True)
    # пользователь выбрал фильтр с без зп
    elif create_filter:
        query_vacancies = get_vacancies_by_user_query()
        display_vacancies(query_vacancies)
        should_save = ask_to_save_vacancies()

        if should_save:
            save_all_vacancies(query_vacancies, 'favourite_vacancies')
    elif create_filter is None:
        return


def search_top_vacancies():
    top_vacancies = get_slice_top_vacancies()
    display_vacancies(top_vacancies)
    if ask_to_save_vacancies():
        save_all_vacancies(top_vacancies, 'top_vacancies')


def ask_to_create_filter() -> bool:
    """ Запрашивает у пользователя вариант просмотра вакансии """

    while True:
        print('Как будем искать вакансии?')
        print('[1 : посмотреть все вакансии по запросу]')
        print('[2 : посмотреть вакансии с фильтром по зарплате]')
        print('[0 : вернуться в меню]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                return True
            elif user_choice == 2:
                return False
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


def ask_to_save_vacancy() -> bool:
    """ Запрашивает у пользователя сохранение одной вакансии """

    while True:
        print('Сохранить вакансию в избранное?')
        print('[1 : да]')
        print('[2 : нет]')
        print('[0 : завершить]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                return True
            elif user_choice == 2:
                return False
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


def ask_to_save_vacancies() -> bool:
    """ Запрашивает у пользователя сохранение всех добавленных вакансии """

    while True:
        print('Сохранить список вакансий?')
        print('[1 : да]')
        print('[2 : нет]')
        print('[0 : завершить]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                return True
            elif user_choice == 2:
                return False
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


def ask_to_sort_vacancies() -> bool:
    """ Спрашивает у пользователя желает ли тот провести сортировку списка вакансий в порядке возрастания """

    while True:
        print('Желаете отсортировать вакансии в порядке возрастания зарплаты?')
        print('[1 : да]')
        print('[2 : нет]')
        print('[0 : завершить]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                return True
            elif user_choice == 2:
                return False
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


def add_vacancy_to_list(vacancy) -> None:
    """ Добавляет указанную вакансию в список вакансий для сохранения """

    user_data.add_vacancy(vacancy)


def save_all_vacancies(vacancies_list: list, filename: str, has_one_before: bool = False) -> None:
    """ Сохраняет все выбранные вакансии в указанный файл """

    if vacancies_list is not None and len(vacancies_list) != 0:
        if not has_one_before:
            for vacancy in vacancies_list:
                add_vacancy_to_list(vacancy)

        JSONSaver.save_json(user_list, filename)
    else:
        print('Список вакансий пуст. Нет данных для сохранения\n')


# формирование топ-вакансий
def get_top_vacancies_by_salary() -> list:
    """ Сортирует вакансии по возрастанию зарплаты """

    vacancies = get_vacancies_by_user_query_with_salary()
    sorted_top_vacancies = get_sorted_vacancies(vacancies)

    return sorted_top_vacancies


def ask_to_slice_top_vacancies() -> bool:
    """ Спрашивает у пользователя желает ли тот выполнить срез ТОП вакансий для просмотра """

    while True:
        print('Желаете указать количество ТОП вакансий для просмотра?')
        print('[1 : да]')
        print('[2 : нет]')
        print('[0 : завершить]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                return True
            elif user_choice == 2:
                return False
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


def get_slice_top_vacancies() -> list:
    """ Возвращает срез ТОП вакансий """

    top_vacancies = get_top_vacancies_by_salary()

    print(Vacancy.get_founded_vacancies(top_vacancies))

    result = ask_to_slice_top_vacancies()

    if result and result is not None:
        while True:
            print("Введите количество вакансий для просмотра:")
            number = input('::=> ')

            try:
                number = int(number)

                if number > len(top_vacancies):
                    return Vacancy.get_sorted_vacancies(top_vacancies, is_slice=True, slice_num=len(top_vacancies))
                else:
                    return Vacancy.get_sorted_vacancies(top_vacancies, is_slice=True, slice_num=number)
            except ValueError:
                print('Неверный ввод. Попробуйте снова.')
    elif not result:
        return top_vacancies
    else:
        return


def load_and_view_saved_vacancies(filename: str) -> None:
    """ Загружает и выводит список сохраненных вакансий """

    saved_data = JSONSaver.load_json(filename)
    display_vacancies([Vacancy(**data) for data in saved_data['items']])


# просмотр сохраненных вакансий
def ask_to_view_saved_vacancies_list() -> None:
    """ Спрашивает у пользователя какой список он желает посмотреть """

    while True:
        print('Выберите действие:')
        print('[1 : просмотр избранных вакансий]')
        print('[2 : просмотр ТОП вакансий]')
        print('[0 : завершить]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                load_and_view_saved_vacancies('favourite_vacancies')
            elif user_choice == 2:
                load_and_view_saved_vacancies('top_vacancies')
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


# редактирование вакансий
def ask_to_edit_saved_vacancies_list() -> None:
    """ Спрашивает у пользователя какой список тот желает отредактировать """

    while True:
        print('Выберите действие:')
        print('[1 : редактировать список избранных вакансий]')
        print('[2 : редактировать список ТОП вакансий]')
        print('[0 : выйти в главное меню]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                edit_saved_vacancy('favourite_vacancies')
            elif user_choice == 2:
                edit_saved_vacancy('top_vacancies')
            elif user_choice == 0:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


def edit_saved_vacancy(filename: str) -> None:
    """ Удаляет указанную пользователем вакансию """

    load_and_view_saved_vacancies(filename)

    while True:
        print('Введите номер вакансии для удаления:')
        print('[0 : выйти в главное меню]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice != 0:
                JSONSaver.delete_vacancy(user_data, user_choice, filename)
                break
            else:
                break
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')
