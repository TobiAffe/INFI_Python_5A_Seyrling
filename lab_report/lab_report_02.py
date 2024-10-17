import numpy as np
from matplotlib import pyplot as plt

d = np.genfromtxt('data/london_weather.csv', delimiter=",", skip_header=1 )

dt = d[:,0]
day = (dt % 100).astype('i')
month = (dt % 10000 / 100).astype('i')
year = (dt % 100000000 / 10000).astype('i')

# 1.1 Darstellung der Temperaturunterschiede
# Jeder Boxplot beinhaltet die Temperatur des entsprechenden Jahres.
# Die Box in der Mitte beinhaltet 50%, wobei der rote Strich die Box in zwei
# 25% hälften einordnet
# Die Schnurrhaare präsentieren jeweils 25%
# 1990 war mit 35 Grad das heißeste Jahr
temp = d[:,4]
temp1980 = temp[year == 1980]
temp1990 = temp[year == 1990]
temp2000 = temp[year == 2000]
temp2010 = temp[year == 2010]
plt.boxplot([temp1980, temp1990, temp2000, temp2010])
plt.xticks(np.arange(1,5),["1980","1990","2000","2010"])
plt.title("1.1 Temperature Differences")
plt.ylabel("Temperature")
plt.xlabel("Year")
plt.show()

# 1.2 Zeitlicher Verlauf
# Die Temperaturen (y-Achse) des jeweiligen Tag (x-Achse) sind mit blauen Punkten eingezeichnet
# Der Verlauf von Sommer und Winter lässt sich schön verfolgen
# Jahresanfag und Ende sind kälter (Winter) und die Mitte ist Wärmer (Sommer)
plt.plot(temp1980, "b*")
plt.title("1.2 Temperature 1980")
plt.ylabel("Temperature")
plt.xlabel("Days")
plt.show()

# 1.3 Herausfinden von Wetterextremen
# In den beiden Graphen sind die Temperaturen von 1980 als blau eingezeichnet
# und die Temperaturen von 2010 als rot eingezeichnet
coldx1980 = temp1980[temp1980 < np.nanquantile(temp1980, 0.25)]
coldx2010 = temp2010[temp2010 < np.nanquantile(temp2010, 0.25)]
hotx1980 = temp1980[temp1980 > np.nanquantile(temp1980, 0.75)]
hotx2010 = temp2010[temp2010 > np.nanquantile(temp2010, 0.75)]

# Das Jahr 1990 ist an kalten Tagen im Durchschnitt wärmer als 2010
plt.plot(coldx1980, "b*", label="Cold 1980")
plt.plot(coldx2010, "r*", label="Cold 2010")
plt.title("1.3 Cold Extremes")
plt.legend()
plt.show()

# Es zeigt sich ein anderer Trend als wie bei den Cold Extrems, 2010 ist an heißen Tagen
# im Durchschitt wäremer als 1990
# Klimawandel?
plt.plot(hotx1980, "b*", label="Hot 1980")
plt.plot(hotx2010, "r*", label="Hot 2010")
plt.title("1.3 Hot Extremes")
plt.legend()
plt.show()

# 1.4 Mittelwerte der einzelnen Jahre
# Von den letzten 10 Jahren werden die Mittelwerte der Temperatur berechnet und
# als Balkendiagramm angezeigt
# Man erkennt keine große Abweichung der Temperatur
year_unique = np.unique(year)
last_10_years = year_unique[-10:]
mean_temps = []
for i in last_10_years:
    temp_year = temp[year == i]
    temp_mean = np.nanmean(temp_year)
    mean_temps.append(temp_mean)

plt.bar(last_10_years, mean_temps)
plt.title("1.4 Mean Temperatures")
plt.ylabel("Mean Temperature")
plt.xlabel("Year")
plt.show()

# 1.5 Weitere Darstellung
# Max Schneetiefe der letzten 10 Jahre
# Es wird die maximale Schneetiefe der letzten 10 Jahre berechnet und als Balkendiagramm angezeigt
# Man erkennt, dass es in 2011 sowie 2014 bis 2016 nicht geschneit hat
# Ansonten ist die maximale Schneetiefe nicht besonders aufregend, mit einem Maximalwert
# von 7cm über die letzten 10 Jahre
snow = d[:,-1]
max_snow = []
for i in last_10_years:
    snow_year = snow[year == i]
    max_snow.append(np.max(snow_year))

plt.bar(last_10_years, max_snow)
plt.title("1.5 Max Snow Depth")
plt.ylabel("Snow Depth in cm")
plt.xlabel("Year")
plt.show()
