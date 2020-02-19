import pymysql
import requests
from linkedin_scraper import Person, actions
from selenium import webdriver

linkedin_email = ""
linkedin_password = ""
GOOGLE_MAPS_KEY = ""

conexao = pymysql.connect(host='',
                             user='',
                             password='',
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



# Cria um cursor:
cursor = conexao.cursor()

# Executa o comando:
cursor.execute("SELECT userId, linkedin,address, address_latitude, address_longitude, currentCompany_Name, currentCompany_latitude, currentCompany_longitude, oldCompany_Name, oldCompany_latitude, oldCompany_longitude FROM customers")

# Recupera o resultado:
resultado = cursor.fetchall()

driver = webdriver.Chrome()
actions.login(driver, linkedin_email, linkedin_password) # if email and password isnt given, it'll prompt in terminal


#complemente dados da region onde reside
print("Buscando informações de regiões...")
print('')
for linha in resultado:

    if(linha['address_latitude'] is None and linha['address'] is not None):
        r = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + linha['address'] + '&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=' + GOOGLE_MAPS_KEY)
        result = r.json()
        lat = result['candidates'][0]['geometry']['location']['lat']
        lng = result['candidates'][0]['geometry']['location']['lng']
        print("     Capturando coordenadas - Região: " + linha['address'] + " lat:" + str(lat) + " long:" + str(lng) )
        sql = "update customers set address_latitude=%s,address_longitude=%s where userId=%s"
        cursor.execute(sql,(lat, lng,linha['userId']))
        conexao.commit()

print('')
print("Buscando informações de redes sociais...")
print('')

# Analisa localizacao e perfil rede social. 
for linha in resultado:
    print ('')
    print('     Capturando perfil: ' + linha['linkedin'])

    person = Person(linha['linkedin'], driver=driver, scrape=False)
    person.scrape(close_on_complete=False)

    experiences = str(person.experiences[0])

    inicio = experiences.find(" at ")
    token_end = experiences.find(" from ")

    companyCrawled = experiences[inicio + 4:token_end]

    r = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + companyCrawled + '&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=' + GOOGLE_MAPS_KEY)

    result = r.json()
    latCrawled = result['candidates'][0]['geometry']['location']['lat']
    lngCrawled = result['candidates'][0]['geometry']['location']['lng']

   

    #se nao possui - entao cadastra
    if(linha['currentCompany_Name'] is None):
        
        print("     Registrando empresa: " + companyCrawled + " lat: " + str(latCrawled) + " long:" + str(lngCrawled))
        sql = "update customers set currentCompany_Name=%s,currentCompany_latitude=%s,currentCompany_longitude=%s where userId=%s"
        cursor.execute(sql,(companyCrawled,latCrawled,lngCrawled,linha['userId']))
        conexao.commit()

   

    # mudou de empresa
    if(linha['currentCompany_Name'] is not None and linha['currentCompany_Name'] != companyCrawled):
        # current eh o crawlead - status de insight = 3

        # registro antigo emprego
        print('     Mudou de Empresa - De: ' + linha['currentCompany_Name'] + "   Para: " + companyCrawled )
        sql = "update customers set currentCompany_Name=%s,currentCompany_latitude=%s,currentCompany_longitude=%s, dataCompanyChanged=now(), status=3, insightNotification=1 where userId=%s"
        cursor.execute(sql,(companyCrawled,latCrawled,lngCrawled,linha['userId']))
        
        conexao.commit()

        # registro antigo emprego

        sql = "update customers set oldCompany_Name=%s,oldCompany_latitude=%s,oldCompany_longitude=%s where userId=%s"
        cursor.execute(sql,(linha['currentCompany_Name'], linha['currentCompany_latitude'],linha['currentCompany_longitude'], linha['userId']))
        conexao.commit()

        #calcula tempo deslocamento de carro 
        urlMaps = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=" + str(linha['address_latitude']) + "," + str(linha['address_longitude']) + "&destinations=" + str(latCrawled) + "," + str(lngCrawled) + "&key=" + GOOGLE_MAPS_KEY
        r = requests.get(urlMaps)
        result = r.json()
        distance = str(result['rows'][0]['elements'][0]['distance']['text'])
        duration = str(result['rows'][0]['elements'][0]['duration']['text'])
        print("     Distância: " + distance + " | Tempo de deslocamento: " + duration)
        sql = "update customers set distance=%s,duration=%s where userId=%s"
        cursor.execute(sql,(distance,duration,linha['userId']))
        conexao.commit()
  
# Finaliza a conexão
conexao.close()


