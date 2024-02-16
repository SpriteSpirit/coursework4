from src.user_interaction import *


def main_menu():
    """ Главное меню для выбора действий """

    print("(👉ﾟヮﾟ)👉 Добро пожаловать в JobFinder!\n")

    while True:
        print('Выберите пункт меню:')
        print('[1 : поиск вакансий]')
        print('[2 : поиск ТОП вакансий]')
        print('[3 : смотреть сохраненные вакансии]')
        print('[4 : редактировать сохраненные вакансии]')
        print('[0 : выйти]')

        user_choice = input('::=> ')

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                search_vacancies()
            elif user_choice == 2:
                search_top_vacancies()
            elif user_choice == 3:
                ask_to_view_saved_vacancies_list()
            elif user_choice == 4:
                ask_to_edit_saved_vacancies_list()
            elif user_choice == 0:
                print("Спасибо за то, что воспользовались JobFinder 👈(ﾟヮﾟ👈)")
                quit()
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')


if __name__ == '__main__':
    main_menu()
