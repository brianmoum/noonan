import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os
import sys
from pylab import plot, show, savefig, xlim, figure, ylim, legend, boxplot, setp, axes

def csvToDataframe(file) :
	data = pd.read_csv(file, dtype='string')
	data_top = data.head()
	return data

def getClubAverages(date_range, lie_type) :
	clubAverages = pd.DataFrame(columns=["Club ID", "Club Name", "Q1", "Q2", "Q3"])


def setBoxColors(bp):
	setp(bp['boxes'][0], color='blue')
	setp(bp['caps'][0], color='blue')
	setp(bp['caps'][1], color='blue')
	setp(bp['whiskers'][0], color='blue')
	setp(bp['whiskers'][1], color='blue')
	setp(bp['fliers'][0], color='blue')
	#setp(bp['fliers'][1], color='blue')
	setp(bp['medians'][0], color='blue')

	setp(bp['boxes'][1], color='red')
	setp(bp['caps'][2], color='red')
	setp(bp['caps'][3], color='red')
	setp(bp['whiskers'][2], color='red')
	setp(bp['whiskers'][3], color='red')
	setp(bp['fliers'][1], color='red')
	#setp(bp['fliers'][3], color='red')
	setp(bp['medians'][1], color='red')

	setp(bp['boxes'][2], color='black')
	setp(bp['caps'][4], color='black')
	setp(bp['caps'][5], color='black')
	setp(bp['whiskers'][4], color='black')
	setp(bp['whiskers'][5], color='black')
	setp(bp['fliers'][2], color='black')
	#setp(bp['fliers'][5], color='black')
	setp(bp['medians'][2], color='black')


def clubDistanceGraph(shot_data, club_data, lie_types, lie_ratings_in_scope=['standard', 'difficult', 'extreme'], club_types=['Wood', 'Hybrid', 'Iron', 'Wedge']) :

	## Final graph will be groups of boxplots for each club, where the group is the distribution of that club for each selected lie. This attribute determines the number of plots per club (e.g. only standard means this value is 1, all lies means this value is 3)
	club_graph_width = len(lie_ratings_in_scope)
	## Initializing the number of "groups" in the final graph. This wvalue willbe set in the loop below by finding all clubs which are both active and within the selected club types.
	club_count = 0
	## Initializing the data dictionary that will drive the graph
	club_graph_data ={}

	shot_data = shot_data.join(club_data.set_index('id'), on='shot_club_id')
	shot_data = shot_data.join(lie_types.set_index('id'), on='shot_lie_id')
	pd.set_option('display.max_columns', None)
	print(shot_data.head())

	## Looping through all clubs to set club_count, and to also create the hashmap structure for the graph_data
	for index, row in club_data.iterrows() :
		if row['club_type'] in club_types and row['club_active'] :
			club_count += 1
			club_graph_data[row['club_symbol']] = {}
			for lie in lie_ratings_in_scope :
				club_graph_data[row['club_symbol']][lie] =[]


	print(club_graph_data)

	for index, row in shot_data.iterrows() :

		## Skips shot if on the green, or if record is for a shot that went out of bounds
		if row['shot_lie_id'] not in (8, 9, 10) and index < len(shot_data)-1:
			row2 = shot_data.iloc[index+1]

			## Skips calculating shot distace if next shot is a tee shot. This shouldn't be an issue in most cases since ideally user is putting on the shot before a tee shot and would be skipped by above condition, but this covers edge cases where holes are surrendered before puttig, etc.
			if row2['shot_number_hole'] != 1 :

				## Only performing calculations and adding data points if the club used was within the specified club types
				if row['club_type'] in club_types :

					shot_distance = int(row['shot_distance_to_green']) - int(row2['shot_distance_to_green'])
					if shot_distance > 200 and row['club_type'] not in ['Wood', 'Hybrid'] :
						print("Abnormal Shot Distance: {1}: {0}".format(shot_distance, row['club_symbol']))
						print(row)
						print(row2)
					club_graph_data[row['club_symbol']][row['lie_type']].append(shot_distance)


	print(club_graph_data)

	## Creating Graph
	fig = figure()
	ax = axes()
	hold = True

	pos = 1

	#bp = boxplot([club_graph_data["5I"]['standard'], club_graph_data["5I"]['difficult'], club_graph_data["5I"]['extreme']], positions=[1, 3, 5], widths = 0.6)
	bp = boxplot([[175,220,200,210,165,100,155,185,195,160,170,120,100,20,30,195,225], [135,145,120,110,45,20,150,170,160,150,120,55,65,20,100], [50,60,50,45,75,100,55,75,90,80,40,20,10,10,10]], positions=[1, 2, 3], widths = 0.6)
	setBoxColors(bp)


	# set axes limits and labels
	ylim(0,250)
	#ax.set_xticklabels("standard", "difficult", "extreme")

	# draw temporary red and blue lines and use them to create a legend
	hBlu, = plot([1,1],'b-')
	hRed, = plot([1,1],'r-')
	hBlk, = plot([1,1],'k-')
	legend((hBlu, hRed, hBlk),('Standard', 'Difficult', 'Extreme'))
	hBlu.set_visible(False)
	hRed.set_visible(False)
	hBlk.set_visible(False)


	savefig('boxcompare.png')
	show()


def main() :
	shots = csvToDataframe("test_data/noonan_test_shots.csv")
	rounds = csvToDataframe("test_data/noonan_test_rounds.csv")
	lie_types = csvToDataframe("test_data/noonan_test_lie_types.csv")
	clubs = csvToDataframe("test_data/noonan_test_clubs.csv")


	#getClubAverages("all", "standard")

	clubDistanceGraph(shots, clubs, lie_types, club_types=["Iron"])


main()