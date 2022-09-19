# Учебный проект "Продуктовый помощник"


## Автор - Домнина Анастасия


# Оглавление

1. [Стек технологий](#Стек-технологий)
2. [Описание workflow](#Описание-workflow)
3. [Базовые модели проекта](#Базовые-модели-проекта)
4. [Главная страница](#Главная-страница)
5. [Страница рецепта](#Страница-рецепта)
6. [Страница пользователя](#Страница-пользователя)
7. [Подписка на авторов](#Подписка-на-авторов)
8. [Список избранного](#Список-избранного)
9. [Список покупок](#Список-покупок)
10. [Фильтрация по тегам](#Фильтрация-по-тегам)
11. [Регистрация и авторизация](#Регистрация-и-авторизация)
12. [Что могут делать неавторизованные пользователи](#Что-могут-делать-неавторизованные-пользователи)
13. [Что могут делать авторизованные пользователи](#Что-могут-делать-авторизованные-пользователи)
14. [Что может делать администратор](#Что-может-делать-администратор)
15. [Настройки админки](#Настройки-админки)
16. [Технические требования и инфраструктура](#Технические-требования-и-инфраструктура)
17. [Шаблон наполнения .env файла](#шаблон-наполнения-env-файла)


## Стек технологий

[![Django-app workflow](https://github.com/foxygen-d/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/foxygen-d/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)


## Описание workflow

* проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
* сборка и доставка докер-образа для контейнера web на Docker Hub
* автоматический деплой проекта на боевой сервер


## Базовые модели проекта

### Рецепт - все поля обязательны для заполнения

* Автор публикации (пользователь)
* Название
* Картинка
* Текстовое описание
* Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения
* Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных)
* Время приготовления в минутах


### Тег - все поля обязательны для заполнения и уникальны

* Название
* Цветовой HEX-код (например, #49B64E)
* Slug


### Ингредиент - все поля обязательны для заполнения

Данные об ингредиентах хранятся в нескольких связанных таблицах. В результате на стороне пользователя ингредиент должен описываться такими полями:

* Название
* Количество
* Единицы измерения


## Главная страница

Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым)

Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация


## Страница рецепта

На странице — полное описание рецепта

Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта


## Страница пользователя

На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя


## Подписка на авторов

Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

Сценарий поведения пользователя:
1. Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
2. Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
3. При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».


## Список избранного

Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.

Сценарий поведения пользователя:
1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
2. Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
3. При необходимости пользователь может удалить рецепт из избранного.


## Список покупок

Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

Сценарий поведения пользователя:
1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
2. Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
3. При необходимости пользователь может удалить рецепт из списка покупок.

Список покупок скачивается в формате .txt (или, по желанию, можно сделать выгрузку PDF).

При скачивании списка покупок ингредиенты в результирующем списке не должны дублироваться; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке должен быть один пункт: Сахар — 15 г.

В результате список покупок может выглядеть так:
* Фарш (баранина и говядина) (г) — 600
* Сыр плавленый (г) — 200
* Лук репчатый (г) — 50
* Картофель (г) — 1000
* Молоко (мл) — 250
* Яйцо куриное (шт) — 5
* Соевый соус (ст. л.) — 8
* Сахар (г) — 230
* Растительное масло рафинированное (ст. л.) — 2
* Соль (по вкусу) — 4
* Перец черный (щепотка) — 3


## Фильтрация по тегам

При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.

При фильтрации на странице пользователя должны фильтроваться только рецепты выбранного пользователя. Такой же принцип должен соблюдаться при фильтрации списка избранного.


## Регистрация и авторизация

### Обязательные поля для пользователя

* Логин
* Пароль
* Email
* Имя
* Фамилия

### Уровни доступа пользователей

* Гость (неавторизованный пользователь)
* Авторизованный пользователь
* Администратор


## Что могут делать неавторизованные пользователи

* Создать аккаунт
* Просматривать рецепты на главной
* Просматривать отдельные страницы рецептов
* Просматривать страницы пользователей
* Фильтровать рецепты по тегам


## Что могут делать авторизованные пользователи

* Входить в систему под своим логином и паролем
* Выходить из системы (разлогиниваться)
* Менять свой пароль
* Создавать/редактировать/удалять собственные рецепты
* Просматривать рецепты на главной
* Просматривать страницы пользователей
* Просматривать отдельные страницы рецептов
* Фильтровать рецепты по тегам
* Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов
* Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок
* Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок


## Что может делать администратор

Администратор обладает всеми правами авторизованного пользователя

Плюс к этому он может:
* изменять пароль любого пользователя
* создавать/блокировать/удалять аккаунты пользователей
* редактировать/удалять любые рецепты
* добавлять/удалять/редактировать ингредиенты
* добавлять/удалять/редактировать теги


## Настройки админки

### Модели

* Вывести все модели с возможностью редактирования и удаления записей

### Модель пользователей:

* Добавить фильтр списка по email и имени пользователя

### Модель рецептов:

* В списке рецептов вывести название и автора рецепта
* Добавить фильтры по автору, названию рецепта, тегам
* На странице рецепта вывести общее число добавлений этого рецепта в избранное

### Модель ингредиентов:

* В список вывести название ингредиента и единицы измерения
* Добавить фильтр по названию


## Технические требования и инфраструктура

* Проект должен использовать базу данных PostgreSQL
* Код должен находиться в репозитории `foodgram-project-react`
* В Django-проекте должен быть файл `requirements.txt` со всеми зависимостями
* Проект нужно запустить в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на вашем сервере в Яндекс.Облаке. Образ с проектом должен быть запушен на Docker Hub


## Шаблон наполнения .env файла

```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
POSTGRES_HOST=db
DB_PORT=5432
SECRET_KEY='m@o%(t!^b1o^q+x#8&d9a#sta@_^zs0+(v+o5_70s&y8@oz00+'
```