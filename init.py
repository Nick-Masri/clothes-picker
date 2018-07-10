import random
import requests
from email.mime.text import MIMEText
import smtplib
from bs4 import BeautifulSoup

t_shirts = ['blue vineyard vines', 'pink vineyard vines', 'blue riot' ]
long_shirts = ['button-1', 'button-2', 'button-3']


pants = ['khakis-1', 'khakis-2']
shorts = ['black vans', 'vineyard shorts', 'eagle shorts']

shoes = ['sambas', 'sperrys', 'nmd']

belt = False

def temperature():
    page = requests.get('https://weather.com/weather/tenday/l/Menlo+Park+CA+94025:4:US')
    soup = BeautifulSoup(page.content, 'html.parser')
    forecast_items = soup.find_all('td', class_="temp")
    temp = []
    for forecast in forecast_items[1:6]:
        temp.append(forecast.select("div")[0].get_text())
    return temp


forecast = temperature()
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

forecast_dict = {}
for day in weekdays:
    forecast_dict["{0}_high".format(day)] = int(forecast[weekdays.index(day)][0:2])
    forecast_dict["{0}_low".format(day)] = int(forecast[weekdays.index(day)][3:5])

monday_average = (forecast_dict['monday_high'] + forecast_dict['monday_low']) / 2
tuesday_average = (forecast_dict['tuesday_high'] + forecast_dict['tuesday_low']) / 2
wednesday_average = (forecast_dict['wednesday_high'] + forecast_dict['wednesday_low']) / 2
thursday_average = (forecast_dict['thursday_high'] + forecast_dict['thursday_low']) / 2
friday_average = (forecast_dict['friday_high'] + forecast_dict['friday_low']) / 2

averages_dict = {
    'monday': monday_average,
    'tuesday': tuesday_average,
    'wednesday': wednesday_average,
    'thursday': thursday_average,
    'friday': friday_average
}

output_file = open('message.txt', 'w')
output_file.write('\n\n')
for average in averages_dict:
    if averages_dict[average] >= 75 or forecast_dict['{}_high'.format(average)] >= 80:
        output_file.write('{}:\n\tWork: wear shorts and a short sleeve shirt'.format(average))
    else:
        output_file.write('{}:\n\tWork: wear long pants and a long sleeve shirt'.format(average))

    if forecast_dict['{}_low'.format(average)] <= 58:
        output_file.write('\n\tbring a sweater')


    output_file.write('\n')

output_file.close()

file = open('message.txt', 'r')


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("nicholasmasri@gmail.com", "nick91700")

msg = file.read()
print(msg)
server.sendmail("nicholasmasri@gmail.com", "masrin123@hotmail.com", msg)
server.quit()


output_file.close()
