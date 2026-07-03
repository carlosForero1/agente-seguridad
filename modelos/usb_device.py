from dataclasses import dataclass


@dataclass
class USBDevice:

    nombre: str
    fabricante: str
    serial: str
    letra: str
    disk_index: int
    device_id: str
    hora: str