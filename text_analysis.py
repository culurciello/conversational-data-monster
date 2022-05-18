# E. Culurciello, May 2022
# testing text parsing into semantics

import spacy
from spacy.matcher import Matcher                                                                                                                                                                                         


sentence = "plot country versus population!"
print('Your input:', sentence)

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

pattern = [{"LOWER": "plot"}, 
           {"POS": "NOUN"}, 
           {"LOWER": "versus"}, 
           {"POS": "NOUN"}]

matcher.add("command", [pattern])

doc = nlp(sentence)
matches = matcher(doc)

# match pattern:
print('Matching patterns:', pattern)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    print(match_id, string_id, start, end, span.text)