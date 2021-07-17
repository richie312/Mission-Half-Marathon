import pandas as pd

from data.database import db_conn
db = db_conn()
df = db.default_data()
col_list = db.column_list()
default_df = pd.DataFrame(columns=col_list)
col_map = {'Day': 4, 'DistanceCovered': 1, 'Duration': 0, 'EndTime': 6, 'OxygenLevel': 2, 'PulseRate': 3, 'StartTime': 5, 'work_out_type': 7}

for col_index in range(len(col_list)):
    default_df[col_list[col_index]] = [df[i][col_map[col_list[col_index]]] for i in range(len(df))]



# filtering data
default_df = default_df[default_df["work_out_type"] == "Free Hand Exercise"]


df1 = default_df[["Day","DistanceCovered"]].groupby(by=["Day"]).sum()


print(df1)
