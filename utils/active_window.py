import pygetwindow as gw


class ActiveWindow:

    @staticmethod
    def titulo():

        try:

            ventana = gw.getActiveWindow()

            if ventana:

                return ventana.title

        except:

            pass

        return "Desconocida"