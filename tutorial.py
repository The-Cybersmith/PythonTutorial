import requests
import json
from plotly import *
import plotly.offline as py
#from chart_studio.plotly import plot, iplot
#import plotly.express as px
import plotly.graph_objs as go

def get_list_of_atms():
    #response_atms_json = requests.request("GET","https://api.bankofscotland.co.uk/open-banking/v2.2/atms").json()
    #list_of_atms = response_atms_json["data"][0]["Brand"][0]["ATM"] # this is needed to get to the ATMs
    #return list_of_atms
    # we had some problems with over-requesting this API and getting banned from it during the lab
    # so we here will 'pretend' it's an api, but actually we will get the content from a file 
    
    try:
        with open('data/bankofscotland.json') as json_file:  # this is how you load a file
            response_atms_json = json.load(json_file) 
            list_of_atms = response_atms_json["data"][0]["Brand"][0]["ATM"] # this is needed to get to the ATMs
            return list_of_atms
    except:
        print("Error. do you have bankofscotland.json file in your data/ folder?")

#assert  type( get_list_of_atms()) is list # check if result is a list
#assert  len( get_list_of_atms()) > 0 # check if there are any items
#assert 'eng' in get_list_of_atms()[0]['SupportedLanguages'] # check if first ATM has english as a language
#print("tests passed")

def get_rainy_atms_by_region():
    atm_list = get_list_of_atms()
    atm_num = len( atm_list)
    print("number of atms is: "+str(atm_num))

    #first, we need to get a list of regions
    regions = []
    region_amount = []
    region_amount_total = []

    for atm in atm_list:
        #print("Current index is: "+str(index))
        current_region = str(atm['Location']['PostalAddress']['CountrySubDivision'][0])
        branch_subtype = str(atm['Location']['LocationCategory'][0])
        #print("Region is: "+current_region)
        if current_region in regions:
            #print("Region already known")
            placement = regions.index(current_region)
            region_amount_total[placement] = region_amount_total[placement] + 1
            if branch_subtype == 'BranchExternal':
                region_amount[placement] = region_amount[placement] + 1
        else:
            regions.append(current_region)
            region_amount_total.append(1)
            if branch_subtype == 'BranchExternal':
                region_amount.append(1)
            else:
                region_amount.append(0)
            #print("New Region Added")

    #print(regions)
    #print(region_amount)
    
    data = [go.Bar(
       x = regions,
       y = region_amount
    )]
    fig1 = go.Figure(data=data)
    py.plot(fig1, filename = 'result1.html')

    #now we need to calculate our percentages
    region_percentages = []
    
    for index in range(0, len(regions)):
        fraction = float(region_amount[index])/float(region_amount_total[index])
        percentage = fraction*100.0
        region_percentages.append(percentage)
    
    data = [go.Bar(
       x = regions,
       y = region_percentages
    )]
    fig2 = go.Figure(data=data)
    py.plot(fig2, filename = 'result2.html')

def get_atm_accessibility():
    atm_list = get_list_of_atms()
    atm_num = len( atm_list)
    print("number of atms is: "+str(atm_num))

    #first, we need to get a list of regions
    wheelchair_num = 0.0
    audio_num = 0.0
    both_num = 0.0

    for atm in atm_list:
        #print("Current index is: "+str(index))
        sevice_list = atm['Accessibility']
        audio = False
        wheel = False
        if "AudioCashMachine" in sevice_list:
            audio = True
        if "WheelchairAccess" in sevice_list:
            wheel = True
        
        if wheel and audio:
            print("one with both")
            both_num = both_num + 1.0
        elif wheel and (not audio):
            print("one with only wheels")
            wheelchair_num = wheelchair_num + 1.0
        elif audio and (not wheel):
            print("one with only audio")
            audio_num = audio_num + 1.0
        else:
            print("no Accessibility")
            
    name_list = ['Audio Accessibility','Wheelchair Accessibility','total Accessibility']
    wheelchair_num = (wheelchair_num/atm_num)*100.0
    audio_num = (audio_num/atm_num)*100.0
    both_num = (both_num/atm_num)*100.0
    percentage_list = [audio_num,wheelchair_num,both_num]
    
    #now make the graph
    data = [go.Bar(
       x = name_list,
       y = percentage_list
    )]
    fig3 = go.Figure(data=data)
    py.plot(fig3, filename = 'accessibility.html')


print("getting region data")
get_rainy_atms_by_region()
print("getting Accessibility data")
get_atm_accessibility()
