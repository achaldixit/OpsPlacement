from flask import  url_for, redirect, render_template
from server.forms import PropertyForm
from server import app
from dotenv import load_dotenv
from server.core_api.Location import Location
from server.property_api.Property import Property
from server.model import MipModel, GetGraph, whl, cusl, runModel, plotmodel
import pandas as pd
import folium

load_dotenv()


@app.route('/', methods=['GET', 'POST'])
def index():
	# Location_obj = Location()
	# Location_obj.initialize()
	
	flag = True

	prop = Property()
	try:
		prop_data = prop.get_all_props()
	except:
		print("Property Data Could Not be fetched")
	prop_data = pd.json_normalize(prop_data)
	prop_data.head(5)
	# prop_
	# Obtain the Lat-long and Pincodes of the Facilities in a given city

	print(whl)
	form = PropertyForm()
	city = "Mumbai"
	if form.validate_on_submit():
		flag = False
		city = form.City.data
		infFactor = form.inflationFactor.data
		capacity = form.Capacity.data
		truckcost = form.TruckCost.data
		runModel()
		plotmodel()
		output = pd.read_csv("matching.csv")
		print(output)

	if flag :
		if(city == "Mumbai"):
			itineraire = list(zip(whl["plong"], whl["plat"]))
		map = folium.Map((itineraire[0][1],itineraire[0][0]), zoom_start=10)
		for pt in itineraire:
			marker = folium.Marker([pt[1], pt[0]]) #latitude,longitude
			map.add_child(marker) 
		map.save("map.html")
		return render_template('index.html', form1=form,m=map._repr_html_())
	return render_template('index.html', form1=form)
