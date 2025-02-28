import requests


def check_connection() -> bool:
    try:
        requests.get('https://discord.com', verify=False, timeout=10)
    except Exception:
        return False
    else:
        return True
