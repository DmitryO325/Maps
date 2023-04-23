import sys
import requests

from io import BytesIO

from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


def get_image(longitude_input, latitude_input, scale_input):
    longitude_input, latitude_input, scale_input = map(str, (longitude_input, latitude_input, scale_input))

    api_server = 'http://static-maps.yandex.ru/1.x'

    params = {
        'll': ','.join((longitude_input, latitude_input)),
        'spn': ','.join((scale_input, scale_input)),
        'l': 'map'
    }

    response = requests.get(api_server, params=params)

    image = Image.open(BytesIO(response.content))
    image.save('map.png')


class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Maps.ui', self)

        self.add_image()

    def add_image(self):
        get_image(longitude, latitude, scale)
        pixmap = QPixmap('map.png')
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    longitude = 38.910410
    latitude = 45.036114
    scale = 0.0005

    application = QApplication(sys.argv)
    window = Maps()
    window.show()
    sys.exit(application.exec())
