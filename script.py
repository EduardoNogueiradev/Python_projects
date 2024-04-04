import pandas as pd
import os

# Função para verificar se os valores são iguais
def is_equals(value1, value2):
    value1_to_int = int(value1)
    value2_to_int = int(value2)
    is_equals = value1_to_int == value2_to_int
    return is_equals


# Definindo as colunas 
nf_df1 = "F"
name_df1 = "V"
value_df1 = "N"

nf_df2 = "B"
name_df2 = "G"
value_df2 = "F"


# Obtendo as planilhas
df1 = pd.read_excel(
    rf"{os. getcwd()}\planilha_1.xls", usecols=f"{nf_df1},{name_df1},{value_df1}"
).dropna(how='any')

df2 = pd.read_excel(
    rf"{os. getcwd()}\planilha_2.xlsx", usecols=f"{nf_df2},{name_df2},{value_df2}"
).dropna(how="any")


df1_size = df1.index.size
df2_size = df2.index.size


# Nota fiscal
def nf(table, index):
    value = table.at[index, table.columns[0]]
    return int(value)

# Valores da Nota fiscal
def nf_value(table, index):
    value = table.loc[index]
    return value





# for rows in range(0, df2_size):
#     invoice = df2.at[rows, df2.columns[0]]
#     invoice_to_int = int(invoice)
#     print(invoice_to_int)

print(df2)
print(df1)

# # verificar a existência dessa nota na tabela 2
# for ana in range(0, df2_size):
#     if nf(df1, 0) == nf(df2, df2_size):
#         print("have")
#         break

#     # pegar o número dessa nota
#     df1_rows = df1.index.stop


# for rows in range(0, df1_rows - 1):

#     nota = float(df1.loc[rows].at["Nota"])
#     existe = nota != "nan"

#     if existe:
#         print(rows, df1.loc[rows].at["Nota"])
