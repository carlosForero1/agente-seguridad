import requests
from datetime import datetime

from servicios.session_context import SessionContext


class ReportService:

    URL = "http://localhost:8080/reportes/crear"

    @staticmethod
    def crear(
            tipo,
            descripcion,
            nivel,
            recomendacion,
            pasos,
            acciones):

        try:

            body = {

                "tipo": tipo,

                "descripcion": descripcion,

                "tiempoCrea": datetime.now().isoformat(),

                "recomendacionAgente": recomendacion,

                "pasosAgente": pasos,

                "accionesPreAgente": acciones,

                "usuario": SessionContext.user["usuario"],

                "activo": True,

                "solucionado": False,

                "nivelPeligro": nivel

            }

            token = SessionContext.user["token"]

            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = requests.post(
                ReportService.URL,
                json=body,
                headers=headers
            )

            if response.status_code == 201:

                print("✅ Reporte enviado")

            else:

                print("❌ Error enviando reporte")
                print(response.status_code)
                print(response.text)

        except Exception as e:

            print("Error creando reporte")
            print(e)