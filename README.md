# fastapi-detection

Этот проект предоставляет API для работы с видео, включая загрузку, обработку.

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
