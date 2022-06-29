import json

class Config():

    """Gets a config"""

    def __init__(self, json_get):
        """

        :json_get: TODO

        """
        self._json_get = json_get

    def get_key(self, key):
        return self._json_get()[key]

class FileConfig(Config):

    """Gets a config from a file"""

    def __init__(self, file_path):
        """

        :file_path: path to the config json file.

        """
        Config.__init__(self, self._json_get_from_file)

        self._file_path = file_path

    def _json_get_from_file(self):
        with open(self._file_path) as f:
            return json.load(f)
        
