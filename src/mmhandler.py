from sql_module.sql import SQL
import datetime
from dateutil import relativedelta

"""
MoneyMoney handler for all calculating functions.
"""


# # маленький контекстный менеджер для работы с БД
# class Sqltor(object):
#     def __init__(self, sql):
#         self.sql = sql
#         self.sql.open()
#
#     def __enter__(self):
#         return self.sql
#
#     def __exit__(self, *args):
#         self.sql.close()


class MmHandler:
    def __init__(self, user_id):
        self.user_id = user_id
        try:
            self.sql = SQL()
        except Exception as e:
            print('Ошибка при создании базы данных: {}'.format(e))

    def start(self):
        try:
            self.sql.add_user(self.user_id)
        except Exception as e:
            return 'Ошибка при инициализации: {} '.format(e)
        else:
            return  'Привет! Чтобы узнать о моих возможностях,'\
                       'воспользуйся командой /help'

    def add_operation(self, amount, category=None, description=None, date=None):
        print(amount)
        print(self.user_id)
        print(category)
        try:
            if category is None:
                category = 'other'
            categories = set(self.sql.get_all_categories(self.user_id))
            if category in categories:
                self.sql.add_operation(self.user_id, amount, category, date, description)
            else:
                return 'Такой категории не существует! Воспользуйтесь ' \
                       'функцией "добавить категорию".'
        except Exception as e:
            return 'Операция не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Операция успешно добавлена.'

    def show_categories(self, mode=None):
        try:
            if mode == 'income':
                categories_list = self.sql.get_income_categories(self.user_id)
            elif mode == 'expense':
                categories_list = self.sql.get_expense_categories(self.user_id)
            else:
                categories_list = self.sql.get_all_categories(self.user_id)
        except Exception as e:
            return 'Вывод категорий невозможен! Ошибка: {} '.format(e)
        else:
            message = 'Список категорий:' + ', '.join(categories_list)
            return message

    def add_category(self, name):
        try:
            self.sql.add_category(name, self.user_id)
        except Exception as e:
            return 'Категория не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно добавлена.'

    def del_category(self, name):
        try:
            self.sql.delete_category(name, self.user_id)
        except Exception as e:
            return 'Категория не была удалена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно удалена.'

    def view_report(self, period=None):
        if period == 'year':
            delta = relativedelta.relativedelta(years=1)
        elif period == 'month':
            delta = relativedelta.relativedelta(months=1)
        elif period == 'week':
            delta = relativedelta.relativedelta(weeks=1)
        elif period == 'day':
            delta = relativedelta.relativedelta(days=1)
        else:
            delta = None
        try:
            if delta is None:
                history = self.sql.get_history(self.user_id)
            else:
                date_to = datetime.datetime.now()
                date_from_str = (date_to - delta).strftime("%Y-%m-%d")
                date_to_str = date_to.strftime("%Y-%m-%d")
                history = self.sql.get_history(self.user_id, date_from_str, date_to_str)
        except Exception as e:
            return 'Получить историю невозможно! Ошибка: {} '.format(e)
        else:
            message = 'История операций за'
            if period is not None:
                message += ' {}'.format(period)
            str_history = str(history)[1:-1]
            return message + '\n' + str_history

    def view_custom_report(self, date_from, date_to=None):

        try:
            if date_to is None:
                history = self.sql.get_history(self.user_id, date_from)
            else:
                history = self.sql.get_history(self.user_id, date_from, date_to)
        except Exception as e:
            return 'Получить историю невозможно! Ошибка: {} '.format(e)
        else:
            message = 'История операций c {}'.format(date_from)
            if date_to is not None:
                message += ' по {}'.format(date_to)
            str_history = str(history)[1:-1]
            return message + '\n' + str_history
