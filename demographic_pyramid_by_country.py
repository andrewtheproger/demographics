import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_excel("dataset.xls", sheet_name='Data', )
country = input()
df = df[df["Country Name"] == country]
indicators = list(filter(lambda x: x.endswith("5Y"), df["Indicator Code"].values))
df = df[df["Indicator Code"].isin(indicators)]
df["2019"] = df.apply(lambda x: -x["2019"] if "FE" in x["Indicator Code"] else x["2019"], axis=1)
df["Пол"] = df["Indicator Code"].apply(lambda x: "Женский" if "FE" in x else "Мужской")
df["age_group"] = df["Indicator Code"].apply(lambda x: f'{x.split(".")[2][:2]}-{x.split(".")[2][2:]}')
ax = sns.barplot(
    data=df,
    x="2019", y="age_group",
    hue="Пол", dodge=False,
    palette= sns.color_palette("crest", 2))
labels = ax.get_xticks().tolist()
labels = list(map(abs, labels))
ax.set_xticklabels(labels)
plt.title(country)
plt.xlabel('Процент населения')
plt.ylabel('Возраст')
plt.savefig(f"./pyramids/{country}.png")