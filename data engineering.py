import pandas as pd
import os

data = os.listdir('data')

csv = [f for f in data if f.endswith('csv')]

def engineer(csv):
    df = pd.read_csv('data/' + csv, names = ['0', '1', '2', '3', '4', '5'])

    rooms = []
    ap_class = []
    lift = []
    square = []
    parking = []
    price = []

    df = df.iloc[1: , :]

    print(df.columns)

    for row in range(len(df)):

        if df.iloc[row, 0] == 'Класс':
            break

        if df.iloc[row, 1].partition('-комнатные')[0] == 'К':
            continue
        else:
            room = df.iloc[row, 1].partition('-комнатные')[0]
            rooms.append(room)

        if df.iloc[row, 2].startswith('от'):
            sqr = df.iloc[row, 2].replace('от', '').replace('\xa0м2', '').replace('м2', '').replace(' ', '')

        else:
            sqr = df.iloc[row, 2].partition('–')

            sqr = sqr[2].replace('\xa0м2', '').replace(' ', '')

        square.append(sqr)

        prc = str(df.iloc[row, 4]).partition(' ₸')[0].replace('от', '').replace(' ', '').replace('\u200d', '')
        price.append(prc)

    while len(ap_class) < len(rooms):

        for row in range(len(df)):

            if df.iloc[row, 0] == 'Класс':
                ap_class.append(df.iloc[row, 1])

            if df.iloc[row, 0] == 'Наличие лифта':
                lift.append(df.iloc[row, 1])

            if df.iloc[row, 0] == 'Паркинг':
                parking.append(df.iloc[row, 1])

    if len(parking) == 0:
        while len(parking) < len(rooms):
            parking.append('отсутствует')

    if len(lift) == 0:
        while len(lift) < len(rooms):
            lift.append('отсутствует')

    print(rooms)
    
    print(ap_class)
    print(lift)
    print(parking)
    print(price)
    print(square)
    dict_df = {'room_numbers':rooms, 'class':ap_class, 'lift':lift, 'parking':parking, 'square':square, 'price':price}
    df = pd.DataFrame(dict_df)
    return df

df = pd.DataFrame()

for f in csv:
    print(f)
    df1 = engineer(f)
    df = pd.concat([df, df1])

print(df)

df.to_csv('data.csv')