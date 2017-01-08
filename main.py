from flask import Flask
from flask import request
from flask import Response

import time
import pigpio

pi = pigpio.pi()

app = Flask(__name__)
red_value=0
green_value=0
blue_value=0
power_value=True

@app.route("/power")
def power():

   global red_value
   global green_value
   global blue_value
   
   if request.args.get('power'):
      power = request.args.get('power') == "True"
   if(power):
      pi.set_PWM_dutycycle(17, red_value)
      pi.set_PWM_dutycycle(22, green_value)
      pi.set_PWM_dutycycle(24, blue_value)
   else:
      if request.args.get('r'):
         red_value=0
         green_value=0
         blue_value=0
      pi.set_PWM_dutycycle(17, 0)
      pi.set_PWM_dutycycle(22, 0)
      pi.set_PWM_dutycycle(24, 0)
     

   return Response(str(power),mimetype='text/plain')


@app.route("/red")
def red():
   global red_value
   if request.args.get('level'):
      red_value = int(request.args.get('level'))   
   pi.set_PWM_dutycycle(17, red_value)

   return Response(str(red_value),mimetype='text/plain')

@app.route("/blue")
def blue():
   global blue_value
   if request.args.get('level'):
      blue_value = int(request.args.get('level'))
   pi.set_PWM_dutycycle(24, blue_value)

   return Response(str(blue_value),mimetype='text/plain')

@app.route("/green")
def green():
   global green_value
   if request.args.get('level'):
      green_value = int(request.args.get('level'))
   pi.set_PWM_dutycycle(22, green_value)

   return Response(str
(green_value),mimetype='text/plain')

@app.route("/warning")
def warning():
   pi.set_PWM_dutycycle(17, 0)
   pi.set_PWM_dutycycle(22, 0)
   pi.set_PWM_dutycycle(24, 0)

   x=0
   for x in range(0,6):
      pi.set_PWM_dutycycle(17, 255)
      time.sleep(0.1)
      pi.set_PWM_dutycycle(17, 0)
      time.sleep(0.1)

   pi.set_PWM_dutycycle(17, red_value)
   pi.set_PWM_dutycycle(22, green_value)
   pi.set_PWM_dutycycle(24, blue_value)

   return Response("ok",mimetype='text/plain')   


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    pi.stop()
