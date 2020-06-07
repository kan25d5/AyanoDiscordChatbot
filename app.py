from config.config_list import ConfigData
from bot.ayano import Ayano

# 気象情報システム
from WeatherSystem.weather_system import WeatherSystem


config = ConfigData()
DIALOG_SYSTEMS = [WeatherSystem(config.weather_token)]


if __name__ == "__main__":
    ayano = Ayano(DIALOG_SYSTEMS, config.command_prefix)
    ayano.run(config.discord_token)
