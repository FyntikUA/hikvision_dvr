import requests
import logging
import schedule
import time
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth
from datetime import datetime

# Налаштування журналювання
logging.basicConfig(filename='dvr_camera_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Змінні для підключення
dvr_ip = '0.0.0.0'  # IP-адреса вашого DVR
dvr_port = 80
username = 'admin'  # Ім'я користувача
password = 'admin'  # Пароль

# URL для отримання інформації про канали
url = f'http://{dvr_ip}:{dvr_port}/ISAPI/System/Video/inputs/channels'

# Додаткові заголовки
headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml'
}

# Структура для зберігання попереднього стану камер
camera_status = {}
connection_lost_time = None

def log_status_change(camera_id, resolution, enabled, start_time, end_time):
    logging.warning(f"{camera_id} - changed to 'NO VIDEO' or 'false' at {start_time}")
    logging.warning(f"Change started at: {start_time}, ended at: {end_time}")
    logging.warning(f"Duration: {end_time - start_time}")

def check_camera_status():
    global camera_status, connection_lost_time
    
    try:
        print("Sending request to DVR...")
        # Відправка запиту до DVR
        response = requests.get(url, auth=HTTPDigestAuth(username, password), headers=headers)
        logging.debug(response.text)
        print(f"Response status code: {response.status_code}")

        print(camera_status)

        # Перевірка успішності запиту
        if response.status_code == 200:
            print("Successfully retrieved data.")
            logging.info("-" * 24 + 'Start' + "-" * 24)
            logging.info("Successfully retrieved data:")
            if connection_lost_time:
                logging.warning(f"Connection restored at: {datetime.now()}, Downtime: {datetime.now() - connection_lost_time}")
                connection_lost_time = None

            # Парсинг XML
            root = ET.fromstring(response.text)
            current_time = datetime.now()

            # Ітерація по камерах з id 1, 2, ...
            valid_camera_ids = {1, 2, 3, 4, 5, 6, 7, 8}
            for channel in root.findall('.//{http://www.hikvision.com/ver20/XMLSchema}VideoInputChannel'):
                id_elem = channel.find('{http://www.hikvision.com/ver20/XMLSchema}id')
                if id_elem is not None and int(id_elem.text) in valid_camera_ids:
                    name_elem = channel.find('{http://www.hikvision.com/ver20/XMLSchema}name')
                    enabled_elem = channel.find('{http://www.hikvision.com/ver20/XMLSchema}videoInputEnabled')
                    resolution_elem = channel.find('{http://www.hikvision.com/ver20/XMLSchema}resDesc')

                    # Перевірка на наявність елементів
                    camera_id = id_elem.text if id_elem is not None else 'N/A'
                    name_cam = name_elem.text if name_elem is not None else 'N/A'
                    enabled = enabled_elem.text if enabled_elem is not None else 'N/A'
                    resolution = resolution_elem.text if resolution_elem is not None else 'N/A'
                    if resolution == 'NO VIDEO':
                        logging.warning(f"{name_cam}: {resolution}")
                    if enabled == 'false':
                        logging.warning(f"{name_cam}: offline, reason: {enabled}")

                    # Перевірка на зміну стану
                    if camera_id in camera_status:
                        prev_status = camera_status[camera_id]
                        if (resolution == 'NO VIDEO' or enabled == 'false') and not prev_status['issue']:
                            prev_status['issue'] = True
                            prev_status['start_time'] = current_time
                        elif (resolution != 'NO VIDEO' and enabled != 'false') and prev_status['issue']:
                            prev_status['issue'] = False
                            end_time = current_time
                            log_status_change(camera_id, resolution, enabled, prev_status['start_time'], end_time)
                    else:
                        camera_status[camera_id] = {
                            'issue': resolution == 'NO VIDEO' or enabled == 'false',
                            'start_time': current_time if resolution == 'NO VIDEO' or enabled == 'false' else None
                        }
            logging.info("-" * 25 + 'End' + "-" * 25)

        else:
            # Фіксація помилки підключення
            if connection_lost_time is None:
                connection_lost_time = datetime.now()
                print(f"Failed to get camera list. Status code: {response.status_code}")
                logging.error(f"Failed to get camera list. Status code: {response.status_code}")

    except Exception as e:
        if connection_lost_time is None:
            connection_lost_time = datetime.now()
            print(f"Connection lost at: {connection_lost_time}")
            logging.error(f"Connection lost at: {connection_lost_time}")
        print(f"Error: {e}")
        

# Перевірка стану камер при запуску
check_camera_status()

# Планування завдання кожні 3 хвилини
schedule.every(3).minutes.do(check_camera_status)

# Основний цикл для виконання запланованих завдань
while True:
    schedule.run_pending()
    time.sleep(1)
