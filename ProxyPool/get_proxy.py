import requests
PROXY_URL='http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_URL)
        if response.status_code == 200:
            print(response.text)
            return str(response.text)
    except ConnectionError:
        return None

if __name__ == '__main__':
    print(get_proxy())