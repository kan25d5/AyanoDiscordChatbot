import dill
from tokenizer import tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder


# 訓練データへのパス
TRAINING_DATA = "sample_da.dat"


class TrainingDA(object):
    def __init__(self, training_data_path=None):
        if training_data_path is None:
            self.training_data_path = TRAINING_DATA
        else:
            self.training_data_path = training_data_path

    def __load_sample(self):
        with open(self.training_data_path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        return lines

    def __get_wakati_label(self):
        label_list = []
        text_lines = []

        lines = self.__load_sample()
        for line in lines:
            line = line.rstrip()
            da, utt = line.split("\t")

            text_lines.append(utt)
            label_list.append(da)

        return text_lines, label_list

    def generate_model(self, save_path):
        # 訓練データから分かち書き文とラベルを取得
        text_lines, label_list = self.__get_wakati_label()

        # 各文を素性ベクトルへ変換
        vectorizer = TfidfVectorizer(analyzer=tokenizer)
        X = vectorizer.fit_transform(text_lines)

        # ラベルを数値に変換
        label_enc = LabelEncoder()
        Y = label_enc.fit_transform(label_list)

        # SVMでモデルを訓練
        svc = SVC(gamma="scale")
        svc.fit(X, Y)

        # モデルを保存
        with open(save_path, "wb") as f:
            dill.dump(tokenizer, f)
            dill.dump(vectorizer, f)
            dill.dump(label_enc, f)
            dill.dump(svc, f)


if __name__ == "__main__":
    model = TrainingDA()
    model.generate_model("predict_da.model")
