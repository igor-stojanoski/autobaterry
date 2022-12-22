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
    'year': '2022',
}

response = requests.post('https://autobatteries.com/search-service/api/ymme', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"type":"MAKE","year":"2023"}'
#response = requests.post('https://autobatteries.com/search-service/api/ymme', headers=headers, data=data)

make_2022 = response.json()

makes = make_2022['APIResponse']['makes']



for make in makes:
    json_data = {
        'type': 'MODEL',
        'year': '2022',
        'make': f'{make}',
    }   

    response = requests.post('https://autobatteries.com/search-service/api/ymme', headers=headers, json=json_data)
    
    # models.update({json_data['make']: response.json()['APIResponse']['models']})
    
    model_2022 = response.json()
    
    models = model_2022['APIResponse']['models']
    time.sleep(2)
    
    for model in models:
        json_data = {
            'type': 'ENGINE',
            'year': '2022',
            'make': f'{make}',
            'model': f'{model}',
        }

        response = requests.post('https://autobatteries.com/search-service/api/ymme', headers=headers, json=json_data)

        engine_2022 = response.json()
        
        engines = engine_2022['APIResponse']['engines']
        
        for engine in engines:
            search_query.update({f'{counter}': [make, model, engine]})
            
            counter += 1
    
            # with open("models.json", "w") as f1:
                # json.dump(search_query, f1)

            # print(search_query)
            # print(f"\n\n\n")
                
            time.sleep(2)
            
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
                'year': '2022',
                'make': f'{make}',
                'model': f'{model}',
                'engine': f'{engine}',
                'subModel': None,
            }
            
            response = requests.post('https://autobatteries.com/search-service/api/part/recommendations', headers=headers, json=json_data)
            
            recommendations = response.json()
            
            lenght = len(recommendations['results'])
            
            for num in range(lenght):
                # if lenght > 1 and recommendations['results'][num]['recommendedText'] == "Recommended Fit":
                if lenght == 0:
                    with open("2022.csv", "a") as f2:
                        csv_append = csv.writer(f2)
                        csv_append.writerow(["2022", make, model, engine, "N/A", "N/A", "N/A"])
                    break
                group_size = recommendations['results'][num]['oeGroup']
                if group_size == "NA":
                    group_size = "N/A"
                cca = recommendations['results'][num]['cca']
                if cca == "NA":
                    cca = "N/A"
                qualifier = recommendations['results'][num].get('qualifier', "N/A")
                
                with open("2022.csv", "a") as f2:
                    csv_append = csv.writer(f2)
                    csv_append.writerow(["2022", make, model, engine, group_size, qualifier, cca])
                    
                    
            time.sleep(3)
            
