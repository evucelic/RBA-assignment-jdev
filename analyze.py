import matplotlib.pyplot as plt
import pandas as pd

confidences_trained = pd.read_csv("tests/e2e/data/confidences_trained.csv")

plt.hist(confidences_trained["confidence"], bins=20, edgecolor='black')
plt.title("Histogram vjerojatnosti točnih predikcija na trening podacima")
plt.xlabel("Vjerojatnost (Confidence)")
plt.ylabel("Broj predikcija")
plt.savefig("tests/e2e/data/confidences_trained_histogram.png")

print(pd.__version__)