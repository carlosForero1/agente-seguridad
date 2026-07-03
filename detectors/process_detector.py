import time
import psutil

from servicios.session_context import SessionContext
from servicios.report_service import ReportService


class ProcessDetector:

    def __init__(self):

        self.detectados = set()

    def start(self):

        print("Monitoreando CMD y PowerShell...")

        while True:

            try:

                procesos_actuales = set()

                for proceso in psutil.process_iter(["pid", "name"]):

                    pid = proceso.info["pid"]
                    nombre = proceso.info["name"]

                    procesos_actuales.add(pid)

                    # Ya fue procesado
                    if pid in self.detectados:
                        continue

                    self.detectados.add(pid)

                    self.validar_proceso(proceso)

                self.detectados &= procesos_actuales

            except Exception:
                pass

            time.sleep(2)


    def validar_proceso(self, proceso):

        permisos = SessionContext.permissions()

        if permisos is None:
            return

        nombre = (proceso.info["name"] or "").lower()

        # CMD
        if nombre == "cmd.exe":

            if not permisos.get("usoCmd", False):

                self.crear_reporte(
                    "CMD",
                    "Uso no autorizado del símbolo del sistema.",
                    proceso
                )

        # PowerShell
        elif nombre in ("powershell.exe", "pwsh.exe"):

            if not permisos.get("powerShell", False):

                self.crear_reporte(
                    "POWERSHELL",
                    "Uso no autorizado de PowerShell.",
                    proceso
                )

        elif nombre == "code.exe":

            self.crear_reporte(
                "VISUAL STUDIO CODE",
                "Se abrió Visual Studio Code.",
                proceso
            )

        elif nombre == "devenv.exe":

            self.crear_reporte(
                "VISUAL STUDIO",
                "Se abrió Microsoft Visual Studio.",
                proceso
            )

    #########################################################

    def crear_reporte(self, tipo, descripcion, proceso):

        usuario = SessionContext.user

        try:
            comando = " ".join(proceso.cmdline())
        except Exception:
            comando = "No disponible"

        ReportService.crear(

            tipo=tipo,

            descripcion=descripcion,

            nivel="ALTO",

            recomendacion=f"Verificar por qué el usuario intentó ejecutar {tipo}.",

            pasos="""
1. Confirmar si el usuario tiene autorización.
2. Revisar el comando ejecutado.
3. Validar si existe actividad sospechosa.
4. Registrar el incidente.
""",

            acciones=f"""
Usuario : {usuario['usuario']}

Proceso : {proceso.info['name']}

Comando : {comando}
"""

        )

        print(f"[{tipo}] Detectado uso sin permisos.")