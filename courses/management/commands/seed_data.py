from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, Lesson


class Command(BaseCommand):
    help = 'Creates seed data for Banan platform'

    def handle(self, *args, **options):
        instructor, _ = User.objects.get_or_create(
            username='instructor',
            defaults={'email': 'instructor@banan.com'}
        )
        instructor.set_password('instructor123')
        instructor.save()

        categories_data = [
            ('oge-informatika', 'ОГЭ Информатика'),
            ('python', 'Python'),
            ('web', 'Веб-разработка'),
            ('data-science', 'Data Science'),
        ]
        categories = {}
        for slug, name in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            categories[slug] = cat

        courses_data = [
            {
                'title': 'ОГЭ по информатике 2026 — Полный курс по ФИПИ',
                'slug': 'oge-informatika-fipi',
                'short_description': 'Подготовка к ОГЭ по информатике с нуля. Все темы кодификатора ФИПИ.',
                'description': (
                    'Полный курс подготовки к ОГЭ по информатике по спецификации ФИПИ 2026 года.\n\n'
                    'Курс охватывает все темы кодификатора:\n'
                    '• Количественные параметры информационных объектов\n'
                    '• Кодирование и декодирование информации\n'
                    '• Логические выражения и таблицы истинности\n'
                    '• Алгоритмы и исполнители\n'
                    '• Программирование (Python)\n'
                    '• Информационные технологии\n'
                    '• Системы счисления\n'
                    '• Поиск информации\n\n'
                    'Каждый урок содержит теорию, примеры и задания.'
                ),
                'category': 'oge-informatika',
            },
            {
                'title': 'Python для начинающих',
                'slug': 'python-dlya-nachinayushih',
                'short_description': 'Изучите Python с нуля. Переменные, циклы, функции, ООП и проекты.',
                'description': (
                    'Полный курс Python для начинающих.\n\n'
                    'Вы научитесь:\n'
                    '• Писать программы на Python\n'
                    '• Работать с данными и файлами\n'
                    '• Создавать функции и классы\n'
                    '• Использовать библиотеки\n'
                    '• Писать тесты и отлаживать код\n\n'
                    'Курс подходит для абсолютных новичков.'
                ),
                'category': 'python',
            },
            {
                'title': 'Веб-разработка на Django',
                'slug': 'web-razrabotka-django',
                'short_description': 'Создавайте веб-приложения на Django. От основ до деплоя.',
                'description': (
                    'Научитесь создавать веб-приложения на Django.\n\n'
                    'Темы курса:\n'
                    '• Модели, шаблоны, представления\n'
                    '• Аутентификация и авторизация\n'
                    '• REST API на Django REST Framework\n'
                    '• Работа с базами данных\n'
                    '• Деплой на сервер\n\n'
                    'После курса вы сможете создавать свои проекты.'
                ),
                'category': 'web',
            },
            {
                'title': 'Основы Data Science',
                'slug': 'osnovy-data-science',
                'short_description': 'Введение в анализ данных: Pandas, NumPy, визуализация и ML.',
                'description': (
                    'Введение в мир Data Science.\n\n'
                    'Что вы изучите:\n'
                    '• Python для анализа данных\n'
                    '• Pandas и NumPy\n'
                    '• Визуализация данных\n'
                    '• Основы машинного обучения\n'
                    '• Работа с реальными датасетами\n\n'
                    'Базовые знания Python желательны.'
                ),
                'category': 'data-science',
            },
        ]

        for cd in courses_data:
            course, created = Course.objects.get_or_create(
                slug=cd['slug'],
                defaults={
                    'title': cd['title'],
                    'short_description': cd['short_description'],
                    'description': cd['description'],
                    'category': categories[cd['category']],
                    'instructor': instructor,
                    'price': 0,
                    'is_published': True,
                }
            )
            if created:
                self.stdout.write(f'  Created course: {cd["title"]}')
            else:
                self.stdout.write(f'  Already exists: {cd["title"]}')

        oge_lessons = [
            (1, 'Количественные параметры информационных объектов',
             'Единицы измерения информации: бит, байт, Кбайт, Мбайт. '
             'Перевод между единицами. Формула Хартли: N = 2^i. Решение задач.'),
            (2, 'Кодирование и декодирование информации',
             'Равномерное и неравномерное кодирование. Условие Фано. '
             'Кодирование текстовой, графической и звуковой информации.'),
            (3, 'Значение логического выражения',
             'Логические операции: НЕ, И, ИЛИ. Таблицы истинности. '
             'Законы алгебры логики. Упрощение выражений.'),
            (4, 'Алгоритмы и исполнители',
             'Исполнители: Черепаха, Робот, Чертёжник. '
             'Линейные алгоритмы и циклы. Анализ программ.'),
            (5, 'Программирование на Python',
             'Условный оператор if. Циклы for и while. '
             'Работа со строками и списками. Решение задач.'),
            (6, 'Системы счисления',
             'Двоичная, восьмеричная, десятичная, шестнадцатеричная системы. '
             'Перевод чисел. Сравнение.'),
            (7, 'Информационно-коммуникационные технологии',
             'IP-адресация. Маска подсети. URL. '
             'Поиск информации в Интернете.'),
            (8, 'Поиск в файловой системе',
             'Файловая система. Путь к файлу. Маски имён файлов. '
             'Поиск по маске.'),
            (9, 'Электронные таблицы',
             'Формулы в Excel. Абсолютные и относительные ссылки. '
             'Диаграммы. Анализ данных.'),
            (10, 'Анализ графов и схем',
             'Графы, деревья, таблицы. Кратчайшие пути. '
             'Чтение графов и схем.'),
            (11, 'Запросы к поисковому серверу',
             'Язык запросов. Круги Эйлера. '
             'Формула включений-исключений.'),
            (12, 'Расчёт информационного объёма',
             'Графические файлы: разрешение, глубина цвета. '
             'Аудиофайлы: частота дискретизации.'),
            (13, 'Оформление документов и презентаций',
             'Форматирование текста. Стили, списки, таблицы. '
             'Создание презентаций.'),
        ]
        oge_course = Course.objects.get(slug='oge-informatika-fipi')
        for order, title, content in oge_lessons:
            Lesson.objects.get_or_create(
                course=oge_course,
                slug=f'urok-{order}',
                defaults={'title': title, 'content': content, 'order': order}
            )

        python_lessons = [
            (1, 'Установка и Hello World', 'Установка Python, IDE. Первая программа.'),
            (2, 'Переменные и типы данных', 'Числа, строки, булевы значения. Ввод/вывод.'),
            (3, 'Условные операторы', 'if, elif, else. Логические операторы.'),
            (4, 'Циклы', 'for и while. Range. Вложенные циклы.'),
            (5, 'Функции', 'Создание функций. Аргументы. return. Области видимости.'),
            (6, 'Списки и словари', 'Работа со списками. Срезы. Словари.'),
            (7, 'Файлы и исключения', 'Чтение/запись файлов. try/except.'),
            (8, 'ООП', 'Классы и объекты. Наследование.'),
        ]
        python_course = Course.objects.get(slug='python-dlya-nachinayushih')
        for order, title, content in python_lessons:
            Lesson.objects.get_or_create(
                course=python_course,
                slug=f'urok-{order}',
                defaults={'title': title, 'content': content, 'order': order}
            )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
