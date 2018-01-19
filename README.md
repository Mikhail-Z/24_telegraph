# Клон сайта telegra.ph

## Описание

Этот сайт является клоном telephra.ph, но на русском языке.
Позволяет анонимно публиковать заметки, менять их содержание
 и полностью удалять в течение года.
 
## Системные требования

Любой современный браузер с поддержкой html5. Для развертывния на локальном 
компьютере нужен python3.3 или выше.

## Развертывание на локальном компьютере

Сначала нужно установить необходимые библиотеки
```
$ pip install -r requirements.txt
```
Далее нужно создать базу данных. В корневой папке проекта:
```
$ python3
>>> from server import db
>>> db.create_all() 
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
