import sys
import requests

from io import BytesIO

from PIL import Image
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


def get_image(longitude_input, latitude_input, scale_input,
              scale_level_input, width_input, height_input, map_type_input):
    longitude_input, latitude_input, scale_input, scale_level_input, width_input, height_input, map_type_input = \
        map(str, (longitude_input, latitude_input, scale_input,
                  scale_level_input, width_input, height_input, map_type_input))

    api_server = 'http://static-maps.yandex.ru/1.x'

    params = {
        'll': f'{longitude_input},{latitude_input}',
        'l': map_type_input,
        'z': scale_level_input,
        'size': f'{width_input},{height_input}'
    }

    response = requests.get(api_server, params=params)

    image = Image.open(BytesIO(response.content))
    image.save('../map.png')


class Maps(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Maps.ui', self)

        for button in self.map_type_buttons.buttons():
            button.clicked.connect(self.change_map_type)
            button.setFocusPolicy(QtCore.Qt.NoFocus)

        self.add_image()

    def change_map_type(self):
        global map_type

        if self.sender().text() == 'Схема':
            map_type = 'map'

        elif self.sender().text() == 'Спутник':
            map_type = 'sat'

        elif self.sender().text() == 'Гибрид':
            map_type = 'sat,skl'

        self.add_image()

    def keyPressEvent(self, event):
        global scale_level, longitude, latitude

        if event.key() == Qt.Key_PageUp and scale_level < 17:
            scale_level += 1

        if event.key() == Qt.Key_PageDown and scale_level > 0:
            scale_level -= 1

        if event.key() == Qt.Key_Right:
            longitude += dictionary_of_z_and_spn[scale_level] * 2
            longitude -= 360 if longitude > 180 else 0

        if event.key() == Qt.Key_Left:
            longitude -= dictionary_of_z_and_spn[scale_level] * 2
            longitude += 360 if longitude <= -180 else 0

        if event.key() == Qt.Key_Up:
            latitude += dictionary_of_z_and_spn[scale_level]
            latitude = 85 if latitude > 85 else latitude

        if event.key() == Qt.Key_Down:
            latitude -= dictionary_of_z_and_spn[scale_level]
            latitude = -85 if latitude < -85 else latitude

        self.add_image()

    def add_image(self):
        get_image(longitude, latitude, scale, scale_level, width, height, map_type)
        pixmap = QPixmap('../map.png')
        self.image.setPixmap(pixmap)


dictionary_of_z_and_spn = {value: 0.002 * 2 ** (17 - value) for value in range(18)}

if __name__ == '__main__':
    longitude = 38.910410
    latitude = 45.036114
    scale = 0.064
    scale_level = 12
    width = 650
    height = 450
    map_type = 'map'

    application = QApplication(sys.argv)
    window = Maps()
    window.show()
    sys.exit(application.exec())
