import re, json
import importlib.resources as pkg_resources
from . import resources

# Basisersetzungen (Umlaute, ß)
REPLACEMENTS = {
    "ß": "ss",
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue"
}


def load_woerterbuch():
    with pkg_resources.open_text(resources, "word_mappings.json", encoding="utf-8") as file:
        return json.load(file)

# Lade die Wörter aus der JSON-Datei
woerter = load_woerterbuch()

# Veraltete Wörter und französische Lehnwörter
OLD_WORDS = woerter['old_words']
FRENCH_WORDS = woerter['french_words']

def convert_to_leist(text: str, *, erweitern: bool = True, franz_modus: bool = True) -> str:
    """
    Konvertiert modernen Text in altdeutsche Schreibweise, optional mit französischem Modus.
    
    :param text: Der Eingabetext.
    :param erweitern: Wendet zusätzliche alte Rechtschreibregeln an.
    :param franz_modus: Ersetzt moderne Begriffe durch französische Lehnwörter.
    :return: Der umgewandelte Text.
    """

    # Umlaute und ß ersetzen
    for original, replacement in REPLACEMENTS.items():
        text = text.replace(original, replacement)

    # Erweiterte Altdeutsche Regeln
    if erweitern:
        text = _anwenden_alte_rechtschreibung(text)

    # Französische Wörter
    if franz_modus:
        text = _ersetze_franzoesische_lehnwoerter(text)

    return text

def _anwenden_alte_rechtschreibung(text: str) -> str:
    for modern, alt in OLD_WORDS.items():
        pattern = re.compile(rf'\b{modern}\b', re.IGNORECASE)
        text = pattern.sub(lambda m: _case_preserve(m.group(), alt), text)

    return text

def _ersetze_franzoesische_lehnwoerter(text: str) -> str:
    for deutsch, franzoesisch in FRENCH_WORDS.items():
        pattern = re.compile(rf'\b{deutsch}\b', re.IGNORECASE)
        text = pattern.sub(lambda m: _case_preserve(m.group(), franzoesisch), text)

    return text

def _case_preserve(original: str, replacement: str) -> str:
    if original.isupper():
        return replacement.upper()
    elif original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    else:
        return replacement.lower()

text = "Die Dame fährt mit dem Auto zum Geschäft und telefoniert."
print(convert_to_leist(text))
