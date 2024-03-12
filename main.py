import requests, json, datetime, twilio.rest, os, dotenv

# load environment variables
dotenv.load_dotenv()

url = 'https://www.alphavantage.co/query'
payload = {
    'apikey': 'EFUBFJGSWCUOWCEU', 
    'function': 'TIME_SERIES_DAILY', 
    'symbol': 'TSLA'
    }

response = requests.get(url, params=payload).json()

time_series_daily = response.get('Time Series (Daily)')
data_lst = []

# define counter to quit in time
count = 0

for key in time_series_daily:
    data_lst.append(time_series_daily[key])
    count += 1
    if count > 1:
        break

# Get news (if needed)
persentage_dif = abs(float(data_lst[0].get('4. close'))/float(data_lst[1].get('4. close')) - 1) * 100
if persentage_dif > 1:
    url = 'https://newsapi.org/v2/everything'
    payload = {
            'q': 'TSLA',
            'from': str(datetime.datetime.today() - datetime.timedelta(days=28)).split(' ')[0],
            'sortBy': 'publishedAt',
            'apiKey': 'e1dc1b7fda1f436c9e9a45fc23e45c7d'
        }
    news = requests.get(url, params=payload).json().get('articles')[:3]
    client = twilio.rest.Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    with open('news.json', 'w') as file:
        file.write(json.dumps(news, indent=4))
    # msg = client.messages.create(body='oki', from_='+15017122661', to='+380635418793')
    # print(msg)
else:
    print(abs(float(data_lst[0].get('4. close'))/float(data_lst[1].get('4. close'))))

with open('response.json', 'w') as file:
    file.write(json.dumps(response, indent=4))
