import requests
import time
import csv

search_query = dict()

counter = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Referer': 'https://autobatteries.com/search-result?y=2022',
    'application': 'aub-NA',
    'Origin': 'https://autobatteries.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
}

json_data = {
    'type': 'MAKE',
           # TUKA <- SMENI GODINA !!!!!!!!!!!!!!!!!!!!
    'year': '2020',
}

response = requests.post('https://autobatteries.com/search-service/api/ymme', headers=headers, json=json_data)


make_2022 = response.json()

makes = make_2022['APIResponse']['makes']



for make in makes:
    json_data = {
        'type': 'MODEL',
# SMENI GODINA -> TUKA <- SMENI GODINA !!!!!!!!!!!!!!!!!!!!!!!
        'year': '2020',
        'make': f'{make}',
    }   

    response = requests.post('https://autobatteries.com/search-service/api/ymme', headers=headers, json=json_data)
    
    model_2022 = response.json()
    
    models = model_2022['APIResponse']['models']
    time.sleep(1)
    
    for model in models:
        json_data = {
            'type': 'ENGINE',
   # SMENI GODINA -> TUKA <- SMENI GODINA
            'year': '2020',
            'make': f'{make}',
            'model': f'{model}',
        }

        response = requests.post('https://autobatteries.com/search-service/api/ymme', headers=headers, json=json_data)

        engine_2022 = response.json()
        
        engines = engine_2022['APIResponse']['engines']
        
        for engine in engines:
            search_query.update({f'{counter}': [make, model, engine]})
            
            counter += 1
                
            time.sleep(1)
            
            json_data = {
                'averageCommuteMinutes': '',
                'averageCommuteMiles': '',
                'primarilyStopAndGo': '',
                'dailyStops': '',
                'longPeriodsNoDriving': '',
                'startStop': False,
                'infotainment': False,
                'premiumAudio': False,
                'winch': False,
                'premiumPackage': False,
                'electronicPlugins': False,
                'snowPlow': False,
                'supercharger': False,
                'changeYear': '',
                'zip': '85001',
       # SMENI GODINA -> TUKA <- SMENI GODINA
                'year': '2020',
                'make': f'{make}',
                'model': f'{model}',
                'engine': f'{engine}',
                'subModel': None,
            }
            
            response = requests.post('https://autobatteries.com/search-service/api/part/recommendations', headers=headers, json=json_data)
            
            recommendations = response.json()
            
            lenght = len(recommendations['results'])
            
            for num in range(lenght):
                if lenght == 0:
             # SMENI GODINA -> TUKA <- SMENI GODINA
                    with open("2020.csv", "a") as f2:
                        csv_append = csv.writer(f2)
                            # SMENI GODINA -> TUKA <- SMENI GODINA
                        csv_append.writerow(["2020", make, model, engine, "N/A", "N/A", "N/A"])
                    break
                group_size = recommendations['results'][num].get('oeGroup', 'N/A')
                if group_size == "NA":
                    group_size = "N/A"
                cca = recommendations['results'][num].get('cca', 'N/A')
                if cca == "NA":
                    cca = "N/A"
                qualifier = recommendations['results'][num].get('qualifier', "N/A")
                
                if group_size == "N/A" and qualifier == "N/A" and cca == "N/A":
                    # print("Nisto")
                    continue
         # SMENI GODINA -> TUKA <- SMENI GODINA
                with open("2020.csv", "a") as f2:
                    csv_append = csv.writer(f2)
                    csv_append.writerow(["2020", make, model, engine, group_size, qualifier, cca])
                    
                    
            time.sleep(1)
            
