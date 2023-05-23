#%%
import os
import pandas as pd
from dictD import dictD
import re
import plotly.express as px

#%%
def reading_activities_from_xamls():
    activities_list = []
    listsOlist = []
    yourpath = 'xamls'

    for root, dirs, files in os.walk(yourpath, topdown=False):
        for name in files:
            with open(f"{root}/{name}", encoding="utf8") as file:
                activities_list = []
                data = file.readlines()
                for line in data:
                    if "DisplayName" in line:
                        match = re.search(r'<.*?\s', line)
                        tag = match.group()
                        tag = tag.replace(" ", "")
                        tag = tag.replace("<", "")
                        activities_list.append(tag)

            activities_list = [x.split(":")[1] if ":" in x else x for x in activities_list]
            listsOlist.append(activities_list)

    print(listsOlist)
    print("end of reading files")
    return listsOlist
#%%
def activities_to_meta_process(list_of_lists):
    change = 0
    changelist = []
    for key, values in dictD.items():
        for value in values:
            for list in list_of_lists:
                if value in list:
                    list[list.index(value)] = key
                    change = change + 1
                    changelist.append((key, value))
                    continue
    print(f"number of changes: {change}")
    print(list_of_lists)
    return list_of_lists

# %%
def longest_common_sequence(list_of_lists):
    all_sequences = []
    def longest_sequence(index1, index2, list1, list2, list1_ind, list2_ind, seq = {}):
        if index1 >= len(list1) or index2 >= len(list2):
            return seq
        if list1[index1] == list2[index2]:
            seq[f"file{list1_ind}_{list2_ind}"].append(list1[index1])
            return longest_sequence(index1+1,index2+1,list1,list2,list1_ind,list2_ind,seq)            
        else:
            return seq


    for i in range(len(list_of_lists)):
        for j in range(i+1, len(list_of_lists)):
            for index1, item1 in enumerate(list_of_lists[i]):
                for index2, item2 in enumerate(list_of_lists[j]):
                    list1_ind = i
                    list2_ind = j
                    seq = longest_sequence(index1, index2, list_of_lists[i], list_of_lists[j], list1_ind, list2_ind, {f"file{list1_ind}_{list2_ind}": []})
                    if len(seq[f"file{list1_ind}_{list2_ind}"]) > 2:
                        all_sequences.append(seq)
                        
    return all_sequences
# %%
#cleaning
def cleaning_the_results(all_sequences):
    print("cleaning start")
    results = []
    key = " "
    for item in all_sequences:
        if key == item.keys():
            continue
        else: 
            key = item.keys()
            results.append(item)            
    return results

#%%


# all together
list_of_lists_xaml = reading_activities_from_xamls()
list_of_lists_meta = activities_to_meta_process(list_of_lists_xaml)
print("start phase 3:")
list_of_all_lcs = longest_common_sequence(list_of_lists_meta)
result = cleaning_the_results(list_of_all_lcs)
print(result)


data = pd.DataFrame(result)
data = data.transpose().stack()
# data merge to one column
# data = data.stack()
data = data.reset_index()
data = data.drop(columns=["level_1"])
# rename columns
data = data.rename(columns={"level_0": "files", 0: "activities"})
data
# %%
# data analysis
data['Length'] = data['activities'].str.len()
data
# %%
# data has any duplicited rows?
# pd.isnull(data).any()

# # %%
# data.info()
# %%

fig = px.histogram(data, x="Length", hover_data=["files"], 
                  title="Distribution ")
fig.show()
# %%

# %%
df = px.data.tips()
fig = px.box(data, y="Length", hover_data=["files"])
fig.show()
# %%

data_count = data.groupby(data.Length).count()
data_count

