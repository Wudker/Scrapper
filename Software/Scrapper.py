import json
import requests
import openai
import os
from datetime import date
import Weather_module

 # 1=football 2=basketball 4=ice_hokej 5=tennis 6=handball 7=Unihokej  11=???, 12=rugby, 13=Futbol australijski 15=???? 19='Snooker  20=Table tennis 22=darty 23='Volleyball 25='waterpolo 31='badminton
HISTORY_FILE = "conversation_history.json"
MAX_CHARS = 4000
conversation_history = []
API_KEY = "API_KEY"
openai.api_key = API_KEY
ustawienia_pierwsze="You are a Polish(answers are in Polish) assistant who chose bettwen '!sport', '!general' or '!weather', based on context of given statement and return nothing else. In extreame cases when you wont be sure of category use '!general'."
ustawienia_koncowe="You are a Polish(answers are in Polish) assistant who speaks succinctly and to the point, answering given question with given data about sports events. If presented with no data or some kind of error you response 'Err'"
ustawienia_zapasowe="You are a Polish(answers are in Polish) assistant who speaks succinctly and to the point, answering given question with given data about sports event"
ustawienia_szukajoce="Your task is to extract the type of sport from the given sentence and nothing else. Example: 'What is current match score at euro?' you will respond 'football', you can guess type by famous names like mess=football, radwanska=tenis etc. If you will be presented sentence without clear situation  eg.'what is current score between france and poland?' where you are not sure is it football, basketball or any world  wide tournament, you will respond with '!help'"
ustawienia_filtrujace="your job is to translate from given word in any leanguge to match this scheme, [if football return 1, if basketball=2, if tennis=5, 6=handball, 20=Table tennis, 22=darty, 23=Volleybal] YOU CAN RERURN ONLY NUMBER!"
ustawienia_pomocne="You are a Polish(answers are in Polish) assistant who speaks succinctly and to the point, your job is to answer as best as you can ti given question"
ustawienia_pogodowe="Odpwiadasz na pytanie dotyczace pogody przy uzyciu dostarczonych ci danych."


def response_ai(input_value, ustawienia_odpowiedzi):  
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system","content": ustawienia_odpowiedzi},
                {"role": "user","content": str(input_value)}
              ]
              )   
    reply_content = completion.choices[0].message.content
    
    return reply_content

def load_history():
    global conversation_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            conversation_history = json.load(file)

def save_history():
    global conversation_history
    while len(json.dumps(conversation_history, ensure_ascii=False)) > MAX_CHARS:
        conversation_history.pop(0)
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(conversation_history, file, ensure_ascii=False, indent=4)

def gadula(input_value):
    global conversation_history
    conversation_history.append({"role": "user", "content": input_value})
    messages_to_send = [{"role": "system", "content": ustawienia_pomocne}] + conversation_history

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send
    )
    reply_content = completion.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply_content})
    save_history()
    return reply_content

def get_live_score(rodzaj_sportu):
    odpowiedz = []  
    url = "https://os-sports-perform.p.rapidapi.com/v1/events/schedule/live"
    querystring = {"sport_id": rodzaj_sportu} 

    headers = {
        "x-rapidapi-key": "YOUR_KEY",
        "x-rapidapi-host": "os-sports-perform.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring).json()

    for i in range(len(response['data'])):
        sport_type = response['data'][i]['tournament']['category']['sport']['slug']
        tournament_name = response['data'][i]["tournament"]['slug']
        team = response['data'][i]['slug']
        wynik1 = response['data'][i]['homeScore']['current']
        wynik2 = response['data'][i]['awayScore']['current']
        odpowiedz.append(f" |{sport_type}|{tournament_name}|   {team} [{wynik1}:{wynik2}] \n")  
    return ''.join(odpowiedz)  

def live_score(wybrany_sport):
        i=wybrany_sport
        try:
            odpowiedzi = get_live_score(i)
            if odpowiedzi:
                return ''.join(odpowiedzi)
            else:
                print(f"brak_spotkan_sportu_{i}")
        except Exception as e:
            print(f"brak_spotkan_sportu_{i}")
            print(f"Error: {e}")

def sport_filter(dane):
     if dane=="!help":
         print("przepraszam ale mam problem z dobraniem rodzaju sporu do pytania. czy mozesz mi powiedziec o jaki sport ci chodzi?") 
         dane=input()
     return(response_ai(dane, ustawienia_filtrujace))  

def match_on_date(wybrany_sport, data):
      odpowiedz = []  
      url = "https://os-sports-perform.p.rapidapi.com/v1/events/schedule/date"

      querystring = {"sport_id":wybrany_sport,"inverse":"false","date":data} #rok-mies-dzien

      headers = {
	      "x-rapidapi-key": "4deef17a14mshf2f2932ba596845p16b547jsncab9108b1f9f",
	      "x-rapidapi-host": "os-sports-perform.p.rapidapi.com"
      }

      response = requests.get(url, headers=headers, params=querystring).json()

      for i in range(len(response['data'])):
        sport_type = response['data'][i]["tournament"]['category']['sport']['slug']
        tournament_name = response['data'][i]["tournament"]['slug']
        team = response['data'][i]['slug']
        try:
          wynik1 = response['data'][i]['homeScore']['current']
          wynik2 = response['data'][i]['awayScore']['current']
          odpowiedz.append(f" |{sport_type}|{tournament_name}|   {team} |{wynik1} : {wynik2} \n")
        except:
          custom=response['data'][i]["status"]["description"]
          odpowiedz.append(f" |{sport_type}|{tournament_name}|   {team} |{custom} \n")  
      return ''.join(odpowiedz) 

def Sport(glowne_pytanie):
      rodzaj_sportu=(response_ai(glowne_pytanie, ustawienia_szukajoce))
      wybrany_sport=sport_filter(rodzaj_sportu)
      pytanie = glowne_pytanie+" | "+live_score(wybrany_sport) 
      odpowiedz=response_ai(pytanie, ustawienia_koncowe)
      if odpowiedz=="err":
        pytanie = glowne_pytanie+" | "+match_on_date(wybrany_sport, today)
        print(response_ai(pytanie, ustawienia_zapasowe))
      if odpowiedz!="err":
        print (odpowiedz)    
    
if __name__ == "__main__":
  while True:  
    today=date.today()
    glowne_pytanie=input()
    gatunek=(response_ai(glowne_pytanie, ustawienia_pierwsze)).lower()
    print(gatunek)
    if gatunek=='!sport':
        print(Sport(glowne_pytanie))
    if gatunek=='!general' or gatunek=='!generalne':
        print(gadula(glowne_pytanie))
    if gatunek=='!weather' or gatunek=='!pogoda':
        print(response_ai(glowne_pytanie+" "+Weather_module.pogoda('YOUR_CITY'), ustawienia_pogodowe))  