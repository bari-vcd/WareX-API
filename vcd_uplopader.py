from requests import Response, post;
from typing import Callable, Any;
from datetime import datetime;
from functools import wraps
import os;

BASE_API_URL: str = f"https://fluffycookies.space/api"
API_KEY: str = 'your api key))'; #

def _timer(func: Callable) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: datetime = datetime.now();
        result: Any = func(*args, **kwargs);
        end_time: datetime = datetime.now();

        print(f'[+] Upload Time Taken: {end_time - start_time}');
        return result;

    return wrapper;

def rbxlx_file_to_string(file_path: str) -> str:
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            string: str = file.read()
            return string or 'Couldnt read the file';

    return 'The file was not found or was not passed as an argument.'

def save_string_to_rbxlx_file(_string: str, file_name: str) -> bool | None:
    try:
        if _string:
            with open(f'{file_name}.rbxlx', 'w') as file:
                file.write(str(_string))
                return True;

        return False;
    except Exception as e:
        print(f"[!] Failed to save file: {e}")
        return False

def _set_cookie(API_KEY: str, Cookie: str) -> bool:
    try:
        response: Response = post(
            url = f'{BASE_API_URL}/v1/vcd-uploader/set-cookie',

            headers = {
                'Authorization': API_KEY,  # required
                'Content-Type': 'application/json'
            },

            json = {
                'cookie': Cookie # required
            }
        )

        if response and response.json().get('message') == 'Cookie successfully setted':
            return True;

        return False;

    except Exception as e:
        print(f'[!] Failed to Connect, Error {e}')
        return False

def _unblacklist(API_KEY: str, file_name: str) -> Response | None:
    file_string: str | None = rbxlx_file_to_string(os.path.join(os.getcwd(), "API", "src", "game-files", file_name))
    
    response: Response = post(
        url = f'{BASE_API_URL}/v1/unblacklist',

        headers = {
            'Authorization': API_KEY, # reqired
            'Content-Type': 'application/json'
        },

        json = {
            'file-type': '.rbxlx',   # required
            'file-name': file_name,  # optional
            'file': file_string      # required
        }
    )

    return response;

@_timer
def upload_new_game(API_KEY: str, Server_Size: int, File_Name: str = 'test.rbxlx', Username: str = 'vcd_', game_name: str = 'meow') ->  Response | None:
    try:
        response: Response = post(
            url = f'{BASE_API_URL}/v1/vcd-uploader/create',
            
            headers = {
                'Authorization': API_KEY, 
                'Username': Username, 
                'Content-Type': 'application/json'
            },

            json = {
                'game-configuration' or 'game-config': {
                    'file': File_Name, 
                    'ServerPlayerCount' or 'ServerSize': Server_Size,
                    'game_name': game_name
                }
            }
        )

        return response

    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return None

def unblacklist_file(file_name: str) -> bool:
    response: Response | None = _unblacklist(API_KEY, file_name)

    if response:
        json_data: Any = response.json()
        message: str = json_data.get('message')
        
        if message == 'Success':
            file: str = json_data.get('file-string')
            save_string_to_rbxlx_file(file, 'example-file-name')

            return True;

    return False

response: Response | None = upload_new_game(
    API_KEY = API_KEY, 
    Server_Size = 60,   
    File_Name = "test.rbxlx", 
    Username = "vcd_", 
    game_name = 'v.c.d._'
)

if response and response.status_code == 200 and response.json():
    print(f'json body: {response.json()}')
