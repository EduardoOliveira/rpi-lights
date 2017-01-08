from flask import Flask
from flask import request
from flask import Response

import time
import pigpio
import copy

pi = pigpio.pi()

app = Flask(__name__)

pins={"r":17,"g":22,"b":24}
state={"r":0,"g":0,"b":0}

power_value=True


def set_colors(colors={},merge=True):
   global state

   for key, value in colors.iteritems():
      #if value:
      state[key]=int(value)
  # else:
  #    state=colors

def light(colors={}, merge=True):
   values = copy.copy(state)

#   if merge:
   for key, value in colors.iteritems():
      print value
      if value or (int(value) ==0):
         print value
         values[key]=int(value)
 #  else:
 #     for key,value in state.iteritems():
 #        if value or (int(value) ==0):
 #           print value
 #           colors[key]=value
 #        else:
 #           colors[key]=0

   for key, value in values.iteritems():
      print values[key]
      pi.set_PWM_dutycycle(pins[key], int(values[key]))

@app.route("/power")
def power():
   global power

   if request.args.get('power'):
      power = request.args.get('power') == "True"
   if(power):
      light()
   else:
      if request.args.get('r'):
         set_colors({"r":0,"g":0,"b":0})     
      light({"r":0,"g":0,"b":0})     


   return Response(str(power),mimetype='text/plain')


@app.route("/red")
def red():

   if request.args.get('level'):
      set_colors({"r":int(request.args.get('level'))})
   light()

   return Response(str(state["r"]),mimetype='text/plain')

@app.route("/blue")
def blue():

   if request.args.get('level'):
      set_colors({"b":int(request.args.get('level'))})
   light()

   return Response(str(state["b"]),mimetype='text/plain')

@app.route("/green")
def green():

   if request.args.get('level'):
      set_colors({"g":int(request.args.get('level'))})
   light()

   return Response(str(state["g"]),mimetype='text/plain')

@app.route("/light")
def light_up():
 
   if request.args.get("merge") and (request.args.get("merge")=="False"):
      merge=False
   else:
      merge=True   


   light({"r":request.args.get("r"),"g":request.args.get("g"),"b":request.args.get("b")},merge)

   if request.args.get("save"):
      set_colors({"r":request.args.get("r"),"g":request.args.get("g"),"b":request.args.get("b")},merge)

   return Response(request.args,mimetype='application/json')

@app.route("/warning")
def warning():
   light({"r":0,"g":0,"b":0},False)   

   x=0
   for x in range(0,6):
      light({"r":255},False)
      time.sleep(0.1)
      light({"r":0,"g":0,"b":0},False)
      time.sleep(0.1)
   if power:
      light()

   return Response("ok",mimetype='text/plain')   


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    pi.stop()
