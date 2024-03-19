from stock import *
from input import *

startrow = 10
startcoulumn = "B"
Filename = "GCI Positions (Live).xlsx"
sheet_name = "GCI Portfolio"


stonks = read_stocks_from_excel(Filename,sheet_name,startrow,startcoulumn, )

for STONK in stonks: # kinda sec(c) tbh
    print(STONK)

# below will be our goals:
'''
1) determine presentable data output form -- james
2) determine portfolio class -- ryan
3) value-at-risk function -- mruds
'''


print("Ello")
