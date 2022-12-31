from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
import colorsys

from PIL import Image

size = (3840, 2160)


def add_alpha(image: Image, alpha_factor: float):
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []
    for x in data:
        new_data.append((
            x[0],
            x[1],
            x[2],
            int(x[3] * alpha_factor)
        ))

    image.putdata(new_data)
    return image


class ImageFactory(ABC):

    @property
    def color(self) -> Optional[str]:
        return None

    @abstractmethod
    def get_image(self) -> Image:
        pass

    def get_enhanced_image(self, brightness_factor: float):
        image = self.get_image()
        return add_alpha(image, brightness_factor)
        # return ImageEnhance.Brightness(self.get_image()).enhance(brightness_factor)


class FileIF(ImageFactory):

    """Gets the image from a file"""

    def __init__(self, path: str):
        """

        :path: TODO

        """
        self._path = path

    def get_image(self):
        with Image.open(self._path) as f:
            f.load()
        return f


class ColorIF(ImageFactory):
    """Gets the image from a file"""

    @property
    def color(self) -> Optional[str]:
        return self._color

    def __init__(self, color_hex: str):
        """

        :path: TODO

        """
        ImageFactory.__init__(self)

        self._color = color_hex
        self._size = size

    def get_image(self):
        return Image.new("RGB", self._size, self._color)


class HueIF(ImageFactory):
    """Gets the image from a hue."""

    @property
    def color(self) -> Optional[str]:
        t = datetime.today()
        hue = (int(t.strftime("%j")) - 1 + (t.hour + (t.minute + t.second / 60) / 60) / 24) / 365
        print(hue)
        hue = (6 - hue + 0.6)
        while hue > 1:
            hue -= 1
        r, g, b = colorsys.hsv_to_rgb(hue, 1, self._color)
        return "#" + self.i_to_h(r) + self.i_to_h(g)  + self.i_to_h(b)

    def i_to_h(self, i: float) -> None:
        h = hex(int(i * 255))
        print(h)
        h = "00" + h[2:]
        return h[-2:]

    def __init__(self, color_value: float):
        """

        :path: TODO

        """
        ImageFactory.__init__(self)

        self._color = color_value
        self._size = size

    def get_image(self):
        return Image.new("RGB", self._size, self.color)


print(HueIF(.69).color)
