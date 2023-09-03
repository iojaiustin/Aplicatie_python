from bs4 import BeautifulSoup
import requests
import re
import phonenumbers

def check_number(number):
    phone_number = phonenumbers.parse(number)
    return phonenumbers.is_possible_number(phone_number)

def get_phones(url):
    rgx_phone = re.compile(r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}")
    phones = []
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    for div in soup.find_all(["div","address"]):
        for phone in re.findall(rgx_phone, str(div)):
            if re.findall(rgx_phone, str(div)) not in phones:
                
                phones.append(re.findall(rgx_phone, str(div)))
    return phones

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match                                                                                                        


def search(oras):
    list = []
    adrese = []
    numere = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'
    }
    content = requests.get("https://"+oras+".cylex.ro/magazin-cu-articole-pentru-pescuit-%C5%9Fi-v%C3%A2n%C4%83toare/",headers=headers)
    soup = BeautifulSoup(content.text,"lxml")
      
    for element in soup.find_all(['span']):
        element = str(element)

        if 'd-block pl-3' in element:
            if "acum" not in element:
                element = element.replace('<span class="d-block pl-3">','')
                element = element.replace('</span>','')
                if element[1].isdigit():
                    numere.append(element)
                else:
                    adrese.append(element)
                

    for adresa in adrese:
        list.append(str(adresa)+" "+str(numere[adrese.index(adresa)]))
    
    return list


def get_cities():
    list = []
    for word in open('orase.txt','r'):
        if str(word):
            word = str(word).replace("\n","")
            list.append(word)

    return list


def main():
    for city in get_cities():
        file = open(city+".txt","w")
        for element in search(city):
                file.write(element+"\n")

main()
