from wsgiref.simple_server import make_server
import json
import os

BASE_ROOT_PATH = "./temp_file_folder"

def file_server(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    html1 = [b"""
<!DOCTYPE html>
<html>
<head>
    <title>File Server</title>
    <style>
        th, td, p, input {
            font:14px Verdana;
        }
        table, th, td
        {
            border: solid 1px #DDD;
            border-collapse: collapse;
            padding: 2px 3px;
            text-align: center;
        }
        th {
            font-weight:bold;
        }
    </style>
</head>
<body>
    <p id="showData"></p>
</body>

<script>
    function httpGet(theUrl)
    {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }

    function rootPath()
    {
        jsonString = httpGet("/?ls");
        json = JSON.parse(jsonString);
        createExplorerFromJSON(json);
    }

    function createExplorerFromJSON(json)
    {
        var table = document.createElement("table");

        for (var key in json) {
            switch (key) {
                case 'path':
                    console.log(key + ':' + json[key]);
                    // TODO: to header
                    break;
                case 'query':
                    console.log(key + ':' + json[key]);
                    // TODO: not show
                    break;
                case 'error':
                    console.log(key + ':' + json[key]);
                    break;
                case 'result':
                    console.log(key + ':' + json[key]);

                    break;
                default:
                    console.log(key + ':' + json[key]);
                    break;
            }
        }

        var rows = [];
        for (var key in json) {
            if (rows.indexOf(key) === -1) {
                rows.push(key);
            }
        }

        for (var i = 0; i < rows.length; i++) {
            var tr = table.insertRow(-1);
            var th = document.createElement("th");
            th.innerHTML = rows[i];
            tr.appendChild(th);
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = json[rows[i]];
        }

        var divContainer = document.getElementById("showData");
        divContainer.innerHTML = "";
        divContainer.appendChild(table);

        var dirNameTextField = document.createElement("input");
        dirNameTextField.setAttribute('type', 'text');
        dirNameTextField.setAttribute('id', 'dirNameTextField');
        divContainer.appendChild(dirNameTextField)

        var mkdirButton = document.createElement("input");
        mkdirButton.setAttribute('type', 'button');
        mkdirButton.setAttribute('value', 'Make New Dir');
        var createDirHandler = function() {
            return function() {
                var dirName = document.getElementById('dirNameTextField').value;
                httpGet(dirName + "?mkdir");
                rootPath();
            };
        };
        mkdirButton.onclick = createDirHandler();
        divContainer.appendChild(mkdirButton);
    }

    rootPath();
</script>

</html>
"""]

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
        if path == "/":
            return html1
        else:
            response['error'] = "Not Correct Query"

    json_string = json.dumps(response, indent=4)
    bytes = json_string.encode('ascii')
    return [bytes]


if __name__ == "__main__":
    print("Starting wsgiref server")
    with make_server('', 8000, file_server) as httpd:
        print("Serving on port 8000...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stop serving")
        except Exception as e:
            print(str(e))
