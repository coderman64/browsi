import urllib.request as request
from tkinter import *
from html.parser import HTMLParser
import threading
import css

class app(Tk):
    def __init__(self):

        Tk.__init__(self)

        self.title("browsi")

        self.minsize(width = 400, height = 300)

        self.titlebar = Frame(self)
        self.titlebar.pack(fill=X)

        self.navEntry = Entry(self.titlebar);
        self.navEntry.pack(fill=BOTH, expand = 1, side = LEFT)
        self.navEntry.insert(0,"AboutBrowsi")

        self.gobutton = Button(self.titlebar, text = "GO!", command = self.go)
        self.gobutton.pack(side = RIGHT)
        
        self.pagescroll = Scrollbar (self)
        self.page = Text(self, yscrollcommand = self.pagescroll.set)
        self.page.pack(fill=BOTH,expand = 1, side = LEFT)
        
        self.pagescroll.pack(side = RIGHT, fill=Y);
        self.pagescroll.config(command = self.page.yview)

        self.page.tag_config("a", foreground="blue", underline=1)
        self.page.tag_config("h1", foreground="black", font = "mono 15 bold")
        self.renderThread = None
        self.go()
    class browsiParse(HTMLParser):
        def __init__(self,parent):
            HTMLParser.__init__(self);
            self.cTg12 = ""
            self.parent = parent
            self.alinkz = ""
            self.inputType = ""
        def handle_starttag(self,tag,attrs):
            if tag == "br":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,"\n")
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
                        if i[1] == "text":
                            h = Entry(self.parent.page)
                            self.parent.page.window_create(END,window=h)
                        elif i[1] == "checkbox":
                            self.parent.page.insert(END,"[chkbox]")
                        elif i[1] == "submit":
                            h = Button(self.parent.page, text = "Submit Query")
                            self.parent.page.window_create(END,window=h)
                if self.inputType == "button":
                    h = Button(self.parent.page, text = say)
                    self.parent.page.window_create(END,window=h)
                self.parent.page.config(state = DISABLED)
            else:
                if tag == "a":
                    for i in attrs:
                        if i[0] == "href":
                            self.alinkz = i[1]
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
                if tag != "style" and tag != "script" and tag != "input" and tag != "form" and tag != "title" and tag != "a":
                    self.parent.page.config(state = NORMAL)
                    self.parent.page.insert(END,"\n")
                    self.parent.page.config(state = DISABLED)
        def handle_data(self, data):
            bob = self.cTg12.rfind("-")
            tagi = self.cTg12[bob+1:]
            data = data.replace("\\n","").replace("\n","")
            data = data.replace("\\t","\t").replace("\\'","\'")
            if tagi == "title":
                self.parent.title("browsi - "+str(data));
            elif tagi == "a":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,data,(tagi,"href"+self.alinkz))
                self.parent.page.config(state = DISABLED)
            elif tagi != "script" and tagi != "style":
                self.parent.page.config(state = NORMAL)
                self.parent.page.insert(END,data,tagi)
                self.parent.page.config(state = DISABLED)
            elif tagi == "style": # --------------STYLE------------
                css.run(self.parent.page, data)
                    
    def go(self):
        if self.renderThread == None or self.renderThread.is_alive() == False:
            self.renderThread = threading.Thread(target = self.loadPage, args = ());
            self.renderThread.start()
    def loadPage(self):
        try:
            url = self.navEntry.get()
            self.navEntry.config(state = DISABLED)
            if url=="AboutBrowsi":
                webpage = open("AboutBrowsi.html");
               
            elif url.startswith("file://"):
                webpage = open(url.replace("file:///","/").replace("\\","/").replace("file://","./"));
            else:
                if url.startswith("http") != True:
                    self.navEntry.config(state = NORMAL)
                    self.navEntry.insert(0,"http://")
                    self.navEntry.config(state = DISABLED)
                    url = "http://"+url
                webpage = request.urlopen(url);
            webpage = webpage.read()
            self.page.config(state = NORMAL)
            self.page.delete("0.0",END)
            self.page.config(state = DISABLED)
            parsy = self.browsiParse(self)
            parsy.feed(str(webpage));
            self.navEntry.config(state = NORMAL)
            #self.page.insert("0.0",webpage);
        except:
            url = self.navEntry.get()
            self.page.config(state = NORMAL)
            self.page.delete("0.0",END)
            self.page.insert(END,"Error while loading \""+url+"\". \nPlease:\n*make sure you typed the right URL\n*make sure you're hooked up to the internet\n*try again\n\nIf you've tried the above solutions and it still won't work, it is probably a problem with the browser. Hang tight until it's fixed!");
            self.page.config(state = DISABLED)
            self.navEntry.config(state = NORMAL)
        
root = app();
root.mainloop();
