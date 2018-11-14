import wsgiref.util
from wsgiref.simple_server import make_server
import json
import os

BASE_ROOT_PATH = "./temp_file_folder"

def file_server(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    start_response(status, headers)

    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    query = environ['QUERY_STRING']

    print(path)
    print(query)

    response = {'path': path, 'query': query}

    if query == "ls":
        try:
            fullpath = BASE_ROOT_PATH + path
            print(fullpath)
            file_folder_list = os.listdir(fullpath)
            response['result'] = file_folder_list
        except FileNotFoundError:
            print("Wrong path")
            response['error'] = "Wrong path"

    elif query == "download":
        response['error'] = "Not implement!"
        pass

    elif query == "mkdir":
        response['error'] = "Not implement!"
        pass

    elif query == "rmdir":
        response['error'] = "Not implement!"
        pass

    json_string = json.dumps(response, indent=4)
    bytes = json_string.encode('ascii')
    print(bytes)
    return [bytes]


if __name__ == "__main__":
    print("Starting wsgiref server")
    with make_server('', 8000, file_server) as httpd:
        print("Serving on port 8000...")

        httpd.serve_forever()
