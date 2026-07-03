from servicios.session_context import SessionContext
from servicios.usb_block_service import USBBlockService
from servicios.notification_service import NotificationService
from servicios.event_service import EventService


class PolicyService:

    @staticmethod
    def validar_usb(device):

        permisos = SessionContext.permissions()

        if permisos is None:

            NotificationService.error(
                "No existe una política de seguridad."
            )

            USBBlockService.bloquear(device)

            return

        if not permisos.get("usoUSB", False):

            NotificationService.error(
                "El uso de dispositivos USB no está permitido para este usuario."
            )

            USBBlockService.bloquear(device)

            return

        EventService.usb_connected(device)