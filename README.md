

# CSD-ProgLang-2018-1
python web-app backend with json API to access file system

Задания 1 и 2 выполняются совместно и должны иметь согласованные протоколы.

Задание 1 - написать на языке Python веб приложение реализующее json API методы
для доступа к файловой системе.

Необходимо реализовать веб приложение с использованием стандартного
BaseHTTPServer или wsgiref, в т.ч. допускается решения с использованием
программных каркасов Flask, Django, web2py, bottle.

Требуется реализовать методы перечисления файлов и папок по передаваемому
пути, удаленное скачивание файлов, создание и удаление пустых папок. По деланию
список может быть расширен заливкой/удалением файлов и т.п..

В настройках скрипта должна быть корневая директория, ограничивающая все
запросы клиента на данные директорий и папок вне ее поддерева.

По url / должен отдаваться код клиентского js приложения из здания 2 (можно
добавить позже, при сдаче 2 лабы). Для успешной сдачи необходимо предоставить
описание протокола и примеры url для тестирования всех методов из браузера.

Срок выполнения 1 задания - 15 ноября

# Starting server
`$ python3 main.py`

# JSON API
All methods GET

 1. Files and folders listing `ls`
    http://localhost:8000/[path]/?ls
	    `{
    "path": "/",
    "query": "ls",
    "result": [
        "data.json",
        "folder1"
    ]
	}`

 2. Downloading file `download`
    http://localhost:8000/[path_to_file]/[filename]?download

 3. Creating new empty folder `mkdir`
    http://localhost:8000/[path]/?mkdir
	    `{
    "path": "/not_found_folder/",
    "query": "mkdir",
    "result": "Success! Folder was created"
	}`

 4. Removing empty folder `rmdir`
    http://localhost:8000/[path]/?rmdir
	    `{
    "path": "/not_found_folder/",
    "query": "rmdir",
    "result": "Success! Folder was removed"
	}`

#### errors example
	`{
    "path": "[path]",
    "query": "",
    "error": "Not Correct Query"
	}`
	
	`{
    "path": "/not_found_folder/",
    "query": "ls",
    "error": "File Not Found"
	}`
