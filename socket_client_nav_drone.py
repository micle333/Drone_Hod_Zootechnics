import rospy
import socket
import threading
from clover import srv
from clover.srv import SetLEDEffect, GetTelemetry
import logging
import pathlib
import sys
from skyros.drone import Drone

# === Настройки сокета ===
SERVER_IP = '192.168.2.136'
PORT = 6003

# Настройка логгирования
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("drone_1.log", encoding="utf-8"),
        logging.StreamHandler()  # Вывод в консоль
    ]
)

# === Инициализация ROS сервисов ===
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
peer = Drone(pathlib.Path(__file__).parent / "zenoh-config.json5")
peer.logger.setLevel(logging.INFO)
peer.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
rospy.init_node(peer.name)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
get_telemetry = rospy.ServiceProxy('get_telemetry', GetTelemetry)

# === Глобальная переменная для передачи команд между потоками ===
command_queue = []
command_lock = threading.Lock()



# === Логика клиента (в отдельном потоке) ===
def socket_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, PORT))
            print("[Клиент] Подключено к серверу")

            while True:
                data = s.recv(1024)
                if not data:
                    print("[Клиент] Сервер закрыл соединение.")
                    break
                command = data.decode().strip()
                print(f"[Команда получена]: {command}")

                with command_lock:
                    command_queue.append(command)

        except ConnectionRefusedError:
            print(f"[Ошибка] Не удалось подключиться к {SERVER_IP}:{PORT}")
        except Exception as e:
            print(f"[Ошибка сети]: {e}")
        finally:
            print("[Клиент] Соединение закрыто.")

# def navigate_to(plate): 
#     play_led_effect('blue')
#     print(f"Navigating to waypoint: {plate}, {points[plate]} ")
#     navigate(x=0, y=0, z=1, frame_id='body', auto_arm=True)
#     navigate(frame_id='aruco_73', x=0, y=0, z=1.5)
#     print(f"Takeoff:")
#     peer.wait(5)
#     navigate(frame_id='aruco_73', x=0, y=0, z=0.25) 
#     peer.wait(5)
#     navigate(frame_id='aruco_73', x=0, y=0, z=0.15) 
#     peer.wait(5)    
#     navigate(frame_id='aruco_140', x=0, y=0, z=0.15) 
#     print(f"Land:")
#     peer.land()
#     play_led_effect('green')

def navigate_to(plate): 
    play_led_effect('blue')
    print(f"Navigating to waypoint: {plate}, {points[plate]} ")
    navigate(x=0, y=0, z=1, frame_id='body', auto_arm=True)
    navigate(frame_id='aruco_24', x=0, y=0, z=1.5)
    print(f"Takeoff:")
    peer.wait(5)
    navigate(frame_id='aruco_24', x=0, y=0, z=0.25) 
    peer.wait(5)
    navigate(frame_id='aruco_24', x=0, y=0, z=0.15) 
    peer.land()
    play_led_effect('green')

# === Функция обработки команд ===
def process_commands():
    global command_queue
    while command_queue:
        with command_lock:
            command = command_queue.pop(0)
            command = command.split()
            print(command, len(command))
        
        if command[0] == "nav_to":
            navigate_to(command[1])
            print(f"NAV: {command[1]}")

        elif command[0] == "led":
            print(f"LED: {command[1]}")
            play_led_effect(command[1])
    return True

# === Функция воспроизведения эффекта на LED ===
def play_led_effect(effect):
    if effect == "red":
        set_effect(r=255, g=0, b=0)
    elif effect == "green":
        set_effect(r=0, g=255, b=0)
    elif effect == "blue":
        set_effect(r=0, g=0, b=255)
    elif effect == "off":
        set_effect(r=0, g=0, b=0)
    else:
        print(f"[LED] Неизвестный эффект: {effect}")

# === Точки движения дрона ===
points = {
    'a1': [-1.3125, -1.3125, 1.5],
    'a3': [-1.3125, -0.5625, 1.5],
    'g7': [0.9375, 0.9375, 1.5],
    # ... другие точки
}

# === Запуск сокет-клиента в отдельном потоке ===
socket_thread = threading.Thread(target=socket_client, daemon=True)
socket_thread.start()

with peer:
    logger.info("Drone started...")
    logger.info("Waiting for other drones...")
    peer.wait_for_peer_amount(0)
    logger.info(f"Connected peers: {peer.get_peers()}")

    running = True

    while running and not rospy.is_shutdown():
        running = process_commands()
        rospy.sleep(0.1)
