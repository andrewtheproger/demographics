import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_excel("dataset.xls", sheet_name='Data', )

df = df[df["Indicator Code"] == "SP.DYN.CBRT.IN"]
df.set_index('Country Name', inplace=True)

del df["Country Code"]
del df["Indicator Code"]
del df["Indicator Name"]
df = df.transpose()
df.reset_index(inplace=True, names="year")
print(df)
df = df.melt(id_vars=["year"], value_vars=list(filter(lambda x: x != "year", df.columns)))
print(df)
df["year"] = df["year"].astype("int64")
df = df[df["Country Name"].isin(["Nigeria", "China", "United States", "Russian Federation"])]
ax = sns.relplot(
    data=df,
    x="year", y="value",
    hue="Country Name",
    kind="line",
    palette = sns.color_palette("mako", 4))
plt.xlabel('Год')
plt.ylabel('Рождаемость на 1000 человек')
ax.legend.set_title("Страна")
new_labels = ['Китай', 'Нигерия', 'Россия', 'США']
for t, l in zip(ax._legend.texts, new_labels):
    t.set_text(l)
plt.savefig("birth_rate.png", transparent=True)
