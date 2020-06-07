import json
import datetime
from random import shuffle

# パイプラインアーキテクチャ
from WeatherSystem.predict_da.predict_da import PredictDA
from WeatherSystem.date import PREFECTURE, DATE, DATE_WORDS
from WeatherSystem.tell_weather import TellWeather


# 発話データへのパス
UTTS_DATA = "WeatherSystem\\utts.json"

# 学習モデルへのパス
DA_MODEL = "WeatherSystem\\predict_da\\"
CONCEPT_MODEL = "WeatherSystem\\predict_concept\\"


class WeatherSystem(object):
    """天候情報案内対話システムの基幹クラス"""

    cogs = None

    def __init__(self, token):
        self.predic_da = PredictDA()
        self.tell_weather = TellWeather(token)
        self.utts = self.__load_json(UTTS_DATA)
        self.__init_frame()
        self.now_day = datetime.datetime.now().day

    def __load_json(self, path):
        with open(path, "r", encoding="UTF-8") as f:
            json_ = json.load(f)
        return json_

    def __init_frame(self):
        """フレームを初期状態にする"""
        self.frame = {"place": "", "placeId": "", "date": ""}

    def __is_init_frame(self):
        """フレームが初期状態か"""
        if (
            self.frame["place"] == ""
            and self.frame["placeId"] == ""
            and self.frame["date"] == ""
        ):
            return True
        else:
            return False

    def __get_utt(self, sys_da):
        """システム対話行為タイプから発話を返す"""
        utts = self.utts[sys_da]
        shuffle(utts)
        return utts[0]

    def __get_tell_utt_temp(self, main, temp):
        """天候と温度から発話を返す"""
        utts = self.utts["tell-info"]

        # 天候から発話を取得
        if main in ["Clear", "Rain"]:
            utts = utts[main]
        else:
            utts = utts["Other"]

        # 気温から生成する発話を分岐
        if temp < 14:
            # 寒い
            utts = utts["cold"]
        elif temp < 22:
            # 肌寒い
            utts = utts["chilly"]
        elif temp < 27:
            # 過ごしやすい
            utts = utts["good"]
        elif temp < 37:
            # 暑い
            utts = utts["hot"]
        else:
            # ファッキンホット
            utts = utts["fuckin’hot"]

        shuffle(utts)
        return utts[0]

    def __get_tell_utt(self):
        """天候情報案内の発話を返す"""
        sys_utt = ""

        placeID = self.frame["placeId"]
        day = self.frame["date"]
        weather = self.tell_weather.get_weather(placeID, day)

        main = weather.weather
        main_jp = weather.weather_jp
        temp = weather.temp

        sys_utt = "{}の天気は{}ね！気温は{}度みたい。".format(self.frame["place"], main_jp, temp)
        sys_utt += "\n" + self.__get_tell_utt_temp(main, temp)

        return sys_utt

    def __extract_place(self, text):
        """テキストから場所を抽出する"""
        for place in PREFECTURE.keys():
            if place in text:
                return place, PREFECTURE[place]
        return "", ""

    def __extract_date(self, text):
        """テキストから日にちを抽出する"""
        # 日にちを表す語彙から抽出する
        for date in DATE_WORDS.keys():
            if date in text:
                return DATE_WORDS[date]

        # 日付から抽出する
        days = [int(day.replace("日", "")) for day in DATE if day in text]
        if len(days) <= 0:
            return ""
        else:
            day = int(days[-1])

        # 今日から何日後
        diff_day = day - self.now_day
        if diff_day < 0:
            return "ValueError"
        elif diff_day > 4:
            return "ValueError"
        else:
            return diff_day

    def __update_frame(self, text):
        """フレームを更新する"""
        # 地域名を抽出
        if self.frame["place"] == "":
            place, placeID = self.__extract_place(text)
            self.frame["place"] = place
            self.frame["placeId"] = placeID

        # 日付を抽出
        if self.frame["date"] == "":
            self.frame["date"] = self.__extract_date(text)

    def __update_sys_da(self, user_da):
        """フレームからシステムの対話行為タイプを返す"""
        if user_da == "request-weather":
            if self.__is_init_frame():
                return "none"
            if self.frame["date"] == "ValueError":
                return "ask-redate"
            elif self.frame["placeId"] == "":
                return "ask-place"
            elif self.frame["date"] == "":
                return "ask-date"
            else:
                return "tell-info"
        elif user_da == "initialize":
            return "none"
        elif user_da == "correct-info":
            # TODO: フレーム情報を訂正する
            return "none"
        else:
            return "none"

    def reply(self, text):
        # ユーザーの対話行為タイプを取得
        user_da = self.predic_da.predict_da(text)
        print("user_da", user_da)

        # フレームの更新
        self.__update_frame(text)
        print("frame", self.frame)

        # システムの対話行為タイプを決定
        sys_da = self.__update_sys_da(user_da)
        print("sys_da", sys_da)

        if sys_da == "none":
            return None
        elif sys_da == "ask-redate":
            self.frame["date"] = ""
            return self.__get_utt(sys_da)
        elif sys_da.startswith("ask-"):
            return self.__get_utt(sys_da)
        elif sys_da == "tell-info":
            utt = self.__get_tell_utt()
            self.__init_frame()
            return utt

        return None
