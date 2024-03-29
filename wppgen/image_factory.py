from abc import ABC, abstractmethod
from typing import Optional

from PIL import Image
from yearly_hue import get_hue

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
        return get_hue(self._color)

    def __init__(self, color_value: float):
        """

        :path: TODO

        """
        ImageFactory.__init__(self)

        self._color = color_value
        self._size = size

    def get_image(self):
        return Image.new("RGB", self._size, self.color)


if __name__ == '__main__':
    print(HueIF(1).color)
