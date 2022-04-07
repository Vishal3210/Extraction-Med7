from flask import Flask, redirect, request
import spacy
import en_core_med7_lg

med7 = en_core_med7_lg.load()
options = {'ents': med7.pipe_labels['ner']}

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

@app.route('/<text>')
def extract(text):
    doc = med7(text)

    spacy.displacy.render(doc, style='ent', options=options)

    li = {"FORM": [""], "DRUG": [""], "STRENGTH": [""], "FREQUENCY": [""], "DURATION": [""], "DOSAGE": [""], "ROUTE": [""]}

    for ent in doc.ents:
        if li[ent.label_] == [""]:
            li[ent.label_].remove("")
            li[ent.label_] = [ent.text]
        else:
            li[ent.label_].append(ent.text)
    
    del li["DOSAGE"]
    del li["ROUTE"]
    return li

if __name__ == '__main__':
    app.run(debug=True)