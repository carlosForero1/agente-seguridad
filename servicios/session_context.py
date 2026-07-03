class SessionContext:

    user = None
    token = None

    @staticmethod
    def set_session(data):
        SessionContext.user = data
        SessionContext.token = data.get("token")

    @staticmethod
    def is_logged():
        return SessionContext.user is not None

    @staticmethod
    def permissions():
        return SessionContext.user["perfil"]["permisosManejo"]