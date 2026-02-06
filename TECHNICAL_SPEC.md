# ТЕХНИЧЕСКОЕ ЗАДАНИЕ
## PHS APP v2.0
**Pharmaceutical Healthcare System**

**Система управления визитами медицинских представителей**

**Версия:** 2.0  
**Дата:** Декабрь 2025

---

## 🎯 ОБЩЕЕ ОПИСАНИЕ ПРОЕКТА
- **Название:** PHS App (Pharmaceutical Healthcare System)
- **Назначение:** Система управления визитами медицинских представителей к врачам, аптекам и дистрибьюторам
- **Платформа:** Telegram Mini App (WebApp)
- **Целевая аудитория:** Медицинские представители фармацевтических компаний

---

## 📊 АРХИТЕКТУРА СИСТЕМЫ

### 🗄️ База данных

**Таблица: `users` (Пользователи/Сотрудники)**

| Поле | Тип | Описание |
| --- | --- | --- |
| user_id | INTEGER PRIMARY KEY | Telegram ID |
| name | TEXT NOT NULL | ФИО сотрудника |
| phone | TEXT UNIQUE | Телефон (+998901234567) |
| region | TEXT NOT NULL | Регион работы |
| pin | TEXT NOT NULL | PIN-код (4 цифры) |
| position | TEXT | Должность |
| is_blocked | INTEGER DEFAULT 0 | Статус блокировки |

**Таблица: `doctors` (Врачи)**

Основные поля: `id`, `full_name`, `specialty`, `organization`, `phone`, `address`, `latitude`, `longitude`, `region`, `category`, `notes`, `is_active`

**Таблица: `pharmacies` (Аптеки)**

Основные поля: `id`, `name`, `network`, `address`, `phone`, `latitude`, `longitude`, `pharmacist_name`, `category`, `is_active`

**Таблица: `distributors` (Дистрибьюторы)**

Основные поля: `id`, `company_name`, `contact_person`, `position`, `phone`, `email`, `address`, `latitude`, `longitude`, `category`

**Таблица: `visits` (Визиты)**

Основные поля: `id`, `user_id`, `visit_type`, `target_id`, `target_name`, `visit_date`, `duration`, `topics`, `result`, `products_presented`, `orders_received`, `latitude`, `longitude`, `location_verified`, `photo_url`, `notes`, `next_visit_date`

**Таблица: `visit_reminders` (Напоминания)**

Основные поля: `id`, `user_id`, `target_type`, `target_id`, `last_visit_date`, `recommended_visit_date`, `reminder_sent`, `priority`

---

## 🤖 TELEGRAM БОТ - СТРУКТУРА

### 1. Первый запуск (незарегистрированный)
**Команда:** `/start`

**Ответ бота:**
```
👋 Привет, [Имя]!
🎉 Добро пожаловать в PHS App!
⚠️ Для использования необходима регистрация.
```
**Кнопка:** 📝 Зарегистрироваться (WebApp)

### 2. Регистрация (WebApp)
**Шаг 1:** ФИО, Телефон (+998), Регион, Должность  
**Шаг 2:** Установка PIN (4 цифры)  
**Шаг 3:** Подтверждение PIN  
**Шаг 4:** Выбор языка (Русский/O'zbek)

**Обработка:** `tg.sendData()` → `bot.py` → `registration.py` → `database.py`

### 3. Главное меню
После регистрации пользователь получает клавиатуру:
- 🏠 Главное меню (WebApp)
- 👤 Мой профиль
- ❓ Помощь

---

## 📱 ФУНКЦИОНАЛЬНОСТЬ WEBAPP

### Главное меню WebApp

| Кнопка | Функция |
| --- | --- |
| 📝 Визит | Регистрация визита к врачу/аптеке/дистрибьютору |
| 🗺️ Карта | Интерактивная карта с точками объектов + GPS |
| 📅 План | Планирование визитов на день/неделю |
| 📚 База | База врачей, аптек, дистрибьюторов |
| 📊 Отчеты | Статистика визитов, выполнение плана |
| ⚙️ Настройки | Язык, PIN-код, профиль |

### Регистрация визита
1. Выбор типа: Врач / Аптека / Дистрибьютор
2. Поиск цели: По имени, организации или GPS (ближайшие)
3. Детали визита:
   - Дата и время
   - Длительность
   - Темы обсуждения
   - Представленные продукты
   - Заметки
   - Фото (опционально)
   - GPS координаты (автоматически)
4. GPS-проверка: Если расстояние >500м от цели → предупреждение
5. Сохранение: `tg.sendData()` → `visits.py` → `database.visits`

---

## 🗺️ GPS TRACKING И MAPPING

### Технологии
- Карты: Leaflet.js или Yandex Maps API
- GPS: `navigator.geolocation.getCurrentPosition()`
- Хранение: `latitude`, `longitude` в БД (REAL)

### Функции карты
1. Маркеры:
   - 🔵 Врачи
   - 🟢 Аптеки
   - 🟡 Дистрибьюторы
   - 🔴 Непосещенные >30 дней
2. Фильтры: По типу, категории, региону
3. Поиск: Ближайшие объекты в радиусе
4. Клик на маркер: Информация + кнопка "Начать визит"
5. Маршруты: Оптимальный путь по плану на день

---

## 🔔 СИСТЕМА НАПОМИНАНИЙ

### Автоматические напоминания
**Скрипт:** `reminder_scheduler.py` (cron каждый час)

**Логика:**
1. Поиск врачей/аптек/дистрибьюторов без визита >30 дней
2. Создание записи в `visit_reminders`
3. Отправка уведомления в Telegram

**Частота напоминаний:**
- Категория A: каждые 14 дней
- Категория B: каждые 21 день
- Категория C: каждые 30 дней

---

## 🔌 API ENDPOINTS

### Пользователи
- `GET  /api/user/{id}`
- `POST /api/register`
- `POST /api/login`

### Врачи
- `GET  /api/doctors`
- `GET  /api/doctors/{id}`
- `GET  /api/doctors/nearby?lat={lat}&lon={lon}&radius={m}`
- `POST /api/doctors`

### Визиты
- `GET  /api/visits`
- `GET  /api/visits/user/{user_id}`
- `POST /api/visits`

---

## 💻 ТЕХНОЛОГИЧЕСКИЙ СТЕК

### Backend
- Python 3.10+
- python-telegram-bot — Telegram Bot API
- Flask — API сервер
- SQLite — База данных

### Frontend (WebApp)
- HTML5 + CSS3 + JavaScript
- Telegram WebApp API
- Leaflet.js — Карты
- Chart.js — Графики

### Deployment
- GitHub Pages — WebApp
- VPS/Cloud — Backend
- Nginx — Reverse proxy
- Systemd — Автозапуск

---

## 📅 ЭТАПЫ РАЗРАБОТКИ

| Фаза | Задачи | Статус |
| --- | --- | --- |
| Фаза 1 | Базовая регистрация, вход по PIN | ✅ Завершено |
| Фаза 2 | База врачей + регистрация визитов | 🔄 В разработке |
| Фаза 3 | Карта + GPS tracking | ⏳ Запланировано |
| Фаза 4 | Аптеки + дистрибьюторы | ⏳ Запланировано |
| Фаза 5 | Напоминания + планирование | ⏳ Запланировано |
| Фаза 6 | Отчеты + статистика | ⏳ Запланировано |
| Фаза 7 | Админ-панель расширенная | ⏳ Запланировано |
| Фаза 8 | Оптимизация + тестирование | ⏳ Запланировано |

---

_Конец документа_  
ТЗ v2.0 — Декабрь 2025
