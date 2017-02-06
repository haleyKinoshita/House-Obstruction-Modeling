import requests, os

from PIL import Image

from io import BytesIO

from flask import Flask, render_template, jsonify, send_file



from tempfile import NamedTemporaryFile

from shutil import copyfileobj



import pymysql

import matplotlib.pyplot as plt, mpld3

import numpy as np

import pandas as pd

from mpld3 import plugins

import json

conn = pymysql.connect(host='us-cdbr-azure-west-b.cleardb.com', port=3306, user='b60dd1c4108b4a', passwd='ad336811',db='corecogic_grand_challenge',autocommit=True)





app = Flask(__name__)



street_view_api = "&key=AIzaSyD2tkW4mIk43yCsMagAzqBsZEN3L2fp6xs"



@app.route("/", methods=["GET"])

def retreive():

    return render_template('map.html')



@app.route("/streetView/<string:address>")

def get_results(address):



  for i in range(0,4):

    heading = i * 90

    base = "https://maps.googleapis.com/maps/api/streetview?&heading={0}&fov=120&size=1200x800&location=".format(heading)

    MyUrl = base + address + street_view_api

    x = requests.get(MyUrl)

    image = Image.open(BytesIO(x.content))



    image.save("static/" + address + "_heading=" + str(heading) + ".jpg")



  return '/static/' + address + "_heading"



@app.route("/getHazards/<string:address>")

def get_hazards(address):

  house_data = {}

  address = address.split(',')

  address = address[0].split()

  address[-1] = address[-1][0]

  address = ' '.join(address)

  address = address.upper()



  cur = conn.cursor()

  cur.execute("select * from houseinfo where Address like \'{0}%\'".format(address))

  #(HouseID,Latitude,Longitude,Address,Elevation,Hazards) where first_name=? and last_name=? and access_code=?", [credentials[0],credentials[1],credentials[2]]

  rv = cur.fetchall()

  house_data['house'] = {}

  house_data['house']['lat_long'] = [round(rv[0][1],5),round(rv[0][2],5)]

  house_data['house']['elevation'] = round(rv[0][4],2)

  house_data['house']['hazards'] = rv[0][5]

  print(house_data)

  cur.close()



  return json.dumps(house_data)



@app.route("/get_house_elevation/<string:address>")

def get_house_elevation(address):



  cur = conn.cursor()

  cur.execute("select Latitude,Longitude,Elevation from houseinfo where Address=\'{0}\'".format(address))

  #(HouseID,Latitude,Longitude,Address,Elevation,Hazards) where first_name=? and last_name=? and access_code=?", [credentials[0],credentials[1],credentials[2]]

  rv = cur.fetchall()

  print(address,rv)

  print(rv[0][0])

  cur.close()



  return str(rv[0][0])+'|'+str(rv[0][1])+'|'+str(rv[0][2])

if __name__ ==  "__main__":

  app.run(debug="True")

  conn.close()
