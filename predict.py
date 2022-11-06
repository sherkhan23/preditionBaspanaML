import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import ensemble
import joblib
import sys

from tornado.httpserver import HTTPServer

clf = joblib.load('trained_model.pkl')

rooms = []
ap_class = []
lift = []
parking = []
square = []

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

rooms.append(3)
ap_class.append(3)
lift.append(1)
parking.append(1)
square.append(65)

dict_df = {'room_numbers':rooms, 'class':ap_class, 'lift':lift, 'parking':parking, 'square':square}
df = pd.DataFrame(dict_df)

df['lift'] = np.where(df['lift']=='отсутствует', 0, 1)
df['parking'] = np.where(df['parking']=='отсутствует', 0, 1)

cls = {'IV класс (эконом)':3,
       'III класс (комфорт)':2,
       'комфорт +':4,
       'II класс (бизнес)':1,
       'I класс (элит)':0
       }

df.replace({'class': cls})

X = df.apply(pd.to_numeric, errors='coerce')

X.fillna(0, inplace=True)

clf = joblib.load('trained_model.pkl')
# Make predictions on the loaded pre-trained model
y_pred = clf.predict(X)

print(y_pred)


# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)


    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")