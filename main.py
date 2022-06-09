import requests
from bs4 import BeautifulSoup
import random
from time import sleep
import json
import csv
import pandas as pd

url = 'https://korter.kz/новостройки-астаны'

headers = {
    "accept" : "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.865 Yowser/2.5 Safari/537.36"
}
# req = requests.get(url, headers = headers)
# src = req.text
# # print(src)
#
# with open("index.html", "w") as file:
#     file.write(src)

# with open("index.html") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="sc-1lwa91k-1 hejUmV sc-1ei3b90-0 jDbYqZ")
#
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://korter.kz" + item.get("href")
#     print(f"{item_text}: {item_href}")
#
#     all_categories_dict[item_text] = item_href
#
# with open("all_categories_dict.json", "w") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories))-1
count = 0
print(f"всего итерации {iteration_count}")

rooms = []
ap_class = []
lift = []
b_material = []
opp_replan = []
square = []
parking = []
year_const = []
price = []

for category_name, category_href in all_categories.items():
    req = requests.get(url=category_href, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    rep = [",", " ", "-", "'", ".", '/']
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    room = soup.find('sc-1lwa91k-1 hejUmV sc-1fzbwks-3 fxlwhv').str.replace('-комнатные', '')

    rooms.append(room)

    sqr = soup.find("sc-16a807r-13 sc-1sd20sg-0 cxljOk").str.partition('–')[1]

    square.append(sqr)

    prc = sqr = soup.find("sc-16a807r-13 sc-1sd20sg-0 cxljOk")
    prc.replace('от', '').replace('₸', '').replace(' ', '')
    price.append(prc)

    cls = soup.find('xbfqge-0 bpYons').find_all('td')
    ap_class.append(cls[1])

    cls = soup.find('').find_all('td')
    ap_class.append(cls[1])


    price1 = price[0].text
    builder = soup.find_all(class_ = "sc-1c8ef6y-0 imefQK")
    builder1 = builder[0].text
    address = soup.find_all(class_= "sc-1ajob5d-4 fEPCjS")
    address1 = address[0].text

    aboutComplex = soup.find(class_="sc-19nb0bc-1 kOYLCi").find_all("p")[0]
    aboutComplex1 = aboutComplex.text

    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow((
            name1,
            price1,
            builder1,
            builder1,
            address1,
            aboutComplex1
        ))

    apartments = soup.find(class_="sc-4g58jr-0 cVHOpU").find("tbody").find_all("tr")
    for item in apartments:
        apartment = item.find_all("td")

        ApartmentPicture = apartment[0].find_all('img', class_='raqiuj-0')[1]['src']
        ApartmentRoom = apartment[1].text
        ApartmentKvM = apartment[2].text
        ApartmentPriceKvM = apartment[3].text
        ApartmentPrice = apartment[4].text

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow((
                ApartmentPicture,
                ApartmentRoom[0],
                ApartmentKvM,
                ApartmentPriceKvM,
                ApartmentPrice
            ))

    # blocks = soup.find_all(class_ = "sc-1b2fk10-3 bDvgJu")
    # block = blocks[0].text
    # constructed = soup.find(class_ = "sc-1b2fk10-0 bzyZwB").find_all("div")
    # constructed = constructed[4].text
    # sales = soup.find(class_="sc-1b2fk10-0 bzyZwB").find_all("div")
    # sales = sales[5].text
    # with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
    #     writer = csv.writer(file)
    #     writer.writerow((
    #         block,
    #         constructed,
    #         sales
    #     ))

    specifications = soup.find(class_="sc-1gdjixd-0 fhfxiX").find("tbody").find_all("tr")

    for item in specifications:
        specification = item.find_all('td')
        classes = [j.text for j in specification]

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow((
                classes
        ))


    aboutApartments = soup.find(class_="sc-1gdjixd-0 fhfxiX").find("tbody").find_all("tr")
    for item in aboutApartments:
        aboutApartment = item.find_all('td')
        aboutApart = [j.text for j in aboutApartment]

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow((
                aboutApart,
            ))
    count += 1
    print(f"итерация {count}. {category_name} записан")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("well done")
        break
    print(f"Осталось итерации: {iteration_count}")
    sleep(random.randint(2, 4))