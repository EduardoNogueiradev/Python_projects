import os
import pandas as pd
from unidecode import unidecode

def find_columns(df, cols):
        columns = []
        for i in range(0, len(cols)):
            input_col = unidecode(cols[i].lower())
            for j in range(0, len(df.columns)):
                if type(df.columns[j]) != int:
                    df_col = unidecode(df.columns[j].lower())
                    if input_col == df_col:
                        columns.append(df.columns[j])
        return columns
    
def set_default_values(df, cols):
    for col in range(0, len(df.columns)):
        for row in range(0, len(df.index)):
            match col:
                case 0:
                    if df.at[df.index[row], cols[col]] != cols[0]:
                        df.at[df.index[row], cols[col]] = int(df.at[df.index[row], cols[col]])
                case 1:
                    if df.at[df.index[row], cols[col]] != cols[1]:
                        df.at[df.index[row], cols[col]] = int(df.at[df.index[row], cols[col]])
                case 2:
                    if df.at[df.index[row], cols[col]] != cols[2]:
                        df.at[df.index[row], cols[col]] = str(df.at[df.index[row], cols[col]]).lower()
                case 3:
                    if df.at[df.index[row], cols[col]] != cols[3]:
                        df.at[df.index[row], cols[col]] = round(df.at[df.index[row], cols[col]], 2)
                case _:
                    return
    return df

def compare_values(df1, df2, cols1, cols2):
    df_incorret_values = pd.DataFrame([], columns=cols2)
    df_correc_values = pd.DataFrame([], columns=cols2)

    for df1_row in range(0, len(df1)):
        df1_value = df1.at[df1.index[df1_row], cols1[0]]
        print(df1_value)
        for df2_row in range(0, len(df2)):
            df2_value = df2.at[df2.index[df2_row], cols2[0]]
            is_find = False

            if df1_value == df2_value:
                is_find = True
                cols_different = []

                for col in range(0, len(df1.columns)):
                    value1 = df1.at[df1.index[df1_row], cols1[col]]
                    value2 = df2.at[df2.index[df2_row], cols2[col]]

                    if(value1 != value2):
                        cols_different.append(df2.columns[col])


                if len(cols_different) == 0:
                    print(df1_value, " é igual") 
                else: 
                    print("\n",df1_value, cols_different)
                    print(df1.loc[df1.index[df1_row]], "\n")
                    print(df2.loc[df2.index[df2_row]])
                    
                break

        if not is_find:
            print("não achou", df1_value)
            
    print("fim")


def compare_sheets(files, columns):
    df1 = pd.read_excel(files["file_1"]).dropna(how="any")
    df2 = pd.read_excel(files["file_2"]).dropna(how="any")

    cols_1 = []
    cols_2 = []

    if len(columns) > 0:
        for index in range(0, len(columns)):
            if index < len(columns) / 2:
                cols_1.append(columns[index])
            else: 
                cols_2.append(columns[index])

        cols_1 = find_columns(df1, cols_1)
        cols_2 = find_columns(df2, cols_2)
        
    print("executando script")

    df1 = pd.read_excel(files["file_1"], usecols=cols_1).dropna(how="any").reindex(columns=cols_1)
    df2 = pd.read_excel(files["file_2"], usecols=cols_2).dropna(how="any").reindex(columns=cols_2)

    df1 = set_default_values(df1, cols_1)
    df2 = set_default_values(df2, cols_2)

    compare_values(df1, df2, cols_1, cols_2)

    # planilha-1 nota, cfop, valor contabil, cliente
    # planilha-2 nota, cfop, valortotal, fantasiacliente

