# Проект FastAPI с грибами и корзинами

Этот проект представляет собой API на основе FastAPI для управления грибами и корзинами.

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <URL_репозитория>
   cd <имя_папки_репозитория>
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

## Настройка окружения

Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные окружения:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=Ваш_пароль
POSTGRES_DB=db
POSTGRES_HOST=db
POSTGRES_PORT=5432
FILE_STORAGE_DIR=/путь/к/вашей/директории
```

## Запуск проекта

1. **Запустите Docker контейнеры:**
   Убедитесь, что у вас установлен Docker и Docker Compose. Затем выполните команду:
   ```bash
   docker-compose up --build
   ```

2. **Запустите приложение:**
   Если вы не используете Docker, вы можете запустить приложение с помощью Uvicorn:
   ```bash
   uvicorn app:app --reload
   ```

## Доступ к API

После запуска приложения вы можете получить доступ к API по следующему адресу:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Эндпоинты

- **Создать гриб**: `POST /mushrooms/`
- **Получить гриб по ID**: `GET /mushrooms/{mushroom_id}`
- **Создать корзинку**: `POST /baskets/`
- **Добавить гриб в корзинку**: `POST /baskets/{basket_id}/mushrooms/{mushroom_id}`
- **Удалить гриб из корзинки**: `DELETE /baskets/{basket_id}/mushrooms/{mushroom_id}`
- **Получить корзинку по ID**: `GET /baskets/{basket_id}`