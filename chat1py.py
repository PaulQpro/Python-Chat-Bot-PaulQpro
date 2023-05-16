# --- Импорт библиотек --- #
import nltk as nlp
import random as rnd
from pyaspeller import YandexSpeller as speller
import json
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
splr = speller()
# Vect = CountVectorizer()
# LogReg = LogisticRegression()
# RndForClass = RandomForestClassifier(n_estimators = 500, min_samples_split = 7)
Phrases = json.load(open(file="Phrases.json",encoding="UTF-8"))

# --- Использование NLTK для коррекции ввода --- #
def look_like (usr_in, example):
    usr_in = usr_in.lower()
    example = example.lower()
    distance = nlp.edit_distance(usr_in,example,transpositions=True)/len(example)
    if distance < 0.5:
        return True
    else:
        return False

# --- Фильтр символов --- #
def filter(usr):
    aphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя -+=1234567890"
    res = []
    for char in usr:
        if char in aphabet:
            res.append(char)
    return str(res).replace('[','').replace(']','').replace('\'','').replace(', ','')

# --- (Output Обработка) : ([Bot]:) --- #
def bot(UsrIn):
    changes = {change['word']:change['s'][0] for change in splr.spell(UsrIn)}
    for word, suggestion in changes.items():
        UsrIn = UsrIn.replace(word,suggestion)
    UsrIn = filter(UsrIn)
    intent = ans(UsrIn)
#     print(intent,UsrIn)
#     if not intent:
#         trans_text = Vect.transform([UsrIn])
#         print(trans_text)
# #         intent = LogReg.predict(trans_text)[0]
#         intent = RndForClass.predict(trans_text)[0]
#         print(intent)
    if intent == "bye":
        return(rnd.choice(Phrases[intent]["reactions"]),True)
    if intent:
        return(rnd.choice(Phrases[intent]["reactions"]),False)
    r = rnd.random()
    if r < .9:
        return ("Не понял",False)
    else: 
        w = []
        for index in Phrases:
            w.append(index)
        return (rnd.choice(Phrases[rnd.choice(w)]["reactions"]),False)

# --- Input Обработка --- #
def ans(UsrIn):
    for index in Phrases:
        for word in Phrases[index]["words"]:
            if look_like(UsrIn, word) == True:
                return index
    return False
# x=[];y=[]
# for index,data in Phrases.items():
#     for words in data["words"]:
#         x.append(words)
#         y.append(index)
# Vect.fit(x)
# vectX = Vect.transform(x)
# LogReg.fit(vectX,y)
# RndForClass.fit(vectX,y)
# --- Код --- #
print("Hello, User!")
on = True
while on:
    usrIn = input('>').lower()
    bot_out = bot(usrIn)
    print(bot_out[0])
    on = not bot_out[1]
