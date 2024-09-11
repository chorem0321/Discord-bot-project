import pandas as pd
import openpyxl as op
from discord.ext import commands

#출석체크
file_name = "matrix_bot\m_registrations.xlsx"
wb = op.load_workbook(file_name)
ws = wb["출석체크"]
print(ws.cell(row=1, column=2).value)