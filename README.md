## 1. Установка:
#### Для управления зависимостями используется Poetry
#### Установите Poetry, если он ещё не установлен

## 2. В корне проекта создайте файл .env со следующим содержимым:

####   Postgres

`POSTGRES_DB=social_network_db`

`POSTGRES_USER=postgres`

`POSTGRES_PASSWORD=postgres`

####  Service

`APP_NAME=social_network`

`DB__HOST=db`

`DB__PORT=5433`

`DB__USER=postgres`

`DB__PASSWORD=postgres`

`DB__DB=social_network_db`

## 3. Запуск проекта в Docker:
#### `docker-compose build`

#### `docker-compose up -d`

#### Контейнер с приложением будет доступен на http://localhost:8000

## 4. Инициализация базы данных
#### Для создания таблиц выполните команду в терминале (psql должен быть установлен локально):
```psql -h localhost -p 5433 -U postgres -d social_network_db -f create_tables.sql```
### Затем ввести пароль от postgres

## 5. Использование Postman-коллекции
#### Импортируйте коллекцию в Postman, выберите нужный запрос и нажмите "Send".
