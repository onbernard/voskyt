from vosk import Model

available_languages = [
    {'lang': 'en-us', 'label': 'english', 'value':0},
    {'lang': 'small-cn', 'label': 'chinese', 'value':1},
    {'lang': 'ru', 'label': 'russian', 'value':2},
    {'lang': 'fr', 'label': 'french', 'value':3},
    {'lang': 'de', 'label': 'german', 'value':4},
    {'lang': 'es', 'label': 'spanish', 'value':5},
    {'lang': 'pt', 'label': 'portugese', 'value':6},
    {'lang': 'tr', 'label': 'turkish', 'value':7},
    {'lang': 'vn', 'label': 'vietnamese', 'value':8},
    {'lang': 'it', 'label': 'italian', 'value':9},
    {'lang': 'nl', 'label': 'dutch', 'value':10},
    {'lang': 'ca', 'label': 'catalan', 'value':11},
    {'lang': 'fa', 'label': 'farsi', 'value':12},
    {'lang': 'kz', 'label': 'kazakh', 'value':13},
    {'lang': 'sv', 'label': 'swedish', 'value':14},
    {'lang': 'ja', 'label': 'japanese', 'value':15},
    {'lang': 'eo', 'label': 'esperanto', 'value':16},
    {'lang': 'hi', 'label': 'hindi', 'value':17},
    {'lang': 'cs', 'label': 'czech', 'value':18},
    {'lang': 'pl', 'label': 'polish', 'value':19},
]


def initialize_vosk():
    for av in available_languages:
        model = Model(lang=av['lang'])