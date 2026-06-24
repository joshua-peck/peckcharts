import pandas as pd
import matplotlib.pyplot as plt
import style
import colors

style.apply("dark")

df = pd.read_csv("datafiles/MORTGAGE30US_DGS10.csv", parse_dates=["observation_date"])
df = df.set_index("observation_date").dropna()
df["MA30"] = df["MORTGAGE30US_DGS10"].rolling(30).mean()

fig, ax = plt.subplots()
ax.plot(df.index, df["MORTGAGE30US_DGS10"], color=colors.GOLD, alpha=0.3, linewidth=1, label="Spread")
ax.plot(df.index, df["MA30"], color=colors.GOLD, linewidth=2, label="30-Period MA")
ax.set_title("30Y Mortgage – 10Y Treasury Spread")
ax.set_ylabel("Spread (pp)")
ax.legend()

plt.tight_layout()
plt.savefig("spread_ma.png")
plt.show()
