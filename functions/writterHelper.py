import os
import csv
class writterHelper():
    def getwritterHelper(fName):
        print(os.path.join(os.getcwd() ,fName))
        f = open(os.path.join(os.getcwd() ,fName), 'w', newline='', encoding='utf-8')
        writer = csv.writer(f, delimiter=";")
        return {
            "writer": writer,
            "file": f
        }