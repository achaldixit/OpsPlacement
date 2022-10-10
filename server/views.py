from flask import  url_for, redirect, render_template
from server.forms import PropertyForm, PropertyForm2
from server import app
from dotenv import load_dotenv
from server.core_api.Location import Location
from server.property_api.Property import Property
from server.model import whl, cusl, runModel
import pandas as pd
import folium
import os
# from rpy2.robjects.conversion import localconverter as lc
# import rpy2
# from rpy2 import robjects
# from rpy2.robjects.packages import importr

load_dotenv()


@app.route('/', methods=['GET', 'POST'])
def index():
	# Location_obj = Location()
	# Location_obj.initialize()

	prop = Property()
	try:
		prop_data = prop.get_all_props()
	except:
		print("Property Data Could Not be fetched")
	prop_data = pd.json_normalize(prop_data)
	prop_data.head(5)

	# For some reason could not POST synthetic data to APIs
	# Using random data for POC.
	# Obtain the Lat-long and Pincodes of the Facilities in a given city
	# wh_locations = get_wh_locations() Using Property API and filtering by city
	# customer locations = obtain all the customer pincodes in the database filter by city

	form = PropertyForm()
	city = "Mumbai"
	if form.validate_on_submit():
		print("FORM SUBMIT")
		city = form.City.data
		infFactor = form.inflationFactor.data
		carting = form.Carting.data
		truckcost = form.TruckCost.data
		with open("model_params.txt", "w") as params:
			temp = "params\n" + str(city) + "\n" + str(infFactor) + "\n" + str(carting) + "\n" + str(truckcost)
			params.write(temp)
		
		os.system("python3 /Users/delhivery/Documents/Hackathons/OpsPlacement/server/model.py")
		# plotmodel()
		# Model ouput is pasted in here
		output = pd.read_csv("selected_warehouses.csv")

		# Create a map function
		itineraire = list(zip(output["y"], output["x"]))
		cus_marker = list(zip(cusl["y"], cusl["x"]))
		map = folium.Map((itineraire[0][1],itineraire[0][0]), zoom_start=10)
		for pt in itineraire:
			marker = folium.Marker([pt[1], pt[0]], icon=folium.Icon(color="green")) #latitude,longitude
			map.add_child(marker) 
		for pt in cus_marker:
			marker = folium.Marker([pt[1], pt[0]], icon=folium.Icon(color="red")) #latitude,longitude
			map.add_child(marker)
		map.save("map.html")
		return render_template('index.html', form1=form,m=map._repr_html_())

	if(city == "Mumbai"):
		itineraire = list(zip(whl["y"], whl["x"]))
	map = folium.Map((itineraire[0][1],itineraire[0][0]), zoom_start=10)
	for pt in itineraire:
		marker = folium.Marker([pt[1], pt[0]], icon=folium.Icon(color="lightgray"), 
								popup=folium.Popup(""),
								) #latitude,longitude
		map.add_child(marker) 
	map.save("map.html")
	return render_template('index.html', form1=form,m=map._repr_html_())

@app.route('/demo/', methods=['GET', 'POST'])
def demo():

	# For some reason could not POST synthetic data to APIs
	# Using random data for POC.
	# Obtain the Lat-long and Pincodes of the Facilities in a given city
	# wh_locations = get_wh_locations() Using Property API and filtering by city
	# customer locations = obtain all the customer pincodes in the database filter by city
	print("Hello")
	form = PropertyForm2()
	flag = True
	if form.validate_on_submit():
		flag = False
		infFactor = form.inflationFactor.data
		carting = form.Carting.data
		truckcost = form.TruckCost.data
		with open("model_params.txt", "w") as params:
			temp = "params\n"+"1"+ "\n" + str(infFactor) + "\n" + str(carting) + "\n" + str(truckcost)
			params.write(temp)
		
		os.system("python3 /Users/delhivery/Documents/Hackathons/OpsPlacement/server/dummy.py")
		# plotmodel()
		# Model ouput is pasted in here
		return render_template('demo.html', form1=form, flag = flag)
	return render_template('demo.html', form1=form, flag = flag)