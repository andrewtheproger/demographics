import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
palette = sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=True)
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
years = list(range(1959, 2201)) * 3
population = int(population)
population = [population]
population_worst = population.copy()
population_best = population.copy()
delta.extend([b + k * i for i in range(check_year, 2201)])
year = 1960
print(f"При экстремально высокой рождаемости: {int((b + interval) / (-k))} год")
print(f"При экстремально низкой рождаемости: {int((b - interval) / (-k))} год")
print(f"Наиболее вероятный исход: {int(b / (-k))} год")
for i in delta:
    prev = population[-1]
    if year > 2020:
        population.append(int(population[-1] + i / 1000 * population[-1]))
        population_worst.append(int(population_worst[-1] + (i + interval) / 1000 * population_worst[-1]))
        population_best.append(int(population_best[-1] + (i - interval) / 1000 * population_best[-1]))
    else:
        population.append(int(population[-1] + i / 1000 * population[-1]))
        population_worst.append(int(population_worst[-1] + i / 1000 * population_worst[-1]))
        population_best.append(int(population_best[-1] + i / 1000 * population_best[-1]))
    year += 1
population.extend(population_worst)
population.extend(population_best)
types = len(list(population_worst)) * ["Базовый"]
types.extend(len(list(population_worst)) * ["Целевой"])
types.extend(len(list(population_worst)) * ["Консервативный"])
population = list(map(int, population))
years = list(map(int, years))
graph = pd.DataFrame(data={"Год": years, "Прогноз": types, "Население": population})
ax = sns.scatterplot(
    data=graph,
    hue="Прогноз",
    x="Год",
    y="Население",
    palette=sns.color_palette("crest", 3))
plt.title(country)
plt.savefig(f"./population/{country}.png")