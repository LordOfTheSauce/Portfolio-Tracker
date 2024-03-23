from stock import *
from input import *

startrow = 10
startcoulumn = "C"
Filename = "GCI Positions (Live).xlsx"
sheet_name = "GCI Portfolio"


portfolio = read_stocks_from_excel(Filename,sheet_name,startrow,startcoulumn)
portfolio.print_stocks()
portfolio.summary()




