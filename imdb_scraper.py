from bs4 import BeautifulSoup
import sys
import datetime
import urllib3
from tqdm import tqdm
import random
import sendgrid
import os
from sendgrid.helpers.mail import *

current_year = int(datetime.datetime.now().year)
i=1
year = random.randint(1998, current_year +1)
print("Suggestions for ", year)
http = urllib3.PoolManager()
url = "http://www.imdb.com/search/title?release_date=" + str(year) + "," + str(year) + "&title_type=feature"
response = http.request('GET', url)
soup = BeautifulSoup(response.data,"html.parser")
movieList = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

random_movie = random.randint(0, len(movieList) -1 )
movie = movieList[random_movie]

div = movie.find('div', attrs={'class': 'lister-item-content'})
header = div.findChildren('h3', attrs={'class': 'lister-item-header'})
movie_name = str((header[0].findChildren('a'))[0].contents[0].encode('utf-8').decode('ascii', 'ignore'))
search_url = "https://www.google.co.in/search?q=fmovies"
response = http.request('GET', search_url)
soup = BeautifulSoup(response.data, "html.parser")
fmovie_url = soup.find('cite')
fmovie_url = str(fmovie_url)
new_url = fmovie_url.replace("<cite>","")
new_url = new_url.replace("<b>","")
new_url = new_url.replace("</cite>","")
new_url = new_url.replace("</b>","")
movie_name_for_url = movie_name.replace(" ","+")
new_url = new_url + 'search/' + str(movie_name_for_url) + '.html'
print(new_url)

mail_ids = ["debashis.gt540m@gmail.com"]
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
for mail_id in mail_ids:
    from_email = Email("deba-suggests@debashis.com")
    to_email = Email(mail_id)
    subject = "Movie Suggestion for the day!"
    content = Content("text/html", "<html><head></head><body>Today's recommended movie based on IMDB ratings is " + str(movie_name) + ' ( Released in ' + str(year) + ' ). Click here to <a href=' + str(new_url) + '  >watch it</a> </body> !')
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
