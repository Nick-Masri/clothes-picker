from random import randint
import requests
import smtplib
from bs4 import BeautifulSoup


# Shirts
t_shirts = ['blue vineyard vines', 'pink vineyard vines']
long_shirts = ['button-1', 'button-2', 'button-3']

shirts = [t_shirts, long_shirts]

# Pants
slacks = ['khakis-1', 'khakis-2']
shorts = ['black vans', 'vineyard shorts', 'eagle shorts']

pants = [shorts, slacks]

# Shoes
shoes = ['sambas', 'nmd', 'sperrys']
shoe_choices = shoes.copy()

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
        return top, bottom, shoe, sweater, belt


for day in weekdays:
    day = report(day)


def select_clothes(drawer, num):
    try:
        clothing = drawer[num].pop(randint(0, len(drawer[num])))
    except IndexError:
        if drawer == 'pants':
            drawer = [shorts, slacks]
        elif drawer == 'shirts':
            drawer = [t_shirts, long_shirts]

        drawer.remove(weekdays(weekdays.index(day) - 1).clothes[1])
        clothing = drawer[num].pop(randint(0, len(drawer[num])))

    return clothing

output_file = open('message.txt', 'w')
output_file.write('\n\n')

for day in weekdays:
    if day.get_average() >= 75 or day.high >= 80:
        number = 0
    else:
        number = 1

    bottom = select_clothes(pants, number)

    if day.low <= 58 and day in ('monday', 'wednesday', 'friday'):
        sweater = True
    else:
        sweater = False

    if bottom != 'black vans':
        belt = True
        top = select_clothes(shirts, number)
    else:
        belt = False
        top = 'blue riot'


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
