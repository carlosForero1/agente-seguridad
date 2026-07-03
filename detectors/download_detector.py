import os
import time
from pathlib import Path

from servicios.report_service import ReportService
from servicios.session_context import SessionContext


class DownloadDetector:

    def __init__(self):

        self.downloads = Path.home() / "Downloads"

        self.archivos = set()

    def start(self):

        print("Monitoreando carpeta Descargas...")

    # Ignorar todo lo que ya existe
        self.archivos = set(os.listdir(self.downloads))

        while True:

            actuales = set(os.listdir(self.downloads))

            nuevos = actuales - self.archivos

            for archivo in nuevos:
                self.procesar_archivo(archivo)

            self.archivos = actuales

            time.sleep(2)

    def procesar_archivo(self, archivo):

        ruta = self.downloads / archivo

        if not ruta.is_file():
            return

        usuario = SessionContext.user

        ReportService.crear(

            tipo="DESCARGA",

            descripcion=f"Se descargó el archivo {archivo}",

            nivel="MEDIO",

            recomendacion="Verificar si el archivo proviene de una fuente confiable.",

            pasos="""
                1. Revisar origen.
                2. Escanear con antivirus.
                3. Validar firma digital.
                """,

            acciones=f"""
                Usuario: {usuario['usuario']}
                Archivo: {archivo}
                Ruta: {ruta}
                """
        )

        print(f"Descarga detectada -> {archivo}")