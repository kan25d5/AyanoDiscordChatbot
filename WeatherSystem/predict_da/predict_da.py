import sys, os
import dill
from WeatherSystem.predict_da.tokenizer import tokenizer


# パス追加
sys.path.append(os.getcwd() + "\\WeatherSystem\\predict_da\\")


class PredictDA(object):
    PATH = "WeatherSystem\\predict_da\\predict_da.model"

    def __init__(self):
        with open(self.PATH, "rb") as f:
            self.tokenizer = dill.load(f)
            self.vectorizer = dill.load(f)
            self.label_enc = dill.load(f)
            self.svc = dill.load(f)

    def predict_da(self, text):
        X = self.vectorizer.transform([text])
        Y = self.svc.predict(X)
        da = self.label_enc.inverse_transform(Y)[0]
        return da
