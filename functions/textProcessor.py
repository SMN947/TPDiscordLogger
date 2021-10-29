import re

class textProcessor():
    def gearBot_Clean(txt):
        txt = re.sub(r"\[`([0-9]{,2}\:){,2}[0-9]{,2}`]  ", "", txt, 1)
        txt = txt.replace(u'\u200b', '')
        content = {}
        split1 = txt.split("> ")
        action = split1[0] + ">"
        if(action == "<:gearBan:585878361491111946>"):
            print(split1[1])
            if "was banned by" in split1[1]:
                print("1")
                test = (re.sub(r"(was banned by )| for ", "\n", split1[1])).split("\n")
                content["actionTarget"] = test[0]
                content["actionAuthor"] = test[1]
                content["actionAction"] = action
                content["actionReason"] = test[2]
            elif "has been temp-banned" in split1[1]:
                print("2")
                test = (re.sub(r"has been temp-banned |by |for ", "\n", split1[1])).split("\n")
                content["actionTarget"] = test[0]
                content["actionAuthor"] = test[2]
                content["actionAction"] = action
                content["actionReason"] = "temp-ban: " + test[3]
            else:
                content = None
        elif(action == "<:gearMute:465177981221077003>"):
            print(split1[1])
            if "has been muted by" in split1[1]:
                print("3")
                test = (re.sub(r" has been muted by |\) for ", "\n", split1[1])).split("\n")
                content["actionTarget"] = test[0]
                content["actionAuthor"] = test[1]
                content["actionAction"] = action
                content["actionReason"] = test[2]
            else:
                content = None
        elif(action == "<:gearDelete:528582707521912832>"):
            if "A channel was removed" in split1[1]:
                print("3")
                test = (re.sub(r"A channel was removed: | by ", "\n", split1[1])).split("\n")
                content["actionTarget"] = test[1]
                content["actionAuthor"] = test[2]
                content["actionAction"] = action
                content["actionReason"] = ""
            else:
                content = None
        elif(action == "<:gearCreate:528593242112131082>"):
            if "A new channel was created" in split1[1]:
                print("3")
                test = (re.sub(r"A new channel was created: | by ", "\n", split1[1])).split("\n")
                content["actionTarget"] = test[1]
                content["actionAuthor"] = test[2]
                content["actionAction"] = action
                content["actionReason"] = ""
            else:
                content = None
        elif(action == "<:gearWarning:473506219919802388>"):
            if "has been warned by" in split1[1]:
                print("3")
                test = (re.sub(r" has been warned by |for ", "\n", split1[1])).split("\n")
                content["actionTarget"] = test[0]
                content["actionAuthor"] = test[1]
                content["actionAction"] = action
                content["actionReason"] = test[2]
            else:
                content = None
        else:
            content = None
        print(content)
        return content