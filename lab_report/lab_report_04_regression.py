import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm

df = pd.read_excel('data/bev_meld.xlsx')

base = ['Bezirk', 'Gemnr', 'Gemeinde']
years = df.columns[3:].astype(str)
base.extend(years)
df.columns = base

year_columns = [col for col in df.columns if col.isdigit()]

bezirke = ['IL', 'RE']
df_il = df[df['Bezirk'] == bezirke[0]]
df_re = df[df['Bezirk'] == bezirke[1]]
df_reith = df[df['Gemeinde'] == 'Reith bei Seefeld']

total_population_il = df_il[year_columns].sum()
total_population_re = df_re[year_columns].sum()
total_population_reith = df_reith[year_columns].sum()
total_population_total = df[year_columns].sum()

df_reg_il = pd.DataFrame({"years": year_columns, "population": total_population_il})
df_reg_re = pd.DataFrame({"years": year_columns, "population": total_population_re})
df_reg_reith = pd.DataFrame({"years": year_columns, "population": total_population_reith})
df_reg_total = pd.DataFrame({"years": year_columns, "population": total_population_total})

df_reg_il = df_reg_il.astype({'years': 'int'})
df_reg_re = df_reg_re.astype({'years': 'int'})
df_reg_reith = df_reg_reith.astype({'years': 'int'})
df_reg_total = df_reg_total.astype(({'years': 'int'}))

def fit_model(df):
    return sm.OLS.from_formula('population ~ years', data=df).fit()

model_il = fit_model(df_reg_il)
model_re = fit_model(df_reg_re)
model_reith = fit_model(df_reg_reith)
model_total = fit_model(df_reg_total)


def calculate_population_prediction(start_year, end_year, model):
    df_pred = pd.DataFrame({"years": np.arange(start_year, end_year + 1)})
    predictions = model.predict(df_pred)
    return df_pred, predictions

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
# Bezirk Ist auch am wachsen, mit einer konstanten Steigung jedoch weniger an der Lineare Form

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
