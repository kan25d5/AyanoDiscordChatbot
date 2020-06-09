from config.config_list import ConfigData
from bot.ayano import Ayano

# 気象情報システム
from WeatherSystem.weather_system import WeatherSystem

# 音楽再生システム
from MusicSystem.music_system import MusicSystem


# コンフィグデータのロード
config = ConfigData()
# 対話システムの保持
DIALOG_SYSTEMS = [WeatherSystem(config.weather_token), MusicSystem()]


if __name__ == "__main__":
    ayano = Ayano(DIALOG_SYSTEMS, config.command_prefix)
    ayano.run(config.discord_token)
