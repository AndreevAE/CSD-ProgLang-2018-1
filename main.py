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

    fullpath = BASE_ROOT_PATH + path

    response = {'path': path, 'query': query}

    if not os.path.exists(BASE_ROOT_PATH):
        os.makedirs(BASE_ROOT_PATH)
    
    if query == "ls":
        try:
            file_folder_list = os.listdir(fullpath)
        except FileNotFoundError:
            response['error'] = "File Not Found"
        except Exception as e:
            response['error'] = str(e)
        else:
            response['result'] = file_folder_list

    elif query == "download":
        data = b''
        try:
            with open(fullpath, 'rb', buffering=0) as f:
                data = f.readall()
        except FileNotFoundError:
            response['error'] = "File Not Found"
        except Exception as e:
            response['error'] = str(e)
        else:
            return [data]

    elif query == "mkdir":
        try:
            os.mkdir(fullpath)
        except FileNotFoundError:
            response['error'] = "File Not Found"
        except Exception as e:
            response['error'] = str(e)
        else:
            response['result'] = "Success! Folder was created"

    elif query == "rmdir":
        try:
            os.rmdir(fullpath)
        except FileNotFoundError:
            response['error'] = "File Not Found"
        except Exception as e:
            response['error'] = str(e)
        else:
            response['result'] = "Success! Folder was removed"
    else:
        response['error'] = "Not Correct Query"

    json_string = json.dumps(response, indent=4)
    bytes = json_string.encode('ascii')
    return [bytes]


if __name__ == "__main__":
    print("Starting wsgiref server")
    with make_server('', 8000, file_server) as httpd:
        print("Serving on port 8000...")

        httpd.serve_forever()
