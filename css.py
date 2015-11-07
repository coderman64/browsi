import tkinter

def run(page, data):
    try:
        page.tag_config("p", foreground="black", background=None, font = "mono 12")
        page.tag_config("a", foreground="blue", background=None, underline=1, font = "mono 12")
        page.tag_config("h1", foreground="black", background = None, font = "mono 24 bold")
        page.tag_config("h2", foreground="black", background = None, font = "mono 18 bold")
        page.tag_config("strong", foreground="black", background = None, font = "mono 12 bold")
        page.tag_config("b", foreground="black", background = None, font = "mono 12 bold")
        dataleft = data
        for i in range(0, data.count("{")):
            loc1 = dataleft.find("{")
            loc2 = dataleft.find("}")
            tagstyle = dataleft[:loc1].rstrip(" ")
            print("tagstyle")
            bg1 = bg(dataleft[loc1:loc2])
            fg1 = fg(dataleft[loc1:loc2])
            page.tag_config(tagstyle, background = bg1, foreground = fg1)
            dataleft = dataleft[loc2+1:]
    except:
        print("CSS ERROR!")

def bg(data):
    loc1 = data.rfind("background-color")
    if loc1 == -1:
        return None
    loc2 = data[loc1:].find(":")
    loc3 = data[loc1:].find(";")
    color = data[loc1:][loc2+1:loc3].strip(" ").rstrip(" ")
    return color

def fg(data):
    loc1 = data.rfind("color")
    if loc1 == -1 or loc1-data.rfind("background-color") == 11:
        return None
    loc2 = data[loc1:].find(":")
    loc3 = data[loc1:].find(";")
    color = data[loc1:][loc2+1:loc3].strip(" ").rstrip(" ")
    return color
