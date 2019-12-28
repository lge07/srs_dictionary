# Uses the brand new stuff from wikitionary! \0/

import re, pickle, os

class Definition:
    def __init__(self,text):
        # Expects a single line.
        if type(text) != str:
            raise TypeError
            pass
        self.original = text
        self.english = []
        self.pos = "" # Incorrect standard, but you can't have everything.
        self.meta = "" # Perhaps can be used to provide some sort of sentiment information
        self.chinese = []
        self.singleletter = "[English letter names are called as in English, no other standard Mandarin name exists]"
        self.parse(self.original)
    def parse(self,text):
        # Parses a line
        td = text.split("::") # Splits into English/Chinese sections
        eng = td[0] # English part
        zh = td[1] # Chinese part
        
        # English Component
        self.pos = re.search(" \{.*?\}",eng).group()
        if "(" in eng:
            self.meta = re.search(" \(.*?\) ",eng).group()
        english = eng.replace(self.pos,"")
        self.english.append(english.replace(self.meta,"")) # Worry about extra spaces

        # Chinese component
        if self.singleletter in zh:
            replacesec = re.search("name of the letter [A-Z]",self.meta)
            self.chinese.append(zh.replace(replacesec.group(),""))
        else:
            allzh = zh.split(",")
            for x in allzh:
                s = re.search("/.*/",x)
                if s!=None:
                    self.chinese.append(x.replace(s.group(),""))
        
# Test the definition class:
#f = open("en-cmn-enwiktionary.txt","r",encoding = "utf-8").read().split("\n")
#x = Definition(f[5])
#print(str(x.english))

class Dictionary:
    def __init__(self,filename):
        # Expects a validly formatted file name.
        self.filename = filename
        self.terms = [] # A list for containing the entries within the dictionary.
        self.d(self.filename)
        self.div()

    def d(self,filename):
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
                pickle.dump(l, open(fl+".p","wb"))
                last = fl
                l = []
            # Line 30464 style extra information

    def retrieve(self,text):
        pass

Dictionary("en-cmn-enwiktionary.txt")