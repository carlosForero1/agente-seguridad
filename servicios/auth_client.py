import requests


class AuthClient:

    def login(self, usuario, contrasena):

        url = "http://localhost:8080/autenticacion/login/agente"

        payload = {
            "usuario": usuario,
            "contrasena": contrasena
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print("Login fallido")
            return None