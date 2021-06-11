import requests
b=input("URL:\n")
a=requests.get("https://s19.aconvert.com/convert/p3r68-cdx67/qyfq1-09y7y.wav")
#a=requests.get(b)
with open("2.wav","wb") as f:
    f.write(a.content)