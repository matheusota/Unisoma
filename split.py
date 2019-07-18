import xlrd
import csv
from datetime import time

def convertTime(x):
	x = int(x * 24 * 3600) # convert to number of seconds
	hours = x//3600
	minutes = (x%3600) // 60

	# rounding errors
	if minutes == 59:
		minutes = 0
		hours += 1
	elif (minutes % 10) == 9:
		minutes += 1
	elif (minutes % 10) == 1:
		minutes -= 1
	
	if minutes == 0:
		return str(hours) + ":00"
	else:
		return str(hours) + ":" + str(minutes)

wb = xlrd.open_workbook('Modelo de Dados_CCP_v1.xlsx')

for i in range(wb.nsheets):
	sheet = wb.sheet_by_index(i)
	print(sheet.name)
	
	with open("data/" + sheet.name.replace(" ", "") + ".csv", "w") as file:
		writer = csv.writer(file, delimiter = ",")
		header = [cell.value for cell in sheet.row(0)]
		print(header)
		writer.writerow(header)

		for row_idx in range(1, sheet.nrows):
			row = []
			
			for cell in sheet.row(row_idx):
				if type(cell.value) == float:
					if cell.value.is_integer():
						row.append(int(cell.value))
					else:
						row.append(convertTime(cell.value))
				else:
					row.append(cell.value)
				
			writer.writerow(row)
