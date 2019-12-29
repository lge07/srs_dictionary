# Uses the brand new stuff from wikitionary! \0/

import re, pickle, os
import hanzidentifier as hz
from zhon import hanzi

class Definition:
    def __init__(self,text):
        # Expects a single string line.
        if type(text) != str:
            raise TypeError
            pass
        self.original = text
        self.english = []
        self.pos = "" # Incorrect standard (not Penn Treebank), but you can't have everything.
        self.meta = "" # Perhaps can be used to provide some sort of sentiment information
        self.chinese = []
        self.zh_extra = []
        self.singleletter = "[English letter names are called as in English, no other standard Mandarin name exists]"
        self.parse(self.original)
    
    def parse(self,text):
        # Expects a single string line
        td = text.split("::") # Splits into English/Chinese sections
        eng = td[0] # English part
        zh = td[1] # Chinese part
        
        # English Component
        pos = re.search(" \{.*?\}",eng).group().replace("{","")
        self.pos = pos.replace("}","")
        if "(" in eng:
            meta = re.search(" \(.*?\) ",eng).group().replace("(","")
            self.meta = meta.replace(")","")
        english = eng.replace(self.pos,"")
        self.english.append(english.replace(self.meta,""))

        # Chinese component
        if self.singleletter in zh:
            replacesec = re.search("name of the letter [A-Z]",self.meta)
            self.chinese.append(zh.replace(replacesec.group(),""))
        else:
            allzh = zh.split(",")
            for x in allzh:
                isSimplified = hz.identify(x) is hz.SIMPLIFIED or hz.identify(x) is hz.BOTH
                if isSimplified:
                    s = re.search("[{}]+".format(hanzi.characters),x)
                    e = re.search("\(.*\)",x)
                    if s!=None:
                        self.chinese.append(s.group())
                    if e!=None:
                        self.zh_extra.append(e.group())
        
## Test the definition class:
#f = open("en-cmn-enwiktionary.txt","r",encoding = "utf-8").read().split("\n")
#x = Definition(f[2915])
#print(str(x.chinese))

class Dictionary:
    def __init__(self,filename):
        # Expects a validly formatted file name.
        self.filename = filename
        self.terms = [] # TODO: Pickle?
        self.d(self.filename)
        self.div()

    def d(self,filename):
        # Expects a validly formatted file name.
        f = open(filename,"r",encoding = "utf-8")
        l = f.read().split("\n") # lines
        count = 0
        while True:
            text = l[count]
            isValid = re.search("\{",text)
            if isValid!=None:
                self.terms.append(Definition(text))
            count+=1
            if count>len(l)-1:
                break
        f.close()
    
    def div(self):
        # Expects nothing, other than that d didn't fail.
        try:
            os.mkdir(r"C:\Users\lge.DESKTOP-NNQ148M\programming\srs\newdict\div")
        except FileExistsError:
            pass
        os.chdir(r"C:\Users\lge.DESKTOP-NNQ148M\programming\srs\newdict\div")
        last = "a"
        l = []
        for t in self.terms:
            fl = t.english[0][0:1].lower()
            if fl==last:
                l.append(t)
            else:
                pickle.dump(l, open(last+".p","wb"))
                last = fl
                l = []
                l.append(t)
            # TODO: Line 30464 style extra information
            # TODO: Line 650 scenarios
    
    def retrieve(self,text):
        fl = text[0:1]
        try:
            l = pickle.load(open(fl+".p","rb"))
            found = False
            ret = []
            for d in l:
                if d.english[0]==text:
                    found = True
                    ret.append(d)
            if found==True:
                return ret
            else:
                return None     
        except FileNotFoundError:
            return None
        

Dictionary("en-cmn-enwiktionary.txt")

## Test out a div. Also, oh my God the Python commenting system sucks

#os.chdir(r"C:\Users\lge.DESKTOP-NNQ148M\programming\srs\newdict\div")
#x = pickle.load(open("b.p","rb"))
#print(x[len(x)-1].english)
#print(x[0].english)
