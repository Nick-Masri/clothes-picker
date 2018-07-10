from random import randint
import requests
import smtplib
from bs4 import BeautifulSoup


# Shirts
t_shirts = ['blue vineyard vines', 'pink vineyard vines', 'blue riot' ]
long_shirts = ['button-1', 'button-2', 'button-3']

shirts = [t_shirts, long_shirts]

# Pants
slacks = ['khakis-1', 'khakis-2']
shorts = ['black vans', 'vineyard shorts', 'eagle shorts']

pants = [shorts, slacks]

# Shoes
shoes = ['sambas', 'sperrys', 'nmd']
shoe_choices = shoes.copy()

# Optional Accessories
belt = False
sweater = True

# Scraping the Website for the Weekday Forecast
page = requests.get('https://weather.com/weather/tenday/l/Menlo+Park+CA+94025:4:US')
soup = BeautifulSoup(page.content, 'html.parser')
forecast_items = soup.find_all('td', class_="temp")
temp = []
for forecast in forecast_items[1:6]:
    temp.append(forecast.select("div")[0].get_text())

forecast = temp

# Storing the forecast in each day
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

class report:
    def __init__(self, day):
        self.high = int(forecast[weekdays.index(day)][0:2])
        self.low = int(forecast[weekdays.index(day)][3:5])
    def get_average(self):
        avg = (self.low + self.high)/2
        return avg
    def clothes(self, top, bottom, shoe, sweater, belt):
        return (top, bottom, shoe, sweater, belt)

for day in weekdays:
    day = report(day)

output_file = open('message.txt', 'w')
output_file.write('\n\n')
for day in weekdays:
    if day.get_average() >= 75 or day.high >= 80:
        try:
            bottom = pants[0].pop(randint(0,len(pants[0])))
        except IndexError:
            pants = [shorts, slacks]
            pants.remove(weekdays(weekdays.index(day)-1).clothes[1])
            bottom = pants[0].pop(randint(0,len(pants[0])))


        try:
            bottom = pants[0].pop(randint(0,len(pants[0])))
        except IndexError:
            pants = [shorts, slacks]
            pants.remove(weekdays(weekdays.index(day)-1).clothes[1])
            bottom = pants[0].pop(randint(0,len(pants[0])))
    else:
        try:
            bottom = pants[1].pop(randint(0,len(pants[1])))
        except IndexError:
            pants = [shorts, slacks]
            pants.remove(weekdays(weekdays.index(day)-1).clothes[1])
            bottom = pants[1].pop(randint(0,len(pants[1])))

        try:
            bottom = pants[1].pop(randint(0,len(pants[1])))
        except IndexError:
            pants = [shorts, slacks]
            pants.remove(weekdays(weekdays.index(day)-1).clothes[1])
            bottom = pants[1].pop(randint(0,len(pants[1])))

    if day.low <= 58 and day in ('monday', 'wednesday', 'friday'):
        sweater = True


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
