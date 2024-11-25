import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tabulate import tabulate
import seaborn as sns

df = pd.read_excel('data/winter_tourism.xlsx')
df_bev = pd.read_excel('data/bev_meld.xlsx')

base = ['Bez','Gemnr','Gemeinde']
years = df.columns[3:].astype(str)
base.extend('x' + years)
df.columns = base

base_bev = ['Bez','Gemnr','Gemeinde']
years_bev = df_bev.columns[3:].astype(str)
base_bev.extend('x' + years_bev)
df_bev.columns = base_bev

# 2. Erste Auswertung
# 2.1 Wachstum darstellen
def bez_population(bez):
    b = df[df.Bez == bez]
    print(tabulate(b, headers=b.columns))

    years = b.columns[3:]
    population = b.iloc[:, 3:].sum(axis=0)

    plt.scatter(years, population, color='blue', marker='o', label='Datenpunkte')
    plt.title('Punktdiagramm Bezirk ' + bez)
    plt.xlabel('Jahre')
    plt.ylabel('Tourismus')
    plt.xticks(rotation=90)
    plt.show()

bez_population('I')
bez_population('IL')


# 3. Berechnung von Min, Max, Range, Avg und standardisiertem Range
df['min'] = df.iloc[:, 3:].min(axis=1)
df['max'] = df.iloc[:, 3:].max(axis=1)
df['range'] = df['max'] - df['min']
df['avg'] = df.iloc[:, 3:].mean(axis=1)
df['range_std'] = (df['range'] / df['max']) * 100  # Standardisierter Range als Prozentsatz von max

print(tabulate(df[['Bez', 'Gemeinde', 'min', 'max', 'range', 'avg', 'range_std']], headers='keys', tablefmt='grid'))

# 3.2 Berechnung Summe
total_tourists_per_year = df.iloc[:, 3:].sum(axis=0)
print("Summe Touristen per Jahr:" + str(total_tourists_per_year))
total_tourists_all_years = total_tourists_per_year.sum()
print("Summe Touristen über alle Jahre:" + str(total_tourists_all_years))

plt.bar(total_tourists_per_year.index, total_tourists_per_year)
plt.title('Balkendiagramm Summe Touristen')
plt.xlabel('Jahre')
plt.ylabel('Tourismus')
plt.xticks(rotation=45)
plt.show()

# 4 a)
df.boxplot(column="range_std", by='Bez')
plt.show()

# 4 b)
pos = 0
labels = df['Bez'].unique()
for b in labels:
    bez = df[df.Bez == b]
    plt.boxplot(bez['range_std'], positions=[pos])
    pos += 1
plt.xticks(range(len(labels)), labels)
plt.show()

# 4 c)
sns.boxplot(x=df['Bez'], y=df['range_std'], data=df)
plt.show()

# 4.2
# Welche Jahreswerte? Annahme Jahreswere von Jahr x2020
sns.barplot(x='Bez', y='range_std', hue='Bez', data=df, palette='terrain', dodge=False)
plt.title('Standardisierter Range nach Bezirken')
plt.xlabel('Bezirk')
plt.ylabel('Standardisierter Range')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5
df_bev = df_bev.drop(columns=['Gemeinde','Bez'])
both = pd.merge(df, df_bev, how='inner', on='Gemnr')
print(tabulate(both, headers='keys', tablefmt='grid'))

# 5 a)
both['tourists_per_population_2018'] = both['x2018_x'] / both['x2018_y']

# 5 b) Boxplot
sns.boxplot(x='Bez', y='tourists_per_population_2018', data=both)
plt.title('Verhältnis von Nächtigungen zu Bevölkerung (2018) nach Bezirken')
plt.xlabel('Bezirk')
plt.ylabel('Touristen pro Einwohner')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5 c)
df_high = both.sort_values('tourists_per_population_2018', ascending=False)[:10]
df_low = both.sort_values('tourists_per_population_2018', ascending=True)[:10]

print(tabulate(df_high[['Gemeinde', 'Bez', 'x2018_x', 'x2018_y', 'tourists_per_population_2018']], headers='keys'))
print(tabulate(df_low[['Gemeinde', 'Bez', 'x2018_x', 'x2018_y', 'tourists_per_population_2018']], headers='keys'))

# 5 d)
df_gemeinde = both[both['Gemeinde'] == "Seefeld in Tirol"]
sns.boxplot(x='Gemeinde', y='tourists_per_population_2018', data=df_gemeinde)
