import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import ensemble
import joblib

df = pd.read_csv('data.csv')

df = df.drop('Unnamed: 0', 1)

classes = df['class'].unique()
df['lift'] = np.where(df['lift']=='отсутствует', 0, 1)
df['parking'] = np.where(df['parking']=='отсутствует', 0, 1)

label_encoder = LabelEncoder()
df['class'] = label_encoder.fit_transform(df['class'])

df['square'] = df['square'].astype('float')

df['price'] = df['price'].astype('float')

X = df.drop('price', 1)
Y = df['price']

X = X.apply(pd.to_numeric, errors='coerce')
Y = Y.apply(pd.to_numeric, errors='coerce')

X.fillna(0, inplace=True)
Y.fillna(0, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

clf = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2,
          learning_rate = 0.1, loss = 'ls')
clf.fit(X_train, y_train)

joblib.dump(clf, 'trained_model.pkl', compress=9)
