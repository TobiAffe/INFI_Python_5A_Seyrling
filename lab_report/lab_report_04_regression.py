import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm

# Laden der Daten
df = pd.read_excel('data/bev_meld.xlsx')

# Spalten umbenennen
base = ['Bezirk', 'Gemnr', 'Gemeinde'] + df.columns[3:].astype(str).tolist()
df.columns = base

# Jahr-Spalten extrahieren
year_columns = [col for col in df.columns if col.isdigit()]

# Bezirke und Gemeinden filtern
def get_population_data(df, group_by, group_value):
    filtered_df = df[df[group_by] == group_value]
    return filtered_df[year_columns].sum()

bezirke = ['IL', 'RE']
df_il = get_population_data(df, 'Bezirk', bezirke[0])
df_re = get_population_data(df, 'Bezirk', bezirke[1])
df_reith = get_population_data(df, 'Gemeinde', 'Reith bei Seefeld')
df_total = df[year_columns].sum()

# DataFrames für Regression vorbereiten
def create_population_df(years, population_data):
    return pd.DataFrame({"years": years, "population": population_data}).astype({'years': 'int'})

df_reg_il = create_population_df(year_columns, df_il)
df_reg_re = create_population_df(year_columns, df_re)
df_reg_reith = create_population_df(year_columns, df_reith)
df_reg_total = create_population_df(year_columns, df_total)

# Modelle erstellen
def fit_model(df):
    return sm.OLS.from_formula('population ~ years', data=df).fit()

model_il = fit_model(df_reg_il)
model_re = fit_model(df_reg_re)
model_reith = fit_model(df_reg_reith)
model_total = fit_model(df_reg_total)

# Vorhersage berechnen
def calculate_population_prediction(start_year, end_year, model):
    df_pred = pd.DataFrame({"years": np.arange(start_year, end_year + 1)})
    return df_pred, model.predict(df_pred)

df_pred_il, predictions_il = calculate_population_prediction(2030, 2100, model_il)
df_pred_re, predictions_re = calculate_population_prediction(2030, 2100, model_re)
df_pred_reith, predictions_reith = calculate_population_prediction(2030, 2100, model_reith)
df_pred_total, predictions_total = calculate_population_prediction(2030, 2100, model_total)

# Bevölkerung wächst schön Linear daher ist auch die Predection Linear
plt.figure(figsize=(10, 6))
plt.plot(df_pred_total.years, predictions_total, label="Regressionsgerade", color="orange")
plt.scatter(df_reg_total.years, df_reg_total.population, label="Datenpunkte", color="blue")
plt.title("Entwicklung der Gesamtbevölkerung")
plt.xlabel("Jahr")
plt.ylabel("Gesamtbevölkerung")
plt.legend()
plt.grid()
plt.show()

# Erkenntnis
# Die Bevölkerung wächst leicht Linear, gegen 2005-2011 gab es wenig zuwachs, doch 2011 > wächst die Bevölkerung wieder
plt.figure(figsize=(10, 6))
plt.plot(df_pred_reith.years, predictions_reith, label="Regressionsgerade", color="orange")
plt.scatter(df_reg_reith.years, df_reg_reith.population, label="Datenpunkte", color="blue")
plt.title("Entwicklung der Bevölkerung in Reith bei Seefeld")
plt.xlabel("Jahr")
plt.ylabel("Gesamtbevölkerung")
plt.legend()
plt.grid()
plt.show()

# Erkenntnis
# Bezirk Innsbruck wächst stark Linear, daher ist auch die prediction klar
# Bezirk RE ist auch am wachsen, mit einer konstanten Steigung jedoch weniger an der Lineare Form

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
df_reg_il.plot(x='years', y='population', ax=axes[0], color='blue', marker='o', label='Tatsächliche Werte IL')
axes[0].plot(df_pred_il['years'], predictions_il, color='red', label='Regressionsgerade IL')
axes[0].set_title('Gesamtbevölkerung IL mit Regressionsgerade')
axes[0].set_xlabel('Jahre')
axes[0].set_ylabel('Bevölkerung')
axes[0].legend()
axes[0].grid()

df_reg_re.plot(x='years', y='population', ax=axes[1], color='blue', marker='o', label='Tatsächliche Werte RE')
axes[1].plot(df_pred_re['years'], predictions_re, color='red', label='Regressionsgerade RE')
axes[1].set_title('Gesamtbevölkerung RE mit Regressionsgerade')
axes[1].set_xlabel('Jahre')
axes[1].set_ylabel('Bevölkerung')
axes[1].legend()
axes[1].grid()

fig.tight_layout()

plt.show()
