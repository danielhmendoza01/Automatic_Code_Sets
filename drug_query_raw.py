# %%
import pandas as pd

# %%
#Global paramenters
#API URLs from RxNorm
base_url = "https://rxnav.nlm.nih.gov/REST/rxcui/"
base_url_2 = "https://rxnav.nlm.nih.gov/REST/"
base_url_3 = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name="
#RxNorm methods
getAllRelatedInfo = "/allrelated.json"
getRelatedByType = "/related.json?tty=IN"
#dataframe
df = pd.DataFrame()

# %%
#Method to get drug with only the opioid ingredient
def query_self(name_of_drug):
    rd_df = pd.read_json(base_url+name_of_drug+getRelatedByType)
    rd_df = pd.DataFrame(rd_df.relatedGroup.conceptGroup)
    rd_df = pd.DataFrame(rd_df.conceptProperties[0])
    return rd_df

#Method to get all drugs with an opioid ingredient
def query_drug(name_of_drug):
    row = 0
    df = pd.DataFrame()
    rd_df = pd.read_json(base_url+name_of_drug+getAllRelatedInfo)
    rd_df = pd.DataFrame(rd_df.allRelatedGroup.conceptGroup)
    rd_df = rd_df.loc[rd_df["tty"] != "DF"].reset_index(drop=True)
    rd_df = rd_df.loc[rd_df["tty"] != "DFG"].reset_index(drop=True)
    while row < rd_df.shape[0]:
        if(pd.isna(rd_df.conceptProperties[row]) is True):
            row+=1
        else:
            new_df = pd.DataFrame(rd_df.conceptProperties[row])
            if df.empty:
                df = new_df
            else:
                df = pd.concat([df, new_df]).reset_index(drop=True)
            row += 1
    return df

# %%
#Read in ingredients from excel file
drug_ingredients = pd.read_excel("Antidepressants_Ingredients.xlsx", header=None)
drugs = []
#Get rxcui for each ingredient
for drug in drug_ingredients[0]:
    ingredient = pd.read_json(base_url_3+drug)
    drugs.append(ingredient.idGroup.rxnormId[0])

#loop array to get complete list of drugs
df = pd.DataFrame()
for drug in drugs:
    self_df = query_self(drug)
    ingredient = self_df["name"].values[0]
    self_df["ingredient"] = ingredient
    merg_df = query_drug(drug)
    merg_df["ingredient"] = ingredient
    df = pd.concat([df, self_df]).drop_duplicates(subset=['rxcui']).reset_index(drop=True)
    df = pd.concat([df, merg_df]).drop_duplicates(subset=['rxcui']).reset_index(drop=True)
df

# %%
#Reduce to usefull columns
df = df[['rxcui', 'name',"tty", "ingredient"]]
df

# %%
#Export
df.to_excel("New_Complete_Antidepressants_List.xlsx", index=False)

# %%
df_list = pd.read_excel("Complete_Antidepressants_List.xlsx")
df_list = df_list[['Code', 'Description','TTY']]
df_list.rename(columns= {'Code' : 'rxcui', 'Description': 'name'}, inplace = True)
df_list

# %%
#Identify new drugs found
same_drug_count = 0
new_drug_count = 0
drug_not_found_count = 0
same_drug = pd.DataFrame()
new_drug = pd.DataFrame()
for code in df['rxcui']:
    drug_name = df['name'].where(df['rxcui'] == code).dropna().values[0]
    if df_list.isin([int(code)]).any().any() == True:
        same_drug_count += 1
        same_drug = pd.concat([same_drug, df.loc[df['rxcui']==code]]).reset_index(drop=True)
    else:
        new_drug_count += 1
        new_drug = pd.concat([new_drug, df.loc[df['rxcui']==code]]).reset_index(drop=True)
print('Same drug count: ', same_drug_count)
print('New drug count: ', new_drug_count)

# %%
#export
new_drug.to_excel("New_Antidepressant_Added.xlsx", index=False)

# %%
absent_drugs = pd.DataFrame()
count = 0
#for every code from the combind excel list
for code in df_list['rxcui']:
    if df.isin([str(code)]).any().any() == True:
        count+=1
    else:
        absent_drugs = pd.concat([absent_drugs, df_list.loc[df_list['rxcui']==code]]).reset_index(drop=True)
print('Count: ', count)
absent_drugs

# %%
#find the status of the not found drugs
df_status = pd.DataFrame()
index = 0
for code in absent_drugs['rxcui']:
    getRxcuiHistoryStatus = 'rxcui/{}/historystatus.json'.format(code)
    df_type = pd.read_json(base_url_2+getRxcuiHistoryStatus)
    df_type = pd.DataFrame(df_type.rxcuiStatusHistory.metaData, index=[0])
    df_type['rxcui'] = code
    df_status = pd.concat([df_status, df_type]).drop_duplicates(subset=['rxcui']).reset_index(drop=True)
df_status

# %%
df_not_found = absent_drugs.merge(df_status, on='rxcui')
df_not_found = df_not_found[['rxcui', 'name','TTY', 'status']]
df_not_found

# %%
df_active=df_not_found.loc[df_not_found['status']== 'Active'].reset_index(drop=True)
df_obsolete = df_not_found.loc[df_not_found['status']== 'Obsolete'].reset_index(drop=True)

# %%
#export
df_not_found.to_excel("Status_of_Not_found_Antidepressant.xlsx", index=False)
df_active.to_excel("Active_Not_Found_Antidepressant.xlsx", index=False)
df_obsolete.to_excel("Obsolete_Not_Found_Antidepressant.xlsx", index=False)


