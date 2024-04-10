import os
import pandas as pd
from unidecode import unidecode
from django.http import FileResponse

def find_columns(df, cols):
        columns = []
        for i in range(0, len(cols)):
            input_col = unidecode(cols[i].upper())
            for j in range(0, len(df.columns)):
                if type(df.columns[j]) != int:
                    df_col = unidecode(df.columns[j].upper())
                    if input_col == df_col:
                        columns.append(df.columns[j])
        return columns
    
def format_values(df, cols):
    df_copy = df.copy()
    df_copy.convert_dtypes()
    
    for col in range(0, len(df.columns)):
        for row in range(0, len(df.index)):
            value = df.at[df.index[row], cols[col]]
            current_row = df_copy.index[row]
            current_col = df_copy.columns[col]

            if value == cols[col]:
                df_copy.drop(current_row)
                continue

            match col:
                case 0:
                    df_copy.at[current_row, current_col] = int(value)
                case 1:
                    df_copy.at[current_row, current_col] = int(value)
                case 2:
                    df_copy.at[current_row, current_col] = str(value).upper()
                case 3:
                    df_copy.at[current_row, current_col] = round(value)
                case _:
                    return

    return df_copy

def create_excel_file(dfs, sheets_name): 
    with pd.ExcelWriter("compared_sheets.xlsx") as writer:
        file = 0
        for df in dfs: 
            df.to_excel(writer, sheet_name=sheets_name[file])  
            file =+ 1

    return FileResponse(open('compared_sheets.xlsx', 'rb'), as_attachment=True)

def compare_values(df1, df2, cols1, cols2):
    new_incorrect_cols = cols2 + ["Compared Values", "Compared Row"]

    df_incorrect_values = pd.DataFrame(columns=new_incorrect_cols)
    df_correct_values = pd.DataFrame(columns=cols1)
    df_not_found_values = pd.DataFrame(columns=cols1)

    # Listar todas os linhas da planilha 
    for row_df1 in range(0, len(df1)):
        current_row_df1 = df1.index[row_df1]
        df1_value = df1.at[current_row_df1, cols1[0]]

        # Pra cada linha da planilha 1, vai listar as linhas da planilha 2
        for row_df2 in range(0, len(df2)):
            current_row_df2 = df2.index[row_df2]
            df2_value = df2.at[current_row_df2, cols2[0]]
            is_find = False

            # Verifica se os valores das notas fiscais são iguais
            if df1_value == df2_value:
                is_find = True
                incorrect_cols_df1 = []
                incorrect_cols_df2 = []
                new_row_df1 = {}
                new_row_df2 = {}

                # Listar os valores de cada coluna 
                for col in range(0, len(df1.columns)):

                    value1 = df1.at[current_row_df1, cols1[col]]
                    value2 = df2.at[current_row_df2, cols2[col]]

                    # Cria a linha comparada de cada planilha
                    new_row_df1.update({cols1[col]: value1})
                    new_row_df2.update({cols2[col]: value2})

                    # Comparar os valores de cada coluna
                    if(value1 != value2):
                        # Adicionar as colunas com os valores incorretos 
                        incorrect_cols_df1.append(cols1[col])
                        incorrect_cols_df2.append(cols2[col])


                # Verifica a quantidade de colunas incorretas
                if len(incorrect_cols_df1) == 0:
                    # Adiciona em um novo DataFrame
                    df_correct_values.loc[len(df_correct_values)] = new_row_df1
                    df_correct_values = df_correct_values.reset_index(drop=True)
                else: 
                    def find_incorrect_values(rows, incorrect_cols):
                        incorrect_values = []

                        for values in  incorrect_cols:
                            incorrect_values.append(rows[values])

                        return incorrect_values

                    def incorrect_color_red(value):
                        color = 'red' if value in incorrect_values_df2 else 'black'
                        return 'color: %s' % color
                    

                    incorrect_values_df1 = find_incorrect_values(new_row_df1, incorrect_cols_df1)
                    incorrect_values_df2 = find_incorrect_values(new_row_df2, incorrect_cols_df2)
                    compared_row = new_row_df1

                    new_row_df2.update({"Compared Values": incorrect_values_df1})
                    new_row_df2.update({"Compared Row": compared_row})

                    df_incorrect_values.map(incorrect_color_red)
                    df_incorrect_values.loc[len(df_incorrect_values)] = new_row_df2
                    df_incorrect_values = df_incorrect_values.reset_index(drop=True)
                    
                break

        if not is_find:
            df_not_found_values.loc[len(df_not_found_values)] = new_row_df1
            df_not_found_values = df_not_found_values.reset_index(drop=True)
    
    # print(df_correct_values)
    # print(df_incorrect_values)
    # print(df_not_found_values)

    return create_excel_file([df_correct_values, df_incorrect_values, df_not_found_values], ["Correct Values", "Incorrect Values", "Not Found Values"])

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

    print(df1)
    print(df2)

    df1 = format_values(df1, cols_1)
    df2 = format_values(df2, cols_2)

    excel_file = compare_values(df1, df2, cols_1, cols_2)
    return excel_file
    # planilha-1 nota, cfop, fantasiacliente, valortotal 
    # planilha-2 nota, cfop, cliente, valor contabil

