from django.shortcuts import render

# Create your views here.
def home(request):
    import json
    import requests
    from datetime import datetime
    from django.utils import timezone 
    api_request = requests.get("https://api.covid19api.com/summary")
    api = json.loads(api_request.content)
    
    covid_date = api['Date']
    covid_date = datetime.strptime(covid_date, "%Y-%m-%dT%H:%M:%SZ")
    covid_date_aware = timezone.make_aware(covid_date, timezone.get_current_timezone())
    
    return render(request, 'home.html', {'api': api, 'covid_date':covid_date_aware })


def charts(request):
    import json
    import requests
    from datetime import datetime
    from django.utils import timezone 
    import numpy as np
    api_request = requests.get("https://api.covid19api.com/summary")
    api = json.loads(api_request.content)
    covid_date = api['Date']
    covid_date = datetime.strptime(covid_date, "%Y-%m-%dT%H:%M:%SZ")
    covid_date_aware = timezone.make_aware(covid_date, timezone.get_current_timezone())
    
    
    api = api['Countries']
    country_list = [d['Country'].encode('utf-8').decode('utf-8') for d in api]
    country_list = np.array(country_list)
    
    total_confirmed = [d['TotalConfirmed'] for d in api]
    total_confirmed = np.array(total_confirmed)
    
    country_list_total_confirmed = [x for _, x in sorted(zip(total_confirmed,country_list), key=lambda pair: pair[0], reverse=True)][:10]
    total_confirmed = sorted(total_confirmed, reverse=True)[:10]
    
    new_confirmed = [d['NewConfirmed'] for d in api]
    new_confirmed = np.array(new_confirmed)
    country_list_new_confirmed = [x for _, x in sorted(zip(new_confirmed,country_list), key=lambda pair: pair[0], reverse=True)][:10]
    new_confirmed = sorted(new_confirmed, reverse=True)[:10]
    
    new_deaths = [d['NewDeaths'] for d in api]
    new_deaths = np.array(new_deaths)
    country_list_new_death = [x for _, x in sorted(zip(new_deaths,country_list), key=lambda pair: pair[0], reverse=True)][:10]
    new_deaths = sorted(new_deaths, reverse=True)[:10]
    
    total_deaths = [d['TotalDeaths'] for d in api]
    total_deaths = np.array(total_deaths)
    country_list_total_deaths = [x for _, x in sorted(zip(total_deaths,country_list), key=lambda pair: pair[0], reverse=True)][:10]
    total_deaths = sorted(total_deaths, reverse=True)[:10]
    
    total_recovered = [d['TotalRecovered'] for d in api]
    total_recovered = np.array(total_recovered)
    country_list_total_recovered = [x for _, x in sorted(zip(total_recovered,country_list), key=lambda pair: pair[0], reverse=True)][:10]
    total_recovered = sorted(total_recovered, reverse=True)[:10]
    
    new_recovered = [d['NewRecovered'] for d in api]
    new_recovered = np.array(new_recovered)
    country_list_new_recovered = [x for _, x in sorted(zip(new_recovered,country_list), key=lambda pair: pair[0], reverse=True)][:10]
    new_recovered = sorted(new_recovered, reverse=True)[:10]
    
    return render(request, 'charts.html', {'country_list_total_confirmed':country_list_total_confirmed, 'covid_date':covid_date_aware, 
                                           'total_confirmed_cases':total_confirmed, 
                                           'total_recovered':total_recovered, 'total_deaths':total_deaths,
                                           'new_confirmed_cases':new_confirmed,
                                           'country_list_new_confirmed':country_list_new_confirmed,
                                           'new_confirmed_deaths':new_deaths,
                                           'country_list_new_deaths':country_list_new_death,
                                           'country_list_total_deaths':country_list_total_deaths,
                                           'country_list_total_recovered':country_list_total_recovered,
                                           'country_list_new_recovered':country_list_new_recovered,
                                           'new_recovered':new_recovered,
                                           'api':api})

def curves(request):
    import json
    import requests
    from datetime import datetime
    from django.utils import timezone
    import pandas as pd
    from fbprophet import Prophet
    import numpy as np
    
    
    country_api_request = requests.get("https://api.covid19api.com/countries")
    country_api = json.loads(country_api_request.content)
    countries_list = [d['Country'] for d in country_api]
    countries_list.sort()
    
    if request.method == 'POST':
        country_selected = request.POST['dropdown_country']
        api_request = requests.get("https://api.covid19api.com/total/dayone/country/"+ country_selected)
        api = json.loads(api_request.content)
        
        confirmed_cases = [d['Confirmed'] for d in api]
        recovered = [d['Recovered'] for d in api]
        deaths = [d['Deaths'] for d in api]
        dates = [d['Date'] for d in api]
        date_list = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date() for date in dates]
        
        # df = pd.DataFrame({ 'date':dates, 'confirmed_cases':confirmed_cases, 'recovered':recovered, 'deaths':deaths })
        # df = df.rename(columns={'date':'ds'})
        # df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
        # df['ds'] = df['ds'].dt.tz_convert(None)
        # print(df.columns)
        # #model = Prophet()
        
        # results = []
        # for col in df.columns:
        #     if col != "ds":
        #         subdf = df.rename(columns={col:'y'})
        #         print(subdf.columns)
        #         model = Prophet()
        #         model.fit(subdf)
        #         result = model.predict(model.make_future_dataframe(periods = 15,freq='D'))
                
        #         result = result[['ds','yhat','yhat_upper','yhat_lower']]
        #         result.iloc[0:len(result)-15,1:4] = np.nan
        #         result.columns = [str(column) + "_" + str(col)  for column in result.columns]
        #         results.append(result)
        #     else:
        #         continue
        #     predicted_df = pd.concat(results, axis=1)
        #     predicted_df.to_csv("/Users/s.prasannachandran/Documents/example2.csv")
        
        # yhat_confirmed = predicted_df['yhat_confirmed_cases'].values.tolist()
        # yhat_upper_confirmed_cases = predicted_df['yhat_upper_confirmed_cases'].values.tolist()
        # yhat_lower_confirmed_cases = predicted_df['yhat_lower_confirmed_cases'].values.tolist()
        
        # yhat_recovered = predicted_df['yhat_recovered'].values.tolist()
        # yhat_upper_recovered = predicted_df['yhat_upper_recovered'].values.tolist()
        # yhat_lower_recovered = predicted_df['yhat_lower_recovered'].values.tolist()
        
        # yhat_deaths = predicted_df['yhat_deaths'].values.tolist()
        # yhat_upper_deaths = predicted_df['yhat_upper_deaths'].values.tolist()
        # yhat_lower_deaths = predicted_df['yhat_lower_deaths'].values.tolist()
        
        # date_list = pd.to_datetime(predicted_df['ds_confirmed_cases'].unique()).tolist()
        # #date_list = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date() for date in dates]
            
        
        return render(request, 'curves.html', {'country_list':countries_list,
                                              'confirmed_cases':confirmed_cases, 'recovered':recovered, 
                                              'deaths':deaths, 'date':date_list })
                                            #   , 'yhat_confirmed': yhat_confirmed,
                                            #   'yhat_upper_confirmed_cases':yhat_upper_confirmed_cases,
                                            #    'yhat_lower_confirmed_cases': yhat_lower_confirmed_cases,
                                            #    'yhat_recovered':yhat_recovered, 'yhat_upper_recovered':yhat_upper_recovered,
                                            #     'yhat_lower_recovered':yhat_lower_recovered, 'yhat_deaths': yhat_deaths,
                                            #     'yhat_upper_deaths': yhat_upper_deaths, 'yhat_lower_deaths': yhat_lower_deaths})
    
    else:
        api_request = requests.get("https://api.covid19api.com/total/dayone/country/india")
        api = json.loads(api_request.content)
        country = "India"
        
        confirmed_cases = [d['Confirmed'] for d in api]
        recovered = [d['Recovered'] for d in api]
        deaths = [d['Deaths'] for d in api]
        dates = [d['Date'] for d in api]
        date_list = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date() for date in dates]
        
        return render(request, 'curves.html', {'country':country,'confirmed_cases':confirmed_cases, 'recovered':recovered, 'deaths':deaths, 'date':date_list, 
                                            'country_list':countries_list})


def about(request):
    import requests
    api_request = requests.get("https://api.covid19api.com/total/dayone/country/india")
    return render(request, 'about.html', {'api':api_request})
