import urllib.request as request
from tkinter import *
from html.parser import HTMLParser
import threading
from htmlParser1 import browsiParse

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
        self.navEntry.bind("<Return>",lambda e: self.go())

        self.gobutton = Button(self.titlebar, text = "GO!", command = self.go)
        self.gobutton.pack(side = RIGHT)
        
        self.pagescroll = Scrollbar (self)
        self.page = Text(self, yscrollcommand = self.pagescroll.set, wrap = "word")
        self.page.pack(fill=BOTH,expand = 1, side = LEFT)
        
        self.pagescroll.pack(side = RIGHT, fill=Y);
        self.pagescroll.config(command = self.page.yview)

        self.page.tag_config("a", foreground="blue", underline=1)
        self.page.tag_config("h1", foreground="black", font = "mono 15 bold")
        self.renderThread = None

        self.browsiParse = browsiParse;
        
        self.go()
                        
    def go(self):
        if self.renderThread == None or self.renderThread.is_alive() == False:
            self.renderThread = threading.Thread(target = self.loadPage, args = ());
            self.renderThread.start()
    def link (self, url):
        if url.startswith("http") or url.startswith("www."):
            self.navEntry.delete(0,END);
        elif url.startswith("/"):
            uuii = self.navEntry.get().find("/",8)
            self.navEntry.delete(uuii,END)
        self.navEntry.insert(END,url);
        self.go();
    def loadPage(self):
        try:
            url = self.navEntry.get()
            self.navEntry.config(state = DISABLED)
            if url.lower()=="aboutbrowsi":
                webpage = open("AboutBrowsi.html"); 
            elif url.startswith("file://"):
                webpage = open(url.replace("file:///","/").replace("\\","/").replace("file://","./"));
            else:
                if url.startswith("http") != True and url.startswith("www."):
                    self.navEntry.config(state = NORMAL)
                    self.navEntry.insert(0,"http://")
                    self.navEntry.config(state = DISABLED)
                    url = "http://"+url
                elif url.startswith("http") != True:
                    self.navEntry.config(state = NORMAL)
                    url = "http://www.duckduckgo.com/lite?q="+url
                    self.navEntry.delete(0,END)
                    self.navEntry.insert(0,url)
                    self.navEntry.config(state = DISABLED)
                webpage = request.urlopen(url);
            webpage = webpage.read()
            self.page.config(state = NORMAL)
            self.page.delete("0.0",END)
            self.page.config(state = DISABLED)
            parsy = self.browsiParse(self)
            print("HERE")
            parsy.feed(str(webpage));
            print("and HERE")
            self.page.config(state = NORMAL)
            if self.page.get("0.0",END).startswith('b\''):
                self.page.delete("0.0","0.2")
            print("hi")
            self.page.config(state = DISABLED)
            self.navEntry.config(state = NORMAL)
        except:
            url = self.navEntry.get()
            self.page.config(state = NORMAL)
            self.page.delete("0.0",END)
            self.page.insert(END,"Error while loading \""+url+"\". \nPlease:\n*make sure you typed the right URL\n*make sure you're hooked up to the internet\n*try again\n\nIf you've tried the above solutions and it still won't work, it is probably a problem with the browser. Hang tight until it's fixed!");
            self.page.config(state = DISABLED)
            self.navEntry.config(state = NORMAL)
        
root = app();
root.mainloop();
