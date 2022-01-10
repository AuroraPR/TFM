import os

def getIndex(base):
    if base=="silence":
        return 0
    if base=="wc":
        return 1
    if base=="tap":
        return 2
    if base=="bash":
        return 3
    if base=="dryer":
        return 4
    if base=="other":
        return 5
    return -1


f = open("audio_wc.csv", "w")
f.write("name,target,category\n")
for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.endswith(".wav"):
            base=filename.split("-")
            f.write(filename+","+str(getIndex(base[0]))+","+base[0]+"\n")
            print(filename)
f.close()


