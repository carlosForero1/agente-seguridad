import threading
import time

from servicios.auth_client import AuthClient
from servicios.session_context import SessionContext

from detectors.usb_detector import USBDetector
from detectors.download_detector import DownloadDetector
from detectors.screenshot_detector import ScreenshotDetector


def login():

    auth = AuthClient()

    session = auth.login(
        "carlos",
        "prueba"
    )

    if session is None:

        print("No fue posible iniciar sesión.")

        return False

    SessionContext.set_session(session)

    print(f"""
====================================

AI SECURITY AGENT

Usuario: {session["usuario"]}

Perfil : {session["perfil"]["nombre"]}

Agente iniciado correctamente.

====================================
""")

    return True


def main():

    if not login():
        return

    usb = USBDetector()

    downloads = DownloadDetector()

    screenshots = ScreenshotDetector()

    # Detector USB
    threading.Thread(
        target=usb.start,
        daemon=True
    ).start()

    # Detector Descargas
    threading.Thread(
        target=downloads.start,
        daemon=True
    ).start()

    # Detector Capturas
    threading.Thread(
        target=screenshots.start,
        daemon=True
    ).start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()