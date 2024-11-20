# fastapi-detection

Этот проект предоставляет API для работы с видео, включая загрузку, обработку.

## Requirements

Ensure you have the following installed:

- [Python 3.11+](https://www.python.org/downloads/)
- [Virtual Environments with Python 3.11+](https://docs.python.org/3/tutorial/venv.html)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Запуск проекта

- ```bash
    cd procject/image-fatapi
    docker-compose up --build
    ```

## Описание эндпойнтов

- ##### POST /video/upload/local

  Загружает видеофайл с локального устройства, обрабатывает его (выделяет кадры) и возвращает результат.

  Параметры:

  - **video_settings**: JSON с настройками обработки видео.
    - **fps**: float = 1.5 - количество кадров
    - **save_pattern**: str = f'frame%05d.jpg' - паттерн сохранения кадров
    - **zipped**: bool = True - вернуть zip архивом, иначе просто относительные пути до фреймов
    - **timecodes**: List | None = None - таймкоды для вырезания с видео
      Пример: ["3:45-6:34", "3:44-4:34"]
  - **video_file**: Файл видео, загружаемый пользователем. Загружается только с популярными расширениями видео.

  Результат:
  Список кадров, если zipped=False или zip архив, содержащий кадры.

- ##### POST /video/upload/link

  Загружает видео по ссылке с ютуба, обрабатывает его и возвращает результат.

  Параметры:

  - **video_link**: JSON с URL видео и настройками обработки.

    - **fps**: float = 1.5 - количество кадров
    - **save_pattern**: str = f'frame%05d.jpg' - паттерн сохранения кадров
    - **zipped**: bool = True - вернуть zip архивом, иначе просто относительные пути до фреймов
    - **timecodes**: List | None = None - таймкоды для вырезания с видео
      Пример: ["3:45-6:34", "3:44-4:34"] -

    * **link**: str - ссылка на ютуб видео, загружает только с сайт youtube.

  Результат:
  Список кадров, если zipped=False или zip архив, содержащий кадры.

- ##### GET /video/select/all

  Возвращает список путей с папками всех видео.

  Результат:
  JSON со списком относительных путей видео.

## Пример

##### Запрос к эндройнту "/video/upload/local"

  ```python
import requests, json, zipfile, io

video_settings = {
    "fps": 2,
    "save_pattern": "frame_%05d.jpg",
    "timecodes": None,  # или список, например ["00:00:10-00:00:20"]
    "zipped": True
}

url ="http://127.0.0.1:8000/video/upload/local"
file = "/Users/kekehaha/Downloads/file_example_MOV_1920_2_2MB.mov"
    
with open(file, "rb") as video_file:
    response = requests.post(
        url,
        files={"video_file": video_file},  # Файл отправляется как часть формы
        data={"video_settings": json.dumps(video_settings)},
    )

if response.status_code == 200:
    # Сохранение полученного архива
    zip_data = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_data) as zip_file:
        # Список всех файлов в архиве
        file_list = zip_file.namelist()
        print("Содержимое архива:", file_list)
else:
    # Вывод ошибки, если запрос не выполнен
    print("Ошибка:", response.status_code)
    print("Ответ:", response.text)
```
##### Вывод нашей программы, которая показывает содержимое отправленного нам zipfile с нарезанным фото.
```zsh
python train.py
Содержимое архива: ['frame_00059.jpg', 'frame_00058.jpg', 'frame_00060.jpg', 'frame_00048.jpg', 'frame_00049.jpg', 'frame_00012.jpg', 'frame_00006.jpg',
'frame_00007.jpg', 'frame_00013.jpg', 'frame_00039.jpg', 'frame_00005.jpg', 'frame_00011.jpg', 'frame_00010.jpg', 'frame_00004.jpg', 'frame_00038.jpg',
'frame_00014.jpg', 'frame_00028.jpg', 'frame_00029.jpg', 'frame_00015.jpg', 'frame_00001.jpg', 'frame_00017.jpg', 'frame_00003.jpg', 'frame_00002.jpg',
'frame_00016.jpg', 'frame_00033.jpg', 'frame_00027.jpg', 'frame_00026.jpg', 'frame_00032.jpg', 'frame_00018.jpg', 'frame_00024.jpg', 'frame_00030.jpg',
'frame_00031.jpg', 'frame_00025.jpg', 'frame_00019.jpg', 'frame_00021.jpg', 'frame_00035.jpg', 'frame_00009.jpg', 'frame_00008.jpg', 'frame_00034.jpg',
'frame_00020.jpg', 'frame_00036.jpg', 'frame_00022.jpg', 'frame_00023.jpg', 'frame_00037.jpg', 'frame_00050.jpg', 'frame_00044.jpg', 'frame_00045.jpg',
'frame_00051.jpg', 'frame_00047.jpg', 'frame_00053.jpg', 'frame_00052.jpg', 'frame_00046.jpg', 'frame_00042.jpg', 'frame_00056.jpg', 'frame_00057.jpg',
'frame_00043.jpg', 'frame_00055.jpg', 'frame_00041.jpg', 'frame_00040.jpg', 'frame_00054.jpg']
```
