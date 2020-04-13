#!/usr/bin/python2
# -*- coding: utf-8 -*-


from time import sleep
import copy
import atexit
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import convertAccentCharutf8
from GlyphSprites import Sprites
import requests

lcd = Adafruit_CharLCDPlate()
atexit.register(lcd.stop)
lcd.backlight(True)

while (True):
  r = requests.get('http://192.168.1.101:25555/api/ets2/telemetry').json();

  truck = r['truck']
  navigation = r['navigation']

  speed = int(truck['speed'])
  speed_str = str(speed).rjust(3)

  gear = truck['displayedGear']

  gear_str = "-N-" if gear == 0 else "R" + str(-gear) if gear < 0 else "D" + str(gear)

  speed_limit = navigation['speedLimit']
  speed_limit_str = str(speed_limit).rjust(3)
  try:
    rpm_percent = int(truck['engineRpm']/truck['engineRpmMax']*100)
  except ZeroDivisionError:
    rpm_percent = 0

  rpm_percent_str = "RPM" + str(rpm_percent).rjust(3) + "%"

  try:
   fuel_percent = int(truck['fuel']/truck['fuelCapacity']*100)
  except ZeroDivisionError:
   fuel_percent = 0

  fuel_percent_str = "F" + str(fuel_percent).rjust(3) + "%"

  cruise_control_on = r['truck']['cruiseControlOn']
  cruise_control_speed = int(r['truck']['cruiseControlSpeed'])
  cruise_control_str = str(cruise_control_speed).rjust(3) if cruise_control_on else "OFF"


  lcd.clear()
  lcd.message("%s|%s|%s  %s\n%s   %s"%(speed_limit_str, speed_str, cruise_control_str, gear_str, fuel_percent_str, rpm_percent_str))
  sleep(0.2)
