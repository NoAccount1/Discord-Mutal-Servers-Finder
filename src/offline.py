import pandas as pd
import time
from utils import DATA_CSV

# with open(DATA_CSV, 'r') as csv_file:
#     data  = csv.reader(csv_file)
#     writer = csv.writer(csv_file)
#     writer.writerows(data)
#     print([i for i in data])


# """
df = pd.read_csv(DATA_CSV)

results = {"": []}
current_time = time.time_ns() / 10000000
ids = []
for i, row in df.iterrows():
    for j, row2 in df.iterrows():
        last_time = current_time
        current_time = time.time_ns() / 10000000

        target1_id = row["id"]
        target1_name = row["name"]
        target1_guild_name = row["guild_name"]
        target1_guild_id = row["guild_id"]

        target2_id = row2["id"]
        target2_name = row2["name"]
        target2_guild_name = row2["guild_name"]
        target2_guild_id = row2["guild_id"]

        if target1_id not in ids:
            print(f"current name: {target1_name:<24} in {current_time - last_time}")
            ids.append(target1_id)

        if (
            target1_guild_id != row2["guild_id"]
            and target1_id == target2_id
            and target1_id not in ids
        ):
            if row["name"] in results:
                results[row["name"]].append(target1_guild_name)
                results[row["name"]].append(target2_guild_name)
            else:
                results.update({row["name"]: [target1_guild_name, target2_guild_name]})

            # print(f'Name : {row["name"]:<32} common servers : {target1_guild_name:>24} | {target2_guild_name:<24}')

results = [list(set(i)) for i in results]

print(results)
# """
