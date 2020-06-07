import requests
import datetime


# エンドポイント
# 5 day / 3 hour forecast data
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"


# main対応表
MAIN = {
    "Thunderstorm": "雷雨",
    "Drizzle": "霧雨",
    "Rain": "雨",
    "Snow": "雪",
    "Mist": "靄",
    "Smoke": "煙",
    "Haze": "煙霧",
    "Clear": "快晴",
    "Clouds": "曇り",
}


class WeatherData(object):
    """
    リクエストした気象情報のデータ構造
    """

    def __init__(self, element):
        dt_txt = element["dt_txt"]
        dt_format = "%Y-%m-%d %H:%M:%S"

        self.dt = datetime.datetime.strptime(dt_txt, dt_format)
        self.temp = element["main"]["temp"]
        self.icon = element["weather"][0]["icon"]
        self.weather = element["weather"][0]["main"]
        try:
            self.weather_jp = MAIN[self.weather]
        except KeyError:
            self.weather_jp = None


class TellWeather(object):
    """
    天候情報を取得し、それを元に適切な応答を返す
    """

    def __init__(self, token_key):
        self.token_key = token_key

    def request_json(self, placeId):
        """天候情報をリクエスト"""
        params = {"id": placeId, "units": "metric", "appid": self.token_key}
        req = requests.get(BASE_URL, params=params)
        return req.json()

    def call_3hour_forecast(self, placeId):
        """5日間の予報を返す"""
        observation = self.request_json(placeId)
        weather_datas = [WeatherData(element) for element in observation["list"]]
        return weather_datas

    def get_morning_weather(self, placeId):
        """朝4時～6時の天候だけを返す"""
        forecasts = self.call_3hour_forecast(placeId)
        morning = []

        for data in forecasts:
            if data.dt.hour in [4, 5, 6]:
                morning.append(data)
        return morning

    def get_weather(self, placeId, day):
        """指定した日にちから気象情報と発話を返す"""
        day = int(day)
        if day < 0:
            raise ValueError("dayの指定が間違い")
            return None
        elif day > 5:
            raise ValueError("dayの指定が間違い。5日間の天気予報しか出来ない")
            return None

        forecast = self.get_morning_weather(placeId)[day - 1]
        print(forecast.dt)
        print(forecast.weather)
        print(forecast.weather_jp)
        return forecast
