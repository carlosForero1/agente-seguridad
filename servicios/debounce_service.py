import time


class DebounceService:

    ultimo_evento = {}

    @staticmethod
    def permitir(nombre, segundos=5):

        ahora = time.time()

        ultimo = DebounceService.ultimo_evento.get(nombre)

        if ultimo is None:

            DebounceService.ultimo_evento[nombre] = ahora

            return True

        if ahora - ultimo >= segundos:

            DebounceService.ultimo_evento[nombre] = ahora

            return True

        return False