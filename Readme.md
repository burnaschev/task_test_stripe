<<<<<<< HEAD


=======
## Описание ТЗ
stripe.com/docs - платёжная система с подробным API и бесплатным тестовым режимом для имитации и тестирования платежей. 
С помощью python библиотеки stripe можно удобно создавать платежные формы разных видов, сохранять данные клиента, и реализовывать прочие платежные функции. 

## Технологии

- python
- django
- postgresql
- stripe
- docker
- docker-compose

## Эндпоинты

- /buy/{id} c помощью которого можно получить Stripe Session Id для оплаты выбранного продукта.
- /item/{id} c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном продукте и кнопка Купить
- order/create создание заказа
- order/payment оплата данного заказа
- toggle_item/{id} добавление и удаление товаров к заказу

## Модели
- Items
- Tax
- Discount
- Orders
  
## Админ панель Django

Для редактирования заказов, продуктов, скидок и налога 
>>>>>>> master

## Установка и запуск 

Следуйте этим шагам для установки и запуска проекта.

### Клонирование проекта

git clone https://github.com/burnaschev/task_test_stripe

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
