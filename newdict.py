# Uses the brand new stuff from wikitionary! \0/

import re
import pickle


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
        self.parse(self.original)
    def parse(self,text):
        # Parses a line
        td = text.split("::") # Splits into English/Chinese sections
        eng = td[0] # English part
        zh = td[1] # Chinese part
        
        # English Component
        self.pos = re.search(" \{.*?\}",eng).group()
        self.meta = re.search(" \(.*?\) ",eng).group()
        english = eng.replace(self.pos,"")
        self.english.append(english.replace(self.meta,"")) # Worry about extra spaces

        # Chinese component
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
        # Remember to handle the single-letter things!
        