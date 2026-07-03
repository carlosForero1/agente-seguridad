import os
import threading
import time
from datetime import datetime
from pathlib import Path

import keyboard
import psutil
from PIL import ImageGrab

from servicios.debounce_service import DebounceService
from servicios.report_service import ReportService
from servicios.session_context import SessionContext
from utils.active_window import ActiveWindow


class ScreenshotDetector:

    PROGRAMAS_CAPTURA = {

        "SnippingTool.exe",
        "ScreenClippingHost.exe",
        "ShareX.exe",
        "Lightshot.exe",
        "Greenshot.exe",
        "ScreenRec.exe",
        "OBS.exe",
        "OBS64.exe"

    }

    def __init__(self):

        self.folder = Path.home() / "Pictures" / "Screenshots"

        self.start_time = datetime.now().timestamp()

        if self.folder.exists():
            self.archivos = set(os.listdir(self.folder))
        else:
            self.archivos = set()

        self.clipboard_detectado = False

        # Evita reportar el mismo proceso muchas veces
        self.procesos_detectados = set()

    #####################################################

    def start(self):

        print("Monitor de capturas iniciado.")

        threading.Thread(
            target=self.monitor_keyboard,
            daemon=True
        ).start()

        threading.Thread(
            target=self.monitor_processes,
            daemon=True
        ).start()

        threading.Thread(
            target=self.monitor_folder,
            daemon=True
        ).start()

        threading.Thread(
            target=self.monitor_clipboard,
            daemon=True
        ).start()

        while True:
            time.sleep(1)

    #####################################################

    def monitor_keyboard(self):

        keyboard.add_hotkey(
            "print screen",
            lambda: self.reportar("Print Screen")
        )

        keyboard.add_hotkey(
            "alt+print screen",
            lambda: self.reportar("Alt + Print Screen")
        )

        keyboard.add_hotkey(
            "windows+shift+s",
            lambda: self.reportar("Windows + Shift + S")
        )

        keyboard.wait()

    #####################################################

    def monitor_processes(self):

        while True:

            try:

                procesos_actuales = set()

                for proceso in psutil.process_iter(["pid", "name"]):

                    pid = proceso.info["pid"]
                    nombre = proceso.info["name"]

                    procesos_actuales.add(pid)

                    if nombre not in self.PROGRAMAS_CAPTURA:
                        continue

                    if pid in self.procesos_detectados:
                        continue

                    self.procesos_detectados.add(pid)

                    self.reportar(f"Proceso: {nombre}")

                # Eliminar procesos cerrados
                self.procesos_detectados &= procesos_actuales

            except Exception:
                pass

            time.sleep(2)

    #####################################################

    def monitor_folder(self):

        while True:

            try:

                if not self.folder.exists():
                    time.sleep(1)
                    continue

                actuales = set(os.listdir(self.folder))

                nuevos = actuales - self.archivos

                for archivo in nuevos:

                    ruta = self.folder / archivo

                    if not ruta.exists():
                        continue

                    creado = ruta.stat().st_ctime

                    # Ignorar capturas anteriores al inicio del agente
                    if creado < self.start_time:
                        continue

                    self.reportar(
                        f"Captura guardada: {archivo}"
                    )

                self.archivos = actuales

            except Exception as e:
                print(e)

            time.sleep(1)

    #####################################################

    def monitor_clipboard(self):

        while True:

            try:

                imagen = ImageGrab.grabclipboard()

                if imagen:

                    if not self.clipboard_detectado:

                        self.clipboard_detectado = True

                        self.reportar(
                            "Imagen copiada al portapapeles"
                        )

                else:

                    self.clipboard_detectado = False

            except Exception:
                pass

            time.sleep(1)

    #####################################################

    def reportar(self, origen):

        if not DebounceService.permitir(
                "SCREENSHOT",
                segundos=5):
            return

        usuario = SessionContext.user

        ventana = ActiveWindow.titulo()

        ReportService.crear(

            tipo="CAPTURA",

            descripcion=f"Se detectó una captura ({origen})",

            nivel="MEDIO",

            recomendacion="Validar si la captura contiene información sensible.",

            pasos="""
1. Identificar el motivo de la captura.
2. Revisar si contiene información confidencial.
3. Verificar que esté autorizada.
4. Registrar el incidente.
""",

            acciones=f"""
Usuario : {usuario['usuario']}

Origen : {origen}

Ventana : {ventana}
"""

        )

        print(f"[CAPTURA] {origen} | {ventana}")