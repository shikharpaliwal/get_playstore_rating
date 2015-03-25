#!/usr/bin/env python

import re, urllib
from bs4 import BeautifulSoup
import gspread
import time

def get_current_rating(app_url):
	a = urllib.urlopen(app_url).read()
	soup = BeautifulSoup(a)
	bar_array = soup.findAll("span", { "class" : "bar-number" })

	current_cum_rating = []
	for elem in bar_array:
		current_cum_rating.insert(len(current_cum_rating),int(elem.string.replace(',','')))

	return current_cum_rating

def convert_to_column_name(num):
	col_name = ""
	divid = num
	modulo = 0
	while (divid > 0):
		modulo = divid % 26
		col_name = str(unichr(64+modulo)) + col_name
		divid = int((divid - modulo) / 26)

	return col_name

# to allow google to sign-in
# https://security.google.com/settings/security/activity?hl=en&pli=1
# http://www.google.com/accounts/DisplayUnlockCaptcha

#c1 = time.time()
print "Connecting to google spreadsheet"
#Opening the sheet
gc = gspread.login('adam.gil99@gmail.com', 'birthday@19111991')
spreadsheet_id = "1aeztLma8UhHZvxMQqRmUdTF3FKrL49o7kYPL5vliZzA"
wks = gc.open_by_key(spreadsheet_id).sheet1

columns_filled = len(wks.row_values(1))
current_date = time.strftime("%d/%m/%Y")

if current_date == wks.cell(1, columns_filled).value:
	print "Date already entered"
else:
	#c2 = time.time()
	print "Reading data from play store"
	#Getting present rating of TinyOwl
	tinyowl_ratings = get_current_rating("https://play.google.com/store/apps/details?id=com.flutterbee.tinyowl")
	zomato_ratings = get_current_rating("https://play.google.com/store/apps/details?id=com.application.zomato")
	foodpanda_ratings = get_current_rating("https://play.google.com/store/apps/details?id=com.global.foodpanda.android")
		
	print "Reading previous data from sheet"
	#c3 = time.time()

	current_column = columns_filled + 1

	#Reading previous tinyowl data
	t5 = int(wks.cell(11, columns_filled).value)
	t4 = int(wks.cell(12, columns_filled).value)
	t3 = int(wks.cell(13, columns_filled).value)
	t2 = int(wks.cell(14, columns_filled).value)
	t1 = int(wks.cell(15, columns_filled).value)

	#Reading previous zomato data
	z5 = int(wks.cell(29, columns_filled).value)
	z4 = int(wks.cell(30, columns_filled).value)
	z3 = int(wks.cell(31, columns_filled).value)
	z2 = int(wks.cell(32, columns_filled).value)
	z1 = int(wks.cell(33, columns_filled).value)

	#Reading previous zomato data
	f5 = int(wks.cell(47, columns_filled).value)
	f4 = int(wks.cell(48, columns_filled).value)
	f3 = int(wks.cell(49, columns_filled).value)
	f2 = int(wks.cell(50, columns_filled).value)
	f1 = int(wks.cell(51, columns_filled).value)	

	print "Completed reading"
	#c4 = time.time()
	#wks.update_cell(1, current_column, current_date)

	col = convert_to_column_name(current_column)
	print col
	cell_list = wks.range(col + '1:' + col + '53')

	new_values = [
			current_date, 
			"", 
			"", 
			tinyowl_ratings[0]-t5, 
			tinyowl_ratings[1]-t4, 
			tinyowl_ratings[2]-t3, 
			tinyowl_ratings[3]-t2, 
			tinyowl_ratings[4]-t1, 
			"", 
			"", 
			tinyowl_ratings[0], 
			tinyowl_ratings[1], 
			tinyowl_ratings[2], 
			tinyowl_ratings[3], 
			tinyowl_ratings[4], 
			"", 
			round((tinyowl_ratings[0]*5.0+tinyowl_ratings[1]*4+tinyowl_ratings[2]*3+tinyowl_ratings[3]*2+tinyowl_ratings[4]*1)/(tinyowl_ratings[0]+tinyowl_ratings[1]+tinyowl_ratings[2]+tinyowl_ratings[3]+tinyowl_ratings[4]),3), 
			"", 
			"", 
			"", 
			"", 
			zomato_ratings[0]-z5, 
			zomato_ratings[1]-z4, 
			zomato_ratings[2]-z3, 
			zomato_ratings[3]-z2, 
			zomato_ratings[4]-z1, 
			"", 
			"", 
			zomato_ratings[0], 
			zomato_ratings[1], 
			zomato_ratings[2], 
			zomato_ratings[3], 
			zomato_ratings[4], 
			"", 
			round((zomato_ratings[0]*5.0+zomato_ratings[1]*4+zomato_ratings[2]*3+zomato_ratings[3]*2+zomato_ratings[4]*1)/(zomato_ratings[0]+zomato_ratings[1]+zomato_ratings[2]+zomato_ratings[3]+zomato_ratings[4]),3), 
			"", 
			"", 
			"", 
			"", 
			foodpanda_ratings[0]-f5, 
			foodpanda_ratings[1]-f4, 
			foodpanda_ratings[2]-f3, 
			foodpanda_ratings[3]-f2, 
			foodpanda_ratings[4]-f1, 
			"", 
			"", 
			foodpanda_ratings[0], 
			foodpanda_ratings[1], 
			foodpanda_ratings[2], 
			foodpanda_ratings[3], 
			foodpanda_ratings[4], 
			"", 
			round((foodpanda_ratings[0]*5.0+foodpanda_ratings[1]*4+foodpanda_ratings[2]*3+foodpanda_ratings[3]*2+foodpanda_ratings[4]*1)/(foodpanda_ratings[0]+foodpanda_ratings[1]+foodpanda_ratings[2]+foodpanda_ratings[3]+foodpanda_ratings[4]),3), 
		]
	i = 0

	for cell in cell_list:
			cell.value = new_values[i]
			i += 1

	# Update in batch
	wks.update_cells(cell_list)

	#c5 = time.time()
	print "New entry created in spreadsheet"