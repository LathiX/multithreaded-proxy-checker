import os
import threading
import requests
import random

os.system('cls')

#
# UI GENERATION
#

try:
    os.remove("goodproxies.txt")
except:
    print("")

def BlankSpace(count):
    result = ""
    for i in range(count):
        result = result + " "
    return result

Col = {
    "BrightRed": "\u001b[31;1m",
    "BrightWhite": "\u001b[37;1m",
    "BrightGreen": "\u001b[32;1m",
    "BrightGray": "\u001b[30;1m",
}

def Inp(text, type):
    if type == "int":
        inp = input(text + " ")
        inp = int(inp)
    elif type == "str":
        inp = input(text + " ")
        inp = str(inp)
    elif type == "bool":
        inp = input(text + " (Y/N) ")
        inp = str(inp).lower()
        try: 
            inp.index("y")
            inp = True
        except:
            inp = False
            
    os.system('cls')
    Header()
        
    return inp

def InputRender(color):
    result = Col["BrightGray"] + "[" + color + "+" + Col["BrightGray"] + "] " + color
    return result
    

def Header():
    print("\n" + Col["BrightRed"]                       )
    print(BlankSpace(47) + " _       _   _     _       ")
    print(BlankSpace(47) + "| | __ _| |_| |__ (_)_  __ ")
    print(BlankSpace(47) + "| |/ _` | __| '_ \| \ \/ / ")
    print(BlankSpace(47) + "| | (_| | |_| | | | |>  <  ")
    print(BlankSpace(47) + "|_|\__,_|\__|_| |_|_/_/\_\ ")
    print("" + Col["BrightWhite"])
    print(BlankSpace(47) + "+========================+ \n")

def ThrowError(error):
    print(error)
    input("Press any key, to close this window.")
    os.close()

#
# Actual work is being done here.
#

def SplitIntoMultiple(array, count):
    arraycount = len(array)
    splitArray = {}
    chunks = int(arraycount / count)
    i = 0

    for ii in range(count):
        splitArray[ii] = []

    for proxy in array:
        i = i + 1
        if i == count:
            i = 0
        splitArray[i].append(proxy)

    return splitArray

def MakeArrayFromFile(file):
    try:
        file.index(" ")
        ThrowError("File shouldn't contain spaces in their name.")
    except:
        try:
            file.index(".txt")
            parsedfilename = file
        except:
            parsedfilename = file + ".txt"

        result = []
        try:
            ourfile = open(parsedfilename, "r")
            for line in ourfile:
                result.append(line.rstrip('\n'))

            ourfile.close()
        except:
            ThrowError("File does not exists. (wrong path/no file, with name.)")

        return result

global goodProxies
goodProxies = []

def CheckProxies(index):
    for proxy in proxies[index]:
        proxyDict = { "http": "http://" + proxy, "https": "https://" + proxy, }

        try:
            r = requests.get(random.choice(urls), proxies=proxyDict, timeout=4)
            print(InputRender(Col["BrightGreen"]) + "Working proxy... " + Col["BrightWhite"] + proxy)
            goodProxies.append(proxy)
        except:
            print(InputRender(Col["BrightRed"]) + "Timed out... " + Col["BrightWhite"] + proxy)
    # print(proxies)


print("\n" + Col["BrightRed"]                       )
print(BlankSpace(47) + " _       _   _     _       ")
print(BlankSpace(47) + "| | __ _| |_| |__ (_)_  __ ")
print(BlankSpace(47) + "| |/ _` | __| '_ \| \ \/ / ")
print(BlankSpace(47) + "| | (_| | |_| | | | |>  <  ")
print(BlankSpace(47) + "|_|\__,_|\__|_| |_|_/_/\_\ ")
print("" + Col["BrightWhite"])
print(BlankSpace(47) + "+========================+ \n")
threads = Inp("Thread count.", "int")
proxies = SplitIntoMultiple(MakeArrayFromFile(Inp("The file thats contains proxies.", "str")), threads)
urls = MakeArrayFromFile(Inp("URL list.", "str"))
save = Inp("Save good proxies.", "bool")

threadlist = []
for i in range(threads):
    thread = threading.Thread(target=CheckProxies, args=(i,))
    threadlist.append(thread)
    thread.start()

for thread in threadlist:
    thread.join()

print("")
print("RESULTS: " + str(len(goodProxies)) + Col["BrightGray"] + "/" + Col["BrightWhite"] + str(len(proxies)))
if save == True:
    saveFile = open("goodproxies.txt", "a")
    for proxy in goodProxies:
        saveFile.write(proxy + "\n")

    saveFile.close()

print("SAVED RESULTS TO goodproxies.txt.")
print("")

input("")