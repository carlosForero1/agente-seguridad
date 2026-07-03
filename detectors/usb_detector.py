import time
from datetime import datetime

import pythoncom
import wmi

from modelos.usb_device import USBDevice

from servicios.report_service import ReportService
from servicios.session_context import SessionContext


class USBDetector:

    def __init__(self):

        self.previous_devices = set()
        self.wmi = None

    def get_devices(self):

        devices = []

        for disk in self.wmi.Win32_DiskDrive():

            if "USB" not in disk.InterfaceType:
                continue

            nombre = disk.Caption
            fabricante = disk.Manufacturer or "Desconocido"
            serial = getattr(disk, "SerialNumber", "No disponible")
            letra = "-"

            for partition in disk.associators(
                    "Win32_DiskDriveToDiskPartition"):

                for logical in partition.associators(
                        "Win32_LogicalDiskToPartition"):

                    letra = logical.DeviceID

            devices.append(

                USBDevice(

                    nombre=nombre,
                    fabricante=fabricante,
                    serial=str(serial),
                    letra=letra,
                    hora=datetime.now().strftime("%H:%M:%S"),
                    disk_index=disk.Index,
                    device_id=disk.DeviceID

                )

            )

        return devices

    def start(self):

        pythoncom.CoInitialize()

        try:

            self.wmi = wmi.WMI()

            print("Esperando dispositivos USB...\n")

            while True:

                try:

                    devices = self.get_devices()

                    current = {

                        device.serial

                        for device in devices

                    }

                    new_devices = current - self.previous_devices

                    for device in devices:

                        if device.serial not in new_devices:
                            continue

                        permisos = SessionContext.permissions()

                        # USB NO AUTORIZADA
                        if permisos is None or not permisos.get("usoUSB", False):

                            print("🚨 USB BLOQUEADA POR POLÍTICA")

                            ReportService.crear(

                                tipo="USB",

                                descripcion=f"Se detectó una memoria USB no autorizada ({device.nombre})",

                                nivel="ALTO",

                                recomendacion="Retirar inmediatamente el dispositivo USB.",

                                pasos="""
1. Verificar el propietario de la memoria.
2. Revisar su contenido.
3. Ejecutar un análisis antivirus.
4. Autorizar únicamente dispositivos registrados.
""",

                                acciones=f"""
Serial: {device.serial}
Letra: {device.letra}
Fabricante: {device.fabricante}
"""

                            )

                        else:

                            print(f"USB autorizada: {device.nombre}")

                    self.previous_devices = current

                except Exception as e:

                    print(f"[USBDetector] Error: {e}")

                time.sleep(1)

        finally:

            pythoncom.CoUninitialize()