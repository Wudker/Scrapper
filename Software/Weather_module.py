import requests
from googletrans import Translator
from termcolor import colored

def pogoda(miasto):
  try:  
    api_key = "YOUR_KEY"
    base_url = "https://api.openweathermap.org/data/2.5/forecast?id=524901&appid="
    city = miasto
    url = f"{base_url}{api_key}&q={city}"
    response = requests.get(url).json()  
    zdanie=""
    for i in range(12):
      data=response['list'][i]['dt_txt']
      dzien=data.split(" ")[0]
      dzien=dzien.split("-")[2]+"."+dzien.split("-")[1]
      godzina=data.split(" ")[1]
      godzina=godzina.split(":")[0]+":00"
      temp=round(response['list'][i]['main']['temp']-273.15)
      opis=response['list'][i]['weather'][0]['description']
      opis_pl=translator(opis)
      main=response['list'][i]['weather'][0]['main']
      main_pl=translator(main)
      
      zdanie+=dzien+"|"+godzina+"|"+str(temp)+"|"+main_pl+"|"+opis_pl+"\n"
    return zdanie
  except:
    print(colored("blad operacji","red", attrs=["reverse", "blink"])) 
            
def translator(string):
  translator = Translator() 
  transated_text=translator.translate(string,src="en", dest="pl")
  return transated_text.text