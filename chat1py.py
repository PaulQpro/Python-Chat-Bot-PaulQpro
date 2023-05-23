# --- Импорт библиотек --- #
import nltk as nlp
import random as rnd
from pyaspeller import YandexSpeller as speller
import json
import math
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
splr = speller()
# Vect = CountVectorizer()
# LogReg = LogisticRegression()
# RndForClass = RandomForestClassifier(n_estimators = 500, min_samples_split = 7)

# --- Шестнадцатеричная цифра из дес. числа --- #
def Hex(num):
    match str(num):
        case "10": num = "A"
        case "11": num = "B"
        case "12": num = "C"
        case "13": num = "D"
        case "14": num = "E"
        case "15": num = "F"
        case _: num = str(num)
    return num

# --- Использование NLTK для коррекции ввода --- #
def look_like(usr_in, example):
    usr_in = usr_in.lower()
    example = example.lower()
    distance = nlp.edit_distance(usr_in,example,transpositions=True)/len(example)
    if distance < 0.5:
        return True
    else:
        return False

# --- Фильтр символов (вкл.) --- #
def filter(usr):
    aphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя -+=1234567890"
    res = []
    for char in usr:
        if char in aphabet:
            res.append(char)
    return str(res).replace('[','').replace(']','').replace('\'','').replace(', ','')

# --- [Bot]: --- #
def bot(UsrIn):
    intent = ans(UsrIn,False)
    #Обработка комманд
    if intent == "c1":# c1 - преобразование в двоичную
        num = int(math.fabs(int(UsrIn[2:-1])))
        result = "b"
        while True:
            if num < 2: result = result[:1]+str(num)+result[1:];break
            result = result[:1]+str(num%2)+result[1:]
            num = math.floor(num / 2)
        if int(UsrIn[2:-1]) < 0:
            result = "-("+result+")"
        return (result,False)
    if intent == "c2":# c2 - преобразование в шестнадцатеричную
        num = int(math.fabs(int(UsrIn[2:-1])))
        result = "0x"
        while True:
            if num < 16: 
                num = Hex(num)
                result = result[:2]+num+result[2:]
                break
            preres = num%16
            preres = Hex(preres)
            result = result[:2]+preres+result[2:]
            num = math.ceil(num / 16)
        if int(UsrIn[2:-1]) < 0:
            result = "-("+result+")"
        return (result,False)
    if intent == "c3":# c3 - преобразование из дв. в десятичную
        bnum = UsrIn[2:-1]
        result = 0
        blen = len(bnum)-1
        for d in bnum:
            result = result + int(d)*2**blen
            blen = blen-1
        return (result,False)
    if intent == "c4":# c4 - преобразование из шестн. в десятичную
        num = []
        for d in UsrIn[2:]:
            match(d.lower()):
                case "0": num.insert(0,0)
                case "1": num.insert(0,1)
                case "2": num.insert(0,2)
                case "3": num.insert(0,3)
                case "4": num.insert(0,4)
                case "5": num.insert(0,5)
                case "6": num.insert(0,6)
                case "7": num.insert(0,7)
                case "8": num.insert(0,8)
                case "9": num.insert(0,9)
                case "a": num.insert(0,10)
                case "b": num.insert(0,11)
                case "c": num.insert(0,12)
                case "d": num.insert(0,13)
                case "e": num.insert(0,14)
                case "f": num.insert(0,15)
        result = 0
        for i in range(0,len(num)):
            result = result + num[i]*16**i
        return (result,False)
    # Обработка ввода
    
    changes = {change['word']:change['s'][0] for change in splr.spell(UsrIn)}
    for word, suggestion in changes.items():
        UsrIn = UsrIn.replace(word,suggestion)
    UsrIn = filter(UsrIn)
    intent = ans(UsrIn,True)
#     print(intent,UsrIn)
#     if not intent:
#         vect_text = Vect.transform([UsrIn])
#         print(vect_text)
# #         intent = LogReg.predict(vect_text)[0]
#         intent = RndForClass.predict(vect_text)[0]
#         print(intent)
    if intent == "bye":
        return(rnd.choice(Phrases[intent]["reactions"]),True)
    if intent:
        return(rnd.choice(Phrases[intent]["reactions"]),False)
    if rnd.random() < .9:
        return ("Не понял",False)
    else: 
        w = []
        for index in Phrases:
            w.append(index)
        return (rnd.choice(Phrases[rnd.choice(w)]["reactions"]),False)

# c1 - преобразование в двоичную
# c2 - преобразование в шестнадцатеричную
# c3 - преобразование из двоичной в десятичную
# c4 - преобразование из шестн. в десятичную

# --- Input Обработка --- #
def ans(UsrIn:str,formatted:bool):
    if formatted:
        for index in Phrases:
            for word in Phrases[index]["words"]:
                if look_like(UsrIn, word) == True:
                    return index
        return False
    if UsrIn[:2] == "b(" and UsrIn[-1] == ")":
        return "c1"
    if UsrIn[:2] == "x(" and UsrIn[-1] == ")":
        return "c2"
    if UsrIn[:2] == "d(" and UsrIn[-1] == ")":
        return "c3"
    if UsrIn[:2] == "0x":
        return "c4"
    return False
# --- Обучение (выкл.) --- #
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
Phrases = json.load(open(file="Phrases.json",encoding="UTF-8"))
print("Hello, User!")
on = True
while on:
    usrIn = input('>').lower()
    bot_out = bot(usrIn)
    print(bot_out[0])
    on = not bot_out[1]
