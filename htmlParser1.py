from tkinter import *
from html.parser import HTMLParser
import css

class browsiParse(HTMLParser):
        def __init__(self,parent,page1):
            HTMLParser.__init__(self);
            self.cTg12 = ""
            self.parent = parent
            self.alinkz = ""
            self.inputType = ""
            self.total = 0
            self.page1 = page1
        def handle_starttag(self,tag,attrs):
            self.total += 1
            if self.page1.count("<")-(self.page1.count("</")+self.page1.count("<!")) > 0:
                timez = (self.total/(self.page1.count("<")-(self.page1.count("</")+self.page1.count("<!"))))*100
                self.parent.progress.config(value=timez)
                pass
            else:
                self.parent.progress.config(mode='indeterminate')
            if tag == "br":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,"\n")
                self.parent.page.config(state = DISABLED)
            elif tag == "li":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,"  • ")
                self.parent.page.config(state = DISABLED)
            elif tag == "input":
                self.cTg12 += "-"+tag
                say = ""
                for i in attrs:
                    if i[0] == "value":
                        say = i[1]
                    if i[0] == "type":
                        print("input type: "+i[1])
                        self.parent.page.config(state = NORMAL)
                        self.inputType = i[1]
                        
                        if i[1] == "checkbox":
                            self.parent.page.insert(END,"[v]")
                if self.inputType == "button":
                    h = Button(self.parent.page, text = say)
                    self.parent.page.window_create(END,window=h)
                elif self.inputType == "submit":
                    h = Button(self.parent.page, text = say)
                    self.parent.page.window_create(END,window=h)
                elif self.inputType == "text":
                    h = Entry(self.parent.page)
                    h.insert(END, say)
                    self.parent.page.window_create(END,window=h)
                self.parent.page.config(state = DISABLED)
            else:
                if tag == "a":
                    for i in attrs:
                        if i[0] == "href":
                            self.alinkz = i[1]
                    linko = self.alinkz
                    self.parent.page.tag_bind('href'+self.alinkz, '<1>', lambda e: self.parent.link(linko))
                self.cTg12 += "-"+tag
            #print("TAG: "+tag+" ATTRS: "+str(attrs))
        def handle_endtag(self, tag):
            if tag == "br":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,"\n")
                self.parent.page.config(state = DISABLED)
            else:
                bob = self.cTg12.rfind(tag)
                self.cTg12 = self.cTg12[:bob-1]
                #tag != "style" and tag != "script" and tag != "input" and tag != "form" and tag != "title" and tag != "a" and tag != "strong"
                if tag == "p" or tag == "li" or tag == "tr" or tag == "h1" or tag == "h2" or tag == "ul" or tag == "ol":
                    self.parent.page.config(state = NORMAL)
                    self.parent.page.insert(END,"\n")
                    self.parent.page.config(state = DISABLED)
        def handle_data(self, data):
            bob = self.cTg12.rfind("-")
            tagi = self.cTg12[bob+1:]
            tags = self.cTg12.split("-")
            data = data.replace("\\n","").replace("\n","")
            data = data.replace("\\t","\t").replace("\\'","\'")
            data = data.strip(" ").rstrip(" ")
            if tagi == "title":
                self.parent.title("browsi - "+str(data));
            elif tagi == "a":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,data,(tagi,"href"+self.alinkz))
                self.parent.page.config(state = DISABLED)
            elif tagi != "script" and tagi != "style":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,data,tags)
                self.parent.page.config(state = DISABLED)
            elif tagi == "style": # --------------STYLE------------
                css.run(self.parent.page, data)
