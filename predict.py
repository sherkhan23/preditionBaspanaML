import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import ensemble
import joblib
import sys
import socket


from tornado.httpserver import HTTPServer

clf = joblib.load('trained_model.pkl')

rooms = []
ap_class = []
lift = []
parking = []
square = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 2009))
server.listen(4)
print('working...')
client_socket, address = server.accept()
data = client_socket.recv(1024).decode('utf-8')
print(data)
content = "weldone".encode('utf-8')
client_socket.send(content)
print('shut dowm')



rooms.append(3)
ap_class.append(3)
lift.append(1)
parking.append(1)
square.append(65)

dict_df = {'room_numbers':rooms, 'class':ap_class, 'lift':lift, 'parking':parking, 'square':square}
df = pd.DataFrame(dict_df)

df['lift'] = np.where(df['lift']=='отсутствует', 0, 1)
df['parking'] = np.where(df['parking']=='отсутствует', 0, 1)

cls = {'IV класс (эконом)',
       'III класс (комфорт)',
       'комфорт +',
       'II класс (бизнес)',
       'I класс (элит)'
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