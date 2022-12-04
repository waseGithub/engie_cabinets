import pandas as pd

data = pd.read_csv (r'eventlog.csv')   
df = pd.DataFrame(data)
print(df)
