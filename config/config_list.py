import yaml


class ConfigData(object):
    def __init__(self):
        config = self.read_token()

        keys = config["api_key"]
        self.discord_token = keys["discord"]
        self.weather_token = keys["OpenWeatherMap"]

        self.command_prefix = config["command_prefix"]

    def read_token(self):
        with open("config/config.yaml", "r", encoding="UTF-8") as f:
            obj = yaml.safe_load(f)
        return obj
