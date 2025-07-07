from requests import Response, post;
from typing import Callable, Any, Literal;
from datetime import datetime;
from functools import wraps
import os, json;

BASE_API_URL: str = "https://fluffycookies.space/api"
API_KEY: str = 'get the api key and insert it here';

def _timer(func: Callable) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: datetime = datetime.now();
        result: Any = func(*args, **kwargs);
        end_time: datetime = datetime.now();

        print(f'[+] Upload Time Taken: {end_time - start_time}');
        return result;

    return wrapper;

def _read_file(path: str, is_bytes: bool = True) -> bytes | str | None:
    mode: Literal['rb', 'r'] = 'rb' if is_bytes else 'r'
    encoding: Literal['utf-8'] | None = None if is_bytes else 'utf-8'
    
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, mode, encoding=encoding) as f:
            return f.read()

    except FileNotFoundError:
        print(f"[!] File not found: {path}")

    except Exception as e:
        print(f"[!] Unknown error reading {path}: {e}")

    return None

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
                'Authorization': API_KEY,              # required
                'Content-Type': 'application/json'
            },

            json = {
                'cookie': Cookie                      # required
            }
        )

        if response and response.json().get('message') == 'Cookie successfully setted':
            return True;

        return False;

    except Exception as e:
        print(f'[!] Failed to Connect, Error {e}')
        return False

def _unblacklist(API_KEY: str, file_name: str) -> Response | None:
    file_string: str | bytes | None = _read_file(path=os.path.join(os.getcwd(), "WareX", "API", "src", "game-files", file_name), is_bytes=False)
    
    response: Response = post(
        url = f'{BASE_API_URL}/v1/unblacklist',

        headers = {
            'Authorization': API_KEY,    # reqired
            'Content-Type': 'application/json'
        },

        json = {
            'file-type': '.rbxlx',      # required
            'file-name': file_name,     # optional
            'file': file_string         # required
        }
    )

    return response;

@_timer
def upload_new_game(API_KEY: str, Server_Size: int, File_Name: str, Username: str, game_name: str = 'random') ->  Response | None:
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
            save_string_to_rbxlx_file(file, 'example-file-name') # file name

            return True;

    return False

def cookie_is_valid() -> Any | None:
    cookies: bytes | str | None = _read_file(path = os.path.join(os.getcwd(), "cookies.json"), is_bytes=False)

    json_data: dict = json.loads(json.dumps(cookies))
    
    response = post(
        url = f'{BASE_API_URL}/v1/cookie-is-valid',
        headers = {
            'Authorization': API_KEY,
            'Content-Type': 'application/json'
        },
        json = {
            'cookies': json_data
        }
    )

    if response and response.json():
        response_json_data = response.json();
        status = response_json_data.get('status') # bool
        valid_cookies = response_json_data.get('valid-cookies')

        return valid_cookies;

    return None;

print(cookie_is_valid())

# print(unblacklist_file('nefors.rbxlx'))

"""response: Response | None = upload_new_game(
    API_KEY = API_KEY, 
    Server_Size = 60,   
    File_Name = "test.rbxlx", 
    Username = "vcd_", 
    game_name = 'v.c.d._'
)

print(response.text)
print(response.status_code)

if response and response.status_code == 200 and response.json():
    print(f'json body: {response.json()}')"""
