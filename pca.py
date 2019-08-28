import pandas as pd
import matplotlib.pyplot as mpl
import numpy as np

results = pd.read_csv("./pct_outputs.csv",  encoding="ISO-8859-1", header=0, index_col=0)
results_arr = results.values

candidates = results.columns
industries = results.index

mean_vector = np.mean(results_arr, axis=1)
for i in range(0, len(candidates)):
	results_arr[:, i] = results_arr[:, i] - mean_vector
print(results_arr.shape)
print(results_arr)

DIMENSIONS = 2
u, s, vh = np.linalg.svd(results_arr)
reduced = np.matmul(np.matmul(u[:, 0:DIMENSIONS], np.identity(DIMENSIONS) * s[0:DIMENSIONS]), vh[0:DIMENSIONS])	

pd.DataFrame(data=reduced[0:2, :], columns=candidates).transpose().to_csv("./pca.csv")

for i in range(0, len(candidates)):
	for j in range(0, len(candidates)):
		print(candidates[i], "\t", candidates[j], "\t", np.linalg.norm(reduced[:, i] - reduced[:, j]))

fig, ax = mpl.subplots()
ax.scatter(reduced[0, :], reduced[1, :])
for i, name in enumerate(candidates):
	ax.annotate(name, (reduced[0][i], reduced[1][i]))
mpl.xticks([-.1, -0.05, 0, 0.05, .1])
mpl.yticks([-.1, -0.05, 0, 0.05, .1])
mpl.show()
