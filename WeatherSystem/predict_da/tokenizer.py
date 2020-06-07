import MeCab
import neologdn
import unicodedata


user_dic = ""
tagger = MeCab.Tagger()


def _preprocess(text):
    text = text.strip()
    text = unicodedata.normalize("NFKC", text)
    text = neologdn.normalize(text)

    return text


def tokenizer(
    text, preprocess=None, remove_pos=None, stop_words=None, is_entry_word=False
):
    """
    テキストの分かち書き関数

    preprocess(text)
    テキストの前処理関数
    無指定ならutils.pyの_preprocessを施す
    
    remove_pos
    除外する品詞のリスト
    例：["助詞" "助動詞"]

    stop_words
    ストップワードのリスト
    例：["て", "に", "を", "は", "です", "ます"]
    """
    if preprocess is None:
        text = _preprocess(text)
    else:
        text = preprocess(text)

    words = []
    node = tagger.parseToNode(text)
    while node:
        surface = node.surface
        features = node.feature.split(",")

        # 文頭文末ならスキップ
        if features[0] in ["BOS", "EOS", "BOS/EOS"]:
            node = node.next
            continue

        # 除去品詞リストがある
        if remove_pos:
            if features[0] in remove_pos:
                node = node.next
                continue

        # ストップワードの指定がある
        if stop_words:
            if features[6] == stop_words:
                node = node.next
                continue

        # 原形か、表層形か
        if is_entry_word:
            words.append(features[6])
        else:
            words.append(surface)
        node = node.next

    return words
