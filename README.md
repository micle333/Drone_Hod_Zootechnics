# Drone_Hod_Zootechnics
<br>

Привет, рады видеть тебя в нашем репозитории! Наша команда крутых и первоклассных специалистов Московского авиационного принимает участие в хакатоне "Ход дрона". Играем в овцу и волков. Название нашей команды: ЗооТехники.
<br> 



## Загрузка параметров настройки в QGroundControl
В окне Parameters находим в верхнем правом углу иконку "Tools". Производим загрузку.

![photo_2025-06-26_17-11-11](https://github.com/user-attachments/assets/a5fe9dc5-221f-4af5-b9a7-4528e9d9b1af)
![photo_2025-06-26_17-11-13](https://github.com/user-attachments/assets/5bdf1c3f-7216-4195-93d1-43d290ebe797)

## SSH-доступ

Запускаем терминал в Linux и выполняем команду:
```
 ssh pi@192.168.2.x
```
Пароль для доступа: raspberry

x - ip вашего дрона

1 - 6: 112.

2 - .

3 - .

4 - 4: 109.

## Загрузка карты

Создаем карту и добавляем в неё наши координаты.
```
~/catkin_ws/src/clover/aruco_pose/map $ nano chess_map.txt
```
Старое название карты меняем на новое в файле:
```
~/catkin_ws/src/clover/ $ cd clover/launch/
~/catkin_ws/src/clover/clover/launch $ nano.aruco.launch
```
## Конфигурация и настройка точек по карте
<br>
     ArUco-маркеры — это популярная технология для позиционирования робототехнических систем с использованием компьютерного зрения.
     Модуль aruco_map распознает карты ArUco-маркеров, как единое целое. Также возможна навигация по картам ArUco-маркеров с использованием механизма Vision Position Estimate (VPE).
     
Аргумент aruco находится в файле:
```
~/catkin_ws/src/clover/clover/launch/clover.launch
```

![image](https://github.com/user-attachments/assets/310ac756-5569-4619-84fe-da2bf6cb934b)

Перезагрузка дрона осуществляется по команде:

```
sudo systemctl restart clover
```
