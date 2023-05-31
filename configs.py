LANGUAGES = {
    'ru': 'Русский',
    'en': 'Английский',
    'ar': 'Арабский',
    'fr': 'Французский',
    'zh-tw': 'Китайский',
    'uz': 'Узбекский'
}

def get_key(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k