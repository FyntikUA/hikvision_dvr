# Відстеження Стану Камер DVR

Цей скрипт відстежує стан камер, підключених до DVR, та фіксує будь-які зміни в їх стані, особливо коли камера показує "NO VIDEO" або виходить з ладу. Також фіксуються проблеми з підключенням до DVR.

## Вимоги

- Python 3.x
- Бібліотека `requests`
- Бібліотека `schedule`

## Встановлення

1. **Клонування репозиторію або завантаження скрипта:**

    ```sh
    git clone https://github.com/FyntikUA/hikvision_dvr
    cd https://github.com/FyntikUA/hikvision_dvr
    ```

2. **Створення віртуального середовища:**

    ```sh
    python -m venv venv
    ```

3. **Активація віртуального середовища:**

    - На Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - На MacOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Встановлення необхідних бібліотек:**

    ```sh
    pip install -r requirements.txt
    ```

## Використання

1. **Запуск скрипта:**

    ```sh
    python monitor_cameras.py
    ```

2. **Перевірка файлу журналу:**

    Скрипт створить файл журналу з назвою `baza_camera_log.txt` у тій же директорії, де зберігатимуться журнали станів камер та проблем з підключенням.

## Налаштування

- Оновіть змінні `dvr_ip`, `dvr_port`, `username` та `password` у скрипті відповідно до даних для підключення до вашого DVR.

## Структура файлів

```plaintext
.
├── monitor_cameras.py  # Основний скрипт
├── requirements.txt    # Список необхідних бібліотек
└── README.md           # Цей файл README
