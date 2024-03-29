# AyanoDiscordChatbot
身内サーバーで運用している杉浦綾乃を冠したチャットbot。


## 現在対応している機能
- 天候情報案内
- 音楽再生(コマンドリクエストのみ)


## 必要環境
- Python 3（python3.6以降推奨）
- MeCab
- MeCab用IPA 辞書
- mecab-ipadic-neolog（推奨）


## セッティング
### APIトークンの設定
configファイルにある`config(template).yaml`を`config.yaml`にリネームし、各種APIのトークンキーを記述して下さい。このアプリが使用しているAPIは以下のとおりです。
- discord bot
- OpenWeatherMap（5 day weather forecast）


### 形態素解析ソフトMeCabの導入
<a href="https://taku910.github.io/mecab/">MeCab公式サイト</a>からMeCab本体とIPA 辞書をインストールして下さい。


### 必要ライブラリの導入
このアプリの実行に必要なライブラリをインストールする必要があります。必要なライブラリは`requirements.txt`に記述されています。

このアプリのルートディレクトリ（`app.py`のあるディレクトリ）で、以下を実行して下さい。
```
pip install -r requirements.txt
```


## 実行
必要なライブラリがインストールされているpythonインタープリタで以下を実行して下さい。
```
python app.py
```


## 対話例：
```
ヨシカン今日 09:07
@杉浦綾乃 明日の天気を教えて

杉浦綾乃
ボット
今日 09:07
@ヨシカン 何処の天候を知りたいのかしら？

ヨシカン今日 09:08
@杉浦綾乃 群馬県

杉浦綾乃
ボット
今日 09:08
@ヨシカン 群馬の天気は曇りね！気温は27.48度みたい。
暑いわね...涼しい格好で出かけなさいよ！

ヨシカン今日 09:08
@杉浦綾乃 明日の天気を教えて

杉浦綾乃
ボット
今日 09:08
@ヨシカン 何処の天候を知りたいの？

ヨシカン今日 09:08
@杉浦綾乃 新潟県

杉浦綾乃
ボット
今日 09:08
@ヨシカン 新潟の天気は曇りね！気温は22.17度みたい。
過ごしやすい日になるみたいね！
```