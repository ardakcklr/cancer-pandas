import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# clincial.tsv dosyasının okunması
cancer = pd.read_csv(r'C:\Users\rdkck\Downloads\clinical.tsv', sep='\t')

# '--' değerleri NaN olarak okutulur
cancer = cancer.replace("'--", np.nan)
# Tüm değerleri NaN olan sütunlar silinir
cancer = cancer.dropna(axis=1, how='all')

# İstnenen sütunlar haricindeki sütunlar silinir
cancer.drop(cancer.columns.difference(['case_submitter_id', 'age_at_index', 'days_to_death', 'gender', 'race',
                                       'vital_status', 'year_of_birth', 'year_of_death', 'age_at_diagnosis',
                                       'ajcc_pathologic_stage', 'icd_10_code', 'primary_diagnosis', 'prior_malignancy',
                                       'prior_treatment', 'site_of_resection_or_biopsy', 'synchronous_malignancy',
                                       'tissue_or_organ_of_origin', 'year_of_diagnosis', 'treatment_type']), 1, inplace=True)


# NaN değer içermesi sebebiyle silinen sütunların sayısı
print("Number of rows deleted because they had a NaN value: " + str(cancer.isna().any(axis=1).sum()) + "\n")

# NaN değeri olan satırlar silinir
cancer = cancer.dropna()
# 'Not Reported' ya da 'not reported' değerleri olan satırlar silinir
cancer = cancer.drop([col for col in cancer.columns if cancer[col].eq("not reported").any() or
                      cancer[col].eq("Not Reported").any()], axis=1)
# Hasta barkodu (case_submitter_id) aynı olan satırlardan ilki kalacak şekilde tekrar edenler silinir
cancer = cancer.drop_duplicates(subset=["case_submitter_id"], keep= 'first')
# Hasta barkodu (case_submitter_id) sütunu DataFrame'in index'i olarak atanır
cancer = cancer.set_index("case_submitter_id")

# dataFrame'deki satır ve sütun sayısı
print("Number of rows in cancer dataframe: " + str(cancer.shape[0])
      + "\nNumber of columns in cancer dataframe: " + str(cancer.shape[1]))

#print(list(cancer.columns.values))
