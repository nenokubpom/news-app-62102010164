from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"

OPEN_WEATHER_KEY = '20b96121ddc7bd5e7f05986bc7ca2e0d'
Newsapi = "http://newsapi.org/v2/everything?q={0}&from=2021-02-01&sortBy=publishedAt&apiKey={1}"
Keynews = "a4236d1709124948b6f8ee2d214123ee"

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)
    #return render_template("home.html", weather=weather)

    covidnews = get_news("covid-19",Keynews)
    return render_template("home.html",weather=weather, covidnews=covidnews)

@app.route("/news")
def news():
    newsbase = request.args.get('news')
    if not newsbase:
        newsbase = 'covid-19'
    news = get_news2(newsbase, Keynews)
    return render_template("News.html", news=news)

@app.route("/about")
def about():
    return render_template("about.html")

def get_weather(city,API_KEY):
    query = quote(city)
    url = OPEN_WEATHER_URL.format(query, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):

        description = parsed['weather'][0]['description']
        icon = parsed['weather'][0]['icon']
        press = parsed['main']['pressure']
        temperature = parsed['main']['temp']
        city = parsed['name']
        country = parsed['sys']['country']
        humidity = parsed['main']['humidity']
        wind = parsed['wind']['speed']
        weather = {'description': description,
                   'temperature': temperature,
                   'city': city,
                   'country': country,
                  'press' : press,
                    'humidity' : humidity,
                    'wind' : wind,
                    'icon' : icon
                   }
    return weather
def get_news(arnews,key):
    query = quote(arnews)
    url = Newsapi.format(query, key)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = None
    newsarr = []
    if parsed.get('articles'):
        for x in range(5):
            title = parsed['articles'][x]['title']
            description = parsed['articles'][x]['description']
            link = parsed['articles'][x]['url']
            img = parsed['articles'][x]['urlToImage']
            news = {
                'title': title,
                'description': description,
                'link': link,
                'img': img,
                }
            newsarr.append(news)
    return newsarr
def get_news2(arnews,key):
    query = quote(arnews)
    url = Newsapi.format(query, key)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = None
    newsarr = []
    if parsed.get('articles'):
        for x in parsed['articles']:
            title = x['title']
            description = x['description']
            link = x['url']
            img = x['urlToImage']
            news = {
                'title': title,
                'description': description,
                'link': link,
                'img': img,
                }
            newsarr.append(news)
    return newsarr
app.env="development"
app.run(debug=True)



