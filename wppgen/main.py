from .image_factory import FileIF, ColorIF, ImageFactory
from .decider import get_index
from .config import Config, FileConfig
from .filter import Filter

img_types = {
    "color": ColorIF,
    "file": FileIF
    }

class WallpaperGenerator:

    def __init__(self, config: Config, get_index):
        layers = config.get_key("layers")
        self._city = config.get_key("city")
        self._get_index = get_index
        self._layers = []

        for layer in layers:
            layer_config = config.get_key(layer)
            self._layers.append(WallpaperLayer(layer_config, self._city, self._get_index))

    def generate_wallpaper(self, output_path: str):
        image = self._layers[0].get_layer_final()
        for layer in self._layers[1:]:
            new_layer = layer.get_layer_final()
            image.paste(new_layer, get_image_placement(image, new_layer), mask=new_layer)

        image.save(output_path)

def get_image_placement(bottom, top):
    def calculate(bot, top):
        return (bot-top)//2

    return calculate(bottom.width, top.width), calculate(bottom.height, top.height)


class WallpaperLayer(object):

    """Docstring for WallpaperPart. """

    def __init__(self, config: dict, city: str, get_index):
        """TODO: to be defined.

        :config: TODO
        :city: str
        :img_type: TODO

        """
        self._config = config
        self._city = city
        self._get_index = get_index

    def generate_factories(self):
        factories = []
        for fac_type in self._config["images"].keys():
            for fac in self._config["images"][fac_type]:
                factory = img_types[fac_type](fac)
                factories.append(factory)

        return factories

    def get_factory(self) -> ImageFactory:
        factories = self.generate_factories()
        return factories[self._get_index(len(factories))]

    def get_layer_final(self):
        factory = self.get_factory()
        filter = Filter(self._city, **self._config["filter_values"])
        image = factory.get_enhanced_image(filter.compute_filter_value())
        return image
        
def get_wallpaper(config_path, output_path):
    config = FileConfig(config_path)
    WallpaperGenerator(config, get_index).generate_wallpaper(output_path)
        

