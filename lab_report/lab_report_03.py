import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import tabulate as tabulate

df = pd.read_excel('data/winter_tourism.xlsx')


# Macht man das nicht, heissen die Spalten z.B. 1993 als Zahl. Das kann in Zukunft zu Problemen führen,
# besser ist sie heissen j1993
base = ['Bez','Gemnr','Gemeinde']
years = df.columns[3:].astype(str)
base.extend('x' + years)
df.columns = base

'''
b_i = df[df.Bez == 'I']
c3 = b_i[df.columns[3:]].values[0,:]
print(c3)
v = b_i.values[0,3:]
print("V",v)
plt.plot( v )
plt.plot(years, c3)
plt.xticks(rotation=90)
plt.show()

pd.set_option('display.expand_frame_repr', False) # So werden alle Spalten angezeigt

print(df.describe())


# Kennenlernen und Überprüfen der Daten
print("Die ersten Datensätze:")
print(df.head()) # Zeige die ersten Datensätze an
print("Die letzten Datensätze:")
print(df.tail(3)) # Man kann die Anzahl als Parameter setzen

# Auswahl bestimmter Zeilen wie gewohnt
print(df[3:4]) # Wählt die Zeile 3. Bei komplexeren Abfragen iLoc verwenden
print(df.iloc[3:5,1:5])  # Von den Zeilen 3 und 4 sollen die ersten 4 Spalten angezeigt werden

# Man kann mehrere Spalten auswählen:
print(df[['Gemnr', 'x2000']])
'''

# Tabulate
print(tabulate(df, headers=df.columns))
