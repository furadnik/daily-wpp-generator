from typing import Optional

from .config import Config, FileConfig
from .decider import get_index
from .filter import Filter
from .image_factory import ColorIF, FileIF, ImageFactory

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
            layer_obj = WallpaperLayer(layer_config, self._city, self._get_index)
            self._layers.append(layer_obj)

    @property
    def color(self) -> Optional[str]:
        """Generate color from layers."""
        for layer in self._layers:
            if layer.color:
                return layer.color

        return None

    def generate_wallpaper(self, output_path: str):
        image = ColorIF("#000000").get_image()
        for layer in self._layers:
            new_layer = layer.get_layer_final()
            image.paste(new_layer, get_image_placement(image, new_layer), mask=new_layer)

        image.save(output_path)


def get_image_placement(bottom, top):
    def calculate(bot, top):
        return (bot - top) // 2

    return calculate(bottom.width, top.width), calculate(bottom.height, top.height)


class WallpaperLayer:

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
        self.color = None

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
        self.color = factory.color
        filter = Filter(self._city, **self._config["filter_values"])
        image = factory.get_enhanced_image(filter.compute_filter_value())
        return image


def get_wallpaper(config_path, output_path) -> Optional[str]:
    config = FileConfig(config_path)
    wg = WallpaperGenerator(config, get_index)
    wg.generate_wallpaper(output_path)
    return wg.color
