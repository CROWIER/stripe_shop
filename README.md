1. Клонирование проекта
bashgit clone https://github.com/CROWIER/stripe_shop.git
2. Настройка переменных окружения
Создайте файл .env в корне проекта по образу env.example:
3. Собарть docker-compose up --build
4. docker-compose up
5. Приложение: http://localhost:8000
Админ панель: http://localhost:8000/admin/

Логин: admin
Пароль: admin123

g
Тест товара: http://localhost:8000/item/1/
Тест заказа: http://localhost:8000/order/1/