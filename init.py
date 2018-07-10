from random import randint
import requests
import smtplib
import sys
from bs4 import BeautifulSoup


# Shirts
t_shirts = ['blue vineyard vines', 'pink vineyard vines']
long_shirts = ['button-1', 'button-2', 'button-3']

shirts = [t_shirts.copy(), long_shirts.copy()]

# Pants
slacks = ['khakis-1', 'khakis-2']
shorts = ['black vans', 'vineyard shorts', 'eagle shorts']

pants = [shorts.copy(), slacks.copy()]

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

outfits = []

if forecast == []:
    print('Site is not being scraped rn')
    sys.exit()

# Storing the forecast in each day
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


class Report:
    def __init__(self, day):
        self.high = int(forecast[weekdays.index(day)][0:2])
        self.low = int(forecast[weekdays.index(day)][3:5])
        self.top = None
        self.bottom = None
        self.shoe = None
        self.sweater = None
        self.belt = None

    def get_average(self):
        avg = (self.low + self.high)/2
        return avg

    def get_clothes(self):
        if self.sweater:
            self.sweater = "Take a sweater"
        else:
            self.sweater = "Don't take a sweater"

        if self.belt:
            self.belt = "Take a belt"
        else:
            self.belt = "Don't take a belt"

        return self.top, self.bottom, self.shoe, self.sweater, self.belt


day_dict = {}

for day in weekdays:
    day_dict[day] = Report(day)


def select_clothes(drawer, num, typeof):
    if len(drawer[num]) > 0:
        clothing = drawer[num].pop(randint(0, len(drawer[num])-1))
    else:
        if typeof == 'pants':
            drawer = [shorts, slacks]
        elif typeof == 'shirts':
            drawer = [t_shirts, long_shirts]
        for item in drawer:
            try:
                item.remove(day_dict[weekdays[weekdays.index(day) - 1]].get_clothes()[num])
            except ValueError:
                pass
        clothing = drawer[num].pop(randint(0, len(drawer[num])-1))

    return clothing

output_file = open('message.txt', 'w')
output_file.write('\n\n')

for day in day_dict:
    day_obj = day_dict[day]
    if day_obj.get_average() >= 75 or day_obj.high >= 80:
        number = 0
    else:
        number = 1

    day_obj.bottom = select_clothes(pants, number, 'pants')

    if day_obj.low <= 58 and day in ('monday', 'wednesday', 'friday'):
        day_obj.sweater = True
    else:
        day_obj.sweater = False

    if day_obj.bottom != 'black vans':
        day_obj.belt = True
        day_obj.top = select_clothes(shirts, number, 'shirts')
        day_obj.shoe = shoes[2]
    else:
        day_obj.belt = False
        day_obj.top = 'blue riot'
        day_obj.shoe = shoes[randint(0,1)]

    outfits.append((day_obj.get_clothes()))

for outfit in outfits:
    output_file.write("{}\n".format(outfit))
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
