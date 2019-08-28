import pandas as pd
import numpy as np
import sys

results = pd.read_csv("./pct_outputs.csv",  encoding="ISO-8859-1", header=0, index_col=0)

candidates = results.columns
industries = results.index

if sys.argv[1] in industries:
	sorted_names = results.sort_values(sys.argv[1], axis=1, ascending=False).columns.values

	print(sys.argv[1])
	for i in range(0, len(candidates)):
		print(str(i + 1) + ". " + sorted_names[i])

elif sys.argv[1] in candidates:
	sorted_industries = results.sort_values(sys.argv[1], axis=0, ascending=False).index.values
	print(sys.argv[1])
	for i in range(0, len(industries)):
		print(str(i + 1) + ". " + sorted_industries[i])

else:
	print("ERROR: not an industry or candidate")