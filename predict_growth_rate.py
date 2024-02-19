import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
country = input()
check_year = min(int(input()), 2022)
df = pd.read_excel("dataset.xls", sheet_name='Data', )
df = df[df["Country Name"] == country]
population = df[df["Indicator Code"] == "SP.POP.TOTL"]["1960"].mean()
df = df[df["Indicator Code"] == "SP.DYN.CDRT.IN"]
df.set_index('Country Name', inplace=True)
del df["Country Code"]
del df["Indicator Code"]
del df["Indicator Name"]
df = df.transpose()
df.reset_index(inplace=True, names="year")
df = df.melt(id_vars=["year"], value_vars=list(filter(lambda x: x != "year", df.columns)))
df["year"] = df["year"].astype("int64")
df = df[(df["year"] < check_year)]
death_data = list(df["value"])
df = pd.read_excel("dataset.xls", sheet_name='Data', )
df = df[df["Country Name"] == country]
df = df[df["Indicator Code"] == "SP.DYN.CBRT.IN"]
df.set_index('Country Name', inplace=True)
del df["Country Code"]
del df["Indicator Code"]
del df["Indicator Name"]
df = df.transpose()
df.reset_index(inplace=True, names="year")
df = df.melt(id_vars=["year"], value_vars=list(filter(lambda x: x != "year", df.columns)))
df["year"] = df["year"].astype("int64")
df = df[df["year"] < check_year]
birth_data = list(df["value"])
df = pd.read_excel("dataset.xls", sheet_name='Data', )
df = df[df["Country Name"] == country]
df = df[df["Indicator Code"] == "SP.POP.TOTL"]
df.set_index('Country Name', inplace=True)
del df["Country Code"]
del df["Indicator Code"]
del df["Indicator Name"]
df = df.transpose()
df.reset_index(inplace=True, names="year")
df = df.melt(id_vars=["year"], value_vars=list(filter(lambda x: x != "year", df.columns)))
df["year"] = df["year"].astype("int64")
df = df[df["year"] < check_year]
population_data = list(df["value"])
df = pd.read_excel("dataset.xls", sheet_name='Data', )
df = df[df["Country Name"] == country]
df = df[df["Indicator Code"] == "SM.POP.NETM"]
df.set_index('Country Name', inplace=True)
del df["Country Code"]
del df["Indicator Code"]
del df["Indicator Name"]
df = df.transpose()
df.reset_index(inplace=True, names="year")
df = df.melt(id_vars=["year"], value_vars=list(filter(lambda x: x != "year", df.columns)))
df["year"] = df["year"].astype("int64")
df = df[df["year"] < check_year]
migration_data = list(df["value"])
migration_data = [migration_data[i] / population_data[i] * 1000 for i in range(len(migration_data))]
data = birth_data.copy()
data.extend(death_data)
data.extend(migration_data)
delta = list(map(lambda x: list(birth_data)[x] + list(migration_data)[x] - list(death_data)[x], list(range(len(list(birth_data))))))
delta_series = pd.Series(delta)
model = stats.linregress(df["year"], delta_series)
b = model[1]
k = model[0]
delta_expected = list(map(lambda x: b + k * df["year"][x], list(range(len(delta)))))
stdev = (1 / ((len(df["year"]) - 2) / sum(list(map(lambda x: (delta_expected[x] - delta[x]) ** 2, list(range(len(delta_expected)))))))) ** 0.5
interval = 1.282 * stdev
print(interval)
years = list(range(1960, 2101)) * 3
delta_expected = list(map(lambda x: b + k * x, list(range(1960, 2101))))
delta1 = []
delta2 = []
delta3 = []
for i in delta_expected:
    delta1.append(i)
    delta2.append(i + interval)
    delta3.append(i - interval)
delta1.extend(delta2)
delta1.extend(delta3)
delta1.extend(delta)
types = len(list(delta2)) * ["Базовый"]
types.extend(len(list(delta2)) * ["Целевой"])
types.extend(len(list(delta2)) * ["Консервативный"])
types.extend(len(list(delta)) * ["Фактический"])
years = list(map(int, years))
years.extend(list(range(1960, check_year)))
print(f"При экстремально высоком приросте: {(b + interval) / (-k)} год")
print(f"При экстремально низком приросте: {(b - interval) / (-k)} год")
print(f"Наиболее вероятный исход: {b / (-k)} год")
graph = pd.DataFrame(data={"Год": years, "Прогноз": types, "Темп прироста на 1000 человек": delta1})
ax = sns.scatterplot(
    data=graph,
    hue="Прогноз",
    x="Год",
    y="Темп прироста на 1000 человек",
    palette= sns.color_palette("crest", 4))
plt.title(country)
plt.savefig(f"./growth_rate/{country}.png")