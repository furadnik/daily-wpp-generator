from abc import ABC, abstractmethod
from typing import Protocol
from PIL import Image, ImageEnhance

size = (1920, 1080)

class ImageFactory(ABC):

    @abstractmethod
    def get_image(self):
        pass

    def get_enhanced_image(self, brightness_factor: float):
        return ImageEnhance.Brightness(self.get_image()).enhance(brightness_factor)


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

    def __init__(self, color_hex: str):
        """

        :path: TODO

        """
        ImageFactory.__init__(self)

        self._color = color_hex
        self._size = size
    
    def get_image(self):
        return Image.new("RGB", self._size, self._color)

