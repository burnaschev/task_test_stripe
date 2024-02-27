## Установка и запуск 

Следуйте этим шагам для установки и запуска проекта.

### Клонирование проекта

git clone https://github.com/burnaschev/Electronics_network


### Создание и активация виртуального окружения

python3 -m venv venv
source venv/bin/activate

### Переменные окружения

Все необходимые переменные окружения находятся в файле .env_sample

Нужно создать свой переменные окружения в файле .env

### Установка зависимостей

pip install -r requirements.txt


### Запуск сервера 

python manage.py runserver

После чего вы сможете получить доступ к API по адресу `http://localhost:8000/`.


## Docker

Если вы предпочитаете использовать Docker:

1. Соберите образ:

    ```bash
    docker-compose build
    ```

2. Запустите контейнер:

    ```bash
    docker-compose up -d
    ```

Приложение будет доступно по адресу http://localhost:8080/.
