import sys
import unicodedata

FILTER_NORMAL_AND_FIRST_FIELD_SET = set([
    ('は', '助詞'),
    ('の', '助詞'),
    ('て', '助詞'),
    ('に', '助詞'),
    ('を', '助詞'),
    ('が', '助詞'),
    ('た', '助動詞'),
    ('だ', '助動詞'),
    ('と', '助詞'),
    ('も', '助詞'),
    ('で', '助詞'),
    ('か', '助詞'),
    ('です', '助動詞'),
    ('な', '助詞'),
    ('よ', '助詞'),
    ('ない', '助動詞'),
    ('ね', '助詞'),
    ('から', '助詞'),
    ('れる', '助動詞'),
    ('ば', '助詞'),
    ('って', '助詞'),
    ('ます', '助動詞'),
    ('けれど', '助詞'),
    ('まで', '助詞'),
    ('ず', '助動詞'),
    ('わ', '助詞'),
    ('へ', '助詞'),
    ('し', '助詞'),
    ('ぞ', '助詞'),
    ('てる', '助動詞'),
    ('られる', '助動詞'),
    ('とく', '助動詞'),
    ('け', '助詞'),
    ('ふっ', '副詞'),
    ('ユー', '名詞'),
    ('はあはあ', '副詞'),
    ('させる', '助動詞'),
    ('〞', '名詞'),
    ('ンンッ', '名詞'),
    ('わっ', '副詞'),

    # 感動詞
    ('あっ', '感動詞'),
    ('ああ', '感動詞'),
    ('えっ', '感動詞'),
    ('んっ', '感動詞'),
    ('はあ', '感動詞'),
    ('うう', '感動詞'),
    ('あー', '感動詞'),
    ('おお', '感動詞'),
    ('おっ', '感動詞'),
    ('なあ', '感動詞'),
    ('うわ', '感動詞'),
    ('えー', '感動詞'),
    ('あれ', '感動詞'),
    ('はっ', '感動詞'),
    ('うー', '感動詞'),
    ('えーと', '感動詞'),
    ('へえ', '感動詞'),
    ('ふふ', '感動詞'),
    ('くっ', '感動詞'),
    ('ねえ', '感動詞'),
    ('わあ', '感動詞'),
    ('あはは', '感動詞'),
    ('あの', '感動詞'),
    ('む', '感動詞'),
    ('ふん', '感動詞'),
    ('いや', '感動詞'),
    ('いー', '感動詞'),
    ('ふう', '感動詞'),
    ('ふふふ', '感動詞'),
    ('きゃあ', '感動詞'),
    ('おー', '感動詞'),
    ('うお', '感動詞'),
    ('ははは', '感動詞'),
    ('ぎゃあ', '感動詞'),
    ('やあ', '感動詞'),
    ('うふふ', '感動詞'),
    ('んー', '感動詞'),
    ('ほう', '感動詞'),
    ('おっと', '感動詞'),
    ('えい', '感動詞'),
])

KANA_KANJI_TABLE = dict.fromkeys(i for i in range(sys.maxunicode) if not any((s in unicodedata.name(chr(i), '') for s in ['KATAKANA', 'HIRAGANA', 'CJK'])))
def extract_kana_kanji(text):
    return text.translate(KANA_KANJI_TABLE)

def include_for_refold(analysis):
    (orig, fields_str, normal) = analysis

    if not extract_kana_kanji(orig):
        return False # no Japanese characters

    if fields_str.startswith('名詞,固有名詞,'):
        return False # name

    fields = fields_str.split(',')
    if (normal, fields[0]) in FILTER_NORMAL_AND_FIRST_FIELD_SET:
        return False

    return True