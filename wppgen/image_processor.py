from Pillow import Image, ImageFilter
from abc import ABC, abstractmethod

class ImageFactory(ABC):
    
    @abstractmethod
    def get_image(self):
        pass

class FileIF(ImageFactory):

    """Takes an image from a file"""

    def __init__(self, file_path: str):
        """

        :file_path: TODO

        """
        ImageFactory.__init__(self)

        self._file_path = file_path
        
    def get_image(self):
        return Image.open(self._file_path)
