
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
