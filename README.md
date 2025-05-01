# Мой Блог

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)](https://flask.palletsprojects.com)

Блог-платформа с возможностью публикации статей, тегами и категориями.

## Особенности

- 📝 Создание и редактирование публикаций
- 🏷️ Система тегов и категорий
- 🔐 Аутентификация пользователей
- 🔍 Поиск по контенту

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Yar-Den/flask-blog.git
cd flask-blog
```
2. Установите зависимости
```bash
pip install -r requirements.txt
```
3. Настройте окружение:
```bash
cp .env.example .env
```

## Конфигурация
Файл .env:
```ini
SECRET_KEY=ваш-секретный-ключ
DATABASE_URI=sqlite:///instance/blog.db
```

## Инициализация БД
1. Создайте базу данных:
```bash
flask db init
flask db upgrade
```
2. Заполните тестовыми данными (также будет создан пользователь admin admin)
```bash
python create_db.py
```

## Запуск
```bash
flask run
```
Приложение будет доступно по адресу: http://localhost:5000

## Структура проекта
├── app.py
├── create_db.py
├── requirements.txt
├── migrations/
├── instance/
├── static/
│   ├── css/
│   └── images/
├── templates/
│   ├── auth/
│   ├── includes/
│   └── *.html
└── .env.example
