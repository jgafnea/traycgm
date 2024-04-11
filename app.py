import os
import time

import appindicator  # type: ignore
import gtk  # type: ignore
from pydexcom import Dexcom

ICON = os.path.abspath("./assets/icon.png")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def get_glucose():
    dexcom = Dexcom(USERNAME, PASSWORD)  # type: ignore
    reading = dexcom.get_current_glucose_reading()
    if reading:
        return f"{reading.value}{reading.trend_arrow}".strip()
    return "ERR"


class Indicator:
    def __init__(self):
        self.glucose = ""
        self.ind = appindicator.Indicator(
            "glucose-indicator", ICON, appindicator.CATEGORY_APPLICATION_STATUS
        )
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.update()
        self.ind.set_menu(self.setup_menu())

    def setup_menu(self):
        menu = gtk.Menu()
        refresh = gtk.MenuItem("Refresh Now")
        refresh.connect("activate", self.on_refresh)
        refresh.show()
        menu.append(refresh)
        return menu

    def update(self):
        INTERVAL = 300  # 5 minutes
        while True:
            try:
                old = self.glucose
                new = get_glucose()
                if new != old:
                    self.glucose = new
                    self.ind.set_label(new)
            except Exception as err:
                print(f"ERR: {err}")

            time.sleep(INTERVAL)

    def on_refresh(self):
        self.update()


if __name__ == "__main__":
    app = Indicator()
    gtk.main()
