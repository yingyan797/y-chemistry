from flask import Flask, render_template, request
from chemeq import Equation
import pandas as pd

app = Flask(__name__)

def read_eltab(fn="static/eltab.csv"):
    data = pd.read_csv(fn)
    kb = [[[data.iloc[0, i] for i in range(3)]] + [["",i,""] for i in [1,2,3,4,5,6,7,8,9,0,"(",")", "+", "Del", "AC"]] + [[]] + [[data.iloc[1, i] for i in range(3)]]]
    kb.append([[data.iloc[j, i] for i in range(3)] for j in [2,3]] +[[]]+[["",i,""] for i in ["OH", "CO3", "NO3", "SO4", "CH", "O2", "H2O", "CO2"]] + [[]] + [[data.iloc[j, i] for i in range(3)] for j in range(4,10)])        
    kb.append([[data.iloc[j, i] for i in range(3)] for j in [10,11]] + [[] for _ in range(10)] + [[data.iloc[j, i] for i in range(3)] for j in range(12,18)])        
    for r in range(1,3):
        kb.append([[data.iloc[j, i] for i in range(3)] for j in range(r*18, (r+1)*18)])
    kb.append([[data.iloc[j, i] for i in range(3)] for j in [54,55]] + [[]] + [[data.iloc[j, i] for i in range(3)] for j in range(71,86)])        
    kb.append([[data.iloc[j, i] for i in range(3)] for j in [86,87]] + [[]] + [[data.iloc[j, i] for i in range(3)] for j in range(103,118)])        
    for f,t in [(56, 71), (88, 103)]:
        kb.append([[] for _ in range(3)] + [[data.iloc[j, i] for i in range(3)] for j in range(f,t)])        
    return kb

def eqread(text:str):
    end = False
    l = 0
    for i in range(len(text)):
        if not end:
            if text[i].isalnum() or text[i] in "[({})]+ ":
                continue
            end = True
            l = i
        elif not text[i].isalnum() and text[i] not in "[({})]+ ":
            continue
        else:
            return text[:l], text[i:]
    return text, ""

class Website:
    def __init__(self) -> None:
        self.side = 0
        self.words = ["",""]
        self.eltab = read_eltab()

    def enter(self, k):
        if k == "Del":
            self.words[self.side] = self.words[self.side][:-1]
        elif k == "AC":
            self.words[self.side] = ""
        else:
            self.words[self.side] += k

class Keyboard:
    def __init__(self) -> None:
        self.text = ""
        self.keywords = [[".","\"",":","<",">","{","}","(",")","self","__init__(self"],["def ","class ","for ","while ","in ","range(","len(","return ","lambda ","print(","raise ","if ","elif ","else:","+= ","*= "]]
        [kw.sort() for kw in self.keywords]
        self.funcs = ["enter","enter_tab","space","<-","AC"]
        self.names = []

    def parse_names(self, symbs="_"):
        word = ""
        self.names = []
        for c in self.text:
            if c.isalnum() or c in symbs:
                word += c
            else:
                if len(word) > 1 and word not in self.names:
                    dup = False
                    for k in range(len(self.keywords)):
                        for kw in self.keywords[k]:
                            if word == kw[:len(kw)-k]:
                                dup = True
                                break
                    if not dup:
                        self.names.append(word)
                word = ""                    
        if word:
            self.names.append(word)
    def op(self, opname):
        match opname:
            case "enter":
                self.text += "\n"
            case "enter_tab":
                lines = self.text.split("\n")
                nid = 0
                for c in lines:
                    if c == " ":
                        nid += 1
                self.text += "\n"+"  "*(int(nid/2)+1)
            case "space":
                self.text += " "
            case "<-":
                self.text = self.text[:-1]
            case "AC":
                self.text = ""

site = Website()
keyboard = Keyboard()
@app.route('/', methods=['GET', 'POST'])    # main page
def index():
    fm = request.form
    print(fm)
    cofl, cofr, info, nt = [], [], "", 0
    if sw:=fm.get("sw"):
        site.side = int(sw)
    elif fm.get("calc_tree"):
        (cofl, cofr), info = Equation(site.words[0], site.words[1]).eq_tree()
        nt = len(info)
    elif fm.get("calc_gauss"):
        (cofl, cofr), info = Equation(site.words[0], site.words[1]).eq_guass()
    elif fm.get("sync"):
        if eq:=fm.get("equation"):
            site.words[0], site.words[1] = eqread(eq)
        else:
            site.words[0] = fm.get("compl")
            site.words[1] = fm.get("compr")
    for k, v in fm.items():
        if k.startswith("type_") and v:
            site.enter(k[5:])
            break
    return render_template("index.html", cofl=cofl, cofr=cofr, info=info, nt=nt, site=site)

@app.route('/editor', methods=['GET', 'POST'])    # main page
def editor():
    fm = request.form
    keyboard.text = fm.get("tbox")
    if not keyboard.text:
        keyboard.text = ""
    if word:=fm.get("word"):
        keyboard.text += word
    elif func:=fm.get("func"):
        keyboard.op(func)
    keyboard.parse_names()
    return render_template("editor.html", kb=keyboard)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
