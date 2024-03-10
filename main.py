from stock import *
from input import *

startrow = 10
startcoulumn = "B"
Filename = "GCI Positions (Live).xlsx"
sheet_name = "GCI Portfolio"


stonks = read_stocks_from_excel(Filename,sheet_name,startrow,startcoulumn, )

for STONK in stonks:
    print(STONK)




print("Ello")
