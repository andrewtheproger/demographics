import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
n = 100
palette = sns.color_palette("crest", as_cmap=True)


def y(x):
    return (5 + 2 * x) + random.randint(1, 1000)


x = []
for i in range(n):
    x.append(random.randint(1, 50))
df = pd.DataFrame({"x": x, "y": list(map(y, x))})
ax = sns.lmplot(palette=palette, data=df, x="x", y="y")
plt.savefig(f"./images//regression_2.png", bbox_inches='tight')