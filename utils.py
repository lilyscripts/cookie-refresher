import requests

def generate_csrf_token(cookie):
    csrf_request = requests.get("https://www.roblox.com/home",
        cookies = {
            ".ROBLOSECURITY": cookie
            }
        )
    
    if csrf_request.status_code != 200:
        return None
    
    csrf_token = csrf_request.text.split('data-token="')[1].split('"')[0]

    return csrf_token

def generate_auth_ticket(cookie, csrf_token):
    auth_request = requests.post("https://auth.roblox.com/v1/authentication-ticket", 
        cookies = {
            ".ROBLOSECURITY": cookie
        },
        headers = {
            "Content-Type": "application/json",
            "origin": "https://www.roblox.com",
            "referer": "https://www.roblox.com/my/account",
            "user-agent": "Roblox/WinInet",
            "x-csrf-token": csrf_token
        }
    )

    auth_ticket = auth_request.headers.get("rbx-authentication-ticket")

    return auth_ticket

def claim_auth_ticket(auth_ticket, csrf_token):
    refresh_request = requests.post("https://auth.roblox.com/v1/authentication-ticket/redeem", 
        json = {
            "authenticationTicket": auth_ticket
        },
        headers = {
            "Content-Type": "application/json",
            "origin": "https://www.roblox.com",
            "RBXAuthenticationNegotiation": "1",
            "referer": "https://www.roblox.com/my/account",
            "user-agent": "Roblox/WinInet",
            "x-csrf-token": csrf_token
        }
    )

    refresh_cookie = refresh_request.headers["set-cookie"].split(".ROBLOSECURITY=")[1].split(";")[0]
    
    return refresh_cookie
