from flask import Flask, render_template, request, Response

import pigpio
import time

from thread import start_new_thread

app = Flask(__name__)

CurrentColour = "White"

RedColourCode = 0
BlueColourCode = 0
GreenColourCode = 0
RedBeforeEffect = 0
BlueBeforeEffect = 0
GreenBeforeEffect = 0
RedPin = 17
BluePin = 22
GreenPin = 24

pi = pigpio.pi()

@app.route('/', methods=['GET'])
def Main():
	global CurrentColour
	if request.args.get('Colour'):
		CurrentColour=request.args.get('Colour')
		ApplyColor()
		return Response("ok",mimetype='text/plain')

	if request.args.get('Warning'):
		start_new_thread(FireWarning,())
		return Response("ok",mimetype='text/plain')

	return render_template('index.html')
 

def ApplyColor():
	print CurrentColour
	if CurrentColour == "White":
		FadeTORGB(255,255,255)

	elif CurrentColour == "Red":
		FadeTORGB(255,0,0)

	elif CurrentColour == "Green":
		FadeTORGB(0,255,0)

	elif CurrentColour == "DarkBlue":
		FadeTORGB(0,0,255)

	elif CurrentColour == "LightBlue":
		FadeTORGB(0,255,255)

	elif CurrentColour == "Orange":
		FadeTORGB(255,15,0)

	elif CurrentColour == "Pink":
		FadeTORGB(255,0,192)

	elif CurrentColour == "Yellow":
		FadeTORGB(255,157,0)

	elif CurrentColour == "Purple":
		FadeTORGB(123,0,255)

	elif CurrentColour == "Black":
		FadeTORGB(0,0,0)
	

def FireWarning():
	FadeTORGB(0,0,0)
	for x in range(0,6):
		FadeTORGB(255,0,0)
		time.sleep(0.1)
		FadeTORGB(0,0,0)
		time.sleep(0.1)
	ApplyColor()		
	
        
        	
def FadeTORGB(RedNum,BlueNum,GreenNum):
    start_new_thread(FadeUpRed,(RedNum,))
    start_new_thread(FadeUpBlue,(BlueNum,))
    start_new_thread(FadeUpGreen,(GreenNum,))

def FadeUpRed(REDUpNum):
    global RedColourCode
    if RedColourCode < REDUpNum:
        while RedColourCode < REDUpNum:
            RedColourCode +=1
            pi.set_PWM_dutycycle(RedPin, RedColourCode)
    elif RedColourCode > REDUpNum:
        while RedColourCode > REDUpNum:
            RedColourCode -=1
            pi.set_PWM_dutycycle(RedPin, RedColourCode)


def FadeUpBlue(BlueUpNum):
    global BlueColourCode
    if BlueColourCode < BlueUpNum:
        while BlueColourCode < BlueUpNum:
            BlueColourCode +=1
            pi.set_PWM_dutycycle(BluePin, BlueColourCode)
    elif BlueColourCode > BlueUpNum:
        while BlueColourCode > BlueUpNum:
            BlueColourCode -=1
            pi.set_PWM_dutycycle(BluePin, BlueColourCode)

def FadeUpGreen(GreenUpNum):
    global GreenColourCode
    if GreenColourCode < GreenUpNum:
        while GreenColourCode < GreenUpNum:
            GreenColourCode +=1
            pi.set_PWM_dutycycle(GreenPin, GreenColourCode)
    elif GreenColourCode > GreenUpNum:
        while GreenColourCode > GreenUpNum:
            GreenColourCode -=1
            pi.set_PWM_dutycycle(GreenPin, GreenColourCode)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

