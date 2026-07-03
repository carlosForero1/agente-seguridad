import time

from servicios.auth_client import AuthClient
from servicios.session_context import SessionContext


class PermissionSyncService:

    @staticmethod
    def start():

        auth = AuthClient()

        while True:

            try:

                usuario = SessionContext.user["usuario"]

                password = "prueba"   # temporal

                nueva = auth.login(usuario, password)

                if nueva:

                    SessionContext.set_session(nueva)


            except Exception as e:

                print(e)

            time.sleep(2)