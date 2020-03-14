import requests
from bs4 import BeautifulSoup
import json
import csv

urls = [
    'http://www.edonorwalk.com/menus/special-rolls-raw/',
    'http://www.edonorwalk.com/menus/special-rolls-cooked/',
]
rolls = []

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(
        r.content,
        'html5lib'
    )
    current_rolls = soup.findAll(
        True,
        attrs={
            'class': [
                'restaurant_menu_categories-special-rolls-raw',
                'restaurant_menu_categories-special-rolls-cooked'
            ]
        }
    )
    rolls.append(current_rolls)

parsed_rolls = []
possible_ingredients = []

for roll_type in rolls:
    for roll in roll_type:
        try:
            roll_title = roll.h2.text.strip().split(' ')
            roll_id = roll_title[0].strip('.').strip('R')
            del(roll_title[0])
            roll_name = " ".join(roll_title)
            ingredients = roll.find('div', attrs={'class': 'ingredients'}).text.strip().split(', ')

            parsed_roll = {
                'id': roll_id,
                'name': roll_name
            }

            for ingredient in ingredients:
                if ingredient not in possible_ingredients:
                    possible_ingredients.append(ingredient)
                parsed_roll[ingredient] = True

            parsed_rolls.append(parsed_roll)
        except Exception:
            break

csv_columns = [
    'id',
    'name',
]
csv_columns += possible_ingredients

csv_file = "rolls.csv"
try:
    with open(csv_file, 'w', newline='\n', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in parsed_rolls:
            writer.writerow(data)
except IOError:
    print("I/O error")
