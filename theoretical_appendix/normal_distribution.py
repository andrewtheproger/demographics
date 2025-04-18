import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
n = 1000000
palette = sns.color_palette("crest", as_cmap=True)
df = pd.Series(np.random.normal(loc=5,scale=1,size=n),)
ax = sns.kdeplot(palette=palette, data=df)
plt.ylabel("")
plt.savefig(f"./images/normal_distribution.png", bbox_inches='tight')