import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# Reading the file 'clincial.tsv'
cancer = pd.read_csv(r'local_path', sep='\t') # insert file's local path between ''

# '--' values are replaced with NaN 
cancer = cancer.replace("'--", np.nan)
# Columns which has only NaN values are dropped
cancer = cancer.dropna(axis=1, how='all')

# Columns which are not going to be used for analysis are dropped
cancer.drop(cancer.columns.difference(['case_submitter_id', 'age_at_index', 'days_to_death', 'gender', 'race',
                                       'vital_status', 'year_of_birth', 'year_of_death', 'age_at_diagnosis',
                                       'ajcc_pathologic_stage', 'icd_10_code', 'primary_diagnosis', 'prior_malignancy',
                                       'prior_treatment', 'site_of_resection_or_biopsy', 'synchronous_malignancy',
                                       'tissue_or_organ_of_origin', 'year_of_diagnosis', 'treatment_type']), 1, inplace=True)


# Number of rows deleted because they had a NaN value
print("Number of rows deleted because they had a NaN value: " + str(cancer.isna().any(axis=1).sum()) + "\n")

# Rows that has a NaN value are dropped
cancer = cancer.dropna()
# Rows with 'Not Reported' or 'not reported' values are dropped
cancer = cancer.drop([col for col in cancer.columns if cancer[col].eq("not reported").any() or
                      cancer[col].eq("Not Reported").any()], axis=1)
# Recurring rows with the same case_submitter_id are dropped except for the first iteration
cancer = cancer.drop_duplicates(subset=["case_submitter_id"], keep= 'first')
# case_submitter_id column is set as the index of the dataFrame
cancer = cancer.set_index("case_submitter_id")

# Number of rows and columns in the dataFrame
print("Number of rows in cancer dataframe: " + str(cancer.shape[0])
      + "\nNumber of columns in cancer dataframe: " + str(cancer.shape[1]))

print(list(cancer.columns.values))



## primary_diagnosis values which has at least 10 patients visualized on a vertically stacked bar graph

v = cancer.primary_diagnosis.value_counts()
df2 = cancer[cancer.primary_diagnosis.isin(v.index[v.gt(10)])]
diagnosis_list = df2['primary_diagnosis'].tolist()
diagnosis_list = list(set(diagnosis_list))
#print(diagnosis_list)
df2 = df2[['primary_diagnosis', 'gender']]
df2 = df2.groupby(['primary_diagnosis']).gender.value_counts().to_frame()
df2.columns.values[0] = "counts"

pivot = pd.pivot_table(data=df2, index=['primary_diagnosis'], columns=['gender'], values='counts')
ax = pivot.plot.barh(stacked=True, color =['lightseagreen', 'tomato'], figsize=(18,6))
ax.set_title('Number of Patients', fontsize=20)
ax.set_xlim(0,400)
ax.set_yticklabels(diagnosis_list, fontsize=6)
plt.show()




## Showing the number of patients for every cancer type (primary_diagnosis) in a descending order 
## Visualizing age distribution for all patients and patients who has the most seen cancer type in the same plot as seperate histograms

df3 = cancer.groupby('primary_diagnosis')['gender'].count().sort_values(ascending=False).reset_index(name='count')
#print(df3)

most_seen = df3['primary_diagnosis'].iloc[0]

fig, axes = plt.subplots(1, 2)


df3_2 = cancer.loc[cancer['primary_diagnosis'] == most_seen]
df3_2['age_at_index']= df3_2['age_at_index'].astype(int)
df3_2.plot.hist(bins=df3_2['age_at_index'].nunique(), ax=axes[0],title='Ages of patients who are diagnosed with\n' + most_seen)

#print(df3_2)


cancer['age_at_index']= cancer['age_at_index'].astype(int)
cancer.plot.hist(bins=df3_2['age_at_index'].nunique(), ax=axes[1], title='Ages of all cancer patients')

plt.show()


## Cancer type(primary_diagnosis)  with the highest life expectancy(days_to_death) average 

cancer[["days_to_death"]] = cancer[["days_to_death"]].apply(pd.to_numeric)
df4 = cancer.groupby('primary_diagnosis')["days_to_death"].mean().reset_index(name='mean')
max = df4.loc[df4['mean'].idxmax()]
print(max)


## Scatter plot visualizing the relation between the age which the patient is diagnosed (age_at_diagnosis) and life expectancy (days_to_death)

cancer.plot.scatter(x='age_at_diagnosis', y='days_to_death', s=100 , c='red')
plt.show()




## "exposure.tsv"  file which gives information related to cancer patients alcohol and cigarette consumption, is read into the dataFrame with 'case_submitter_id' 
## column as the index ("'--" and "Not Reported" values are replaced with NaN)
## Drop columns which only has NaN values
## Drop rows which has any NaN valued cells 
## Merging patients' data in the 'cancer' and 'exposure' DataFrames, using case_submitter_id field
## and load it into a new dataframe named 'cancer_exposure'

exposure = pd.read_csv(r'local_path\exposure.tsv', sep='\t') # insert local path for exposure.tsv

exposure = exposure.replace("'--", np.nan)
exposure = exposure.replace("Not Reported", np.nan)
exposure = exposure.dropna(axis=1, how='all')
exposure = exposure.dropna()

exposure = exposure.drop_duplicates(subset=["case_submitter_id"], keep= 'first')
exposure = exposure.set_index("case_submitter_id")
## Number of columns and rows of the newly constructed dataFrame
print("Number of rows in cancer dataframe: " + str(cancer.shape[0])
      + "\nNumber of columns in cancer dataframe: " + str(cancer.shape[1]))
cancer_exposure = cancer.merge(exposure, left_index=True, right_index=True)

print(cancer_exposure)
#print(list(cancer_exposure.columns.values))



## Visualizing the tissue or organ of origin percentages on patients with a history of drinking and smoking at least 3 cigarettes day, on a pie chart

#v = cancer_exposure.cigarettes_per_day.value_counts()
cancer_exposure[["cigarettes_per_day"]] = cancer_exposure[["cigarettes_per_day"]].apply(pd.to_numeric)

#cancer_exposure = cancer_exposure.loc[cancer_exposure['alcohol_history'] == 'Yes']
#df5 = df5[df5.cigarettes_per_day.isin(v.index[v.gt(3)])]
cancer_exposure.loc[(cancer_exposure['alcohol_history'] == 'Yes') & (cancer_exposure['cigarettes_per_day'] > 3)]
#print(cancer_exposure)


cancer_exposure.groupby('tissue_or_organ_of_origin').sum().plot(kind='pie', autopct='%1.1f%%',subplots=True, figsize=(10,5),
                                                      title = 'Percentage of tissue or organ of origin', legend = None)

#plt.xlabel('categories')
#plt.ylabel('values')


plt.show()
