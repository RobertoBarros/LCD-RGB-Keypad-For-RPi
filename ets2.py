#!/usr/bin/python2
# -*- coding: utf-8 -*-


from time import sleep
import copy
import atexit
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from GlyphSprites import Sprites
import requests
import dateutil.parser

lcd = Adafruit_CharLCDPlate()
atexit.register(lcd.stop)
lcd.backlight(True)
lcd.createChar(0, Sprites.bar0)
lcd.createChar(1, Sprites.bar1)
lcd.createChar(2, Sprites.bar2)
lcd.createChar(3, Sprites.bar3)
lcd.createChar(4, Sprites.bar4)

while (True):
  r = requests.get('http://192.168.1.101:25555/api/ets2/telemetry').json();

  truck = r['truck']
  navigation = r['navigation']
  game = r['game']

  speed = int(truck['speed'])
  speed_str = str(speed).rjust(3)

  gear = truck['displayedGear']

  gear_str = "-N-" if gear == 0 else "R" + str(-gear) if gear < 0 else "D" + str(gear)

  speed_limit = navigation['speedLimit']
  speed_limit_str = str(speed_limit).rjust(3)

  if speed < speed_limit:
    color = lcd.GREEN
  elif speed >= speed_limit and speed < speed_limit + (speed_limit * 0.1):
    color = lcd.YELLOW
  else:
    color = lcd.RED

  try:
    rpm_percent = int(truck['engineRpm']/truck['engineRpmMax']*100)
  except ZeroDivisionError:
    rpm_percent = 0
  # rpm_percent_str = "RPM" + str(rpm_percent).rjust(3) + "%"

  rpm_str = '\x00' if rpm_percent > 50 else ''
  rpm_str = '\x00\x01' if rpm_percent > 60 else rpm_str
  rpm_str = '\x00\x01\x02' if rpm_percent > 70 else rpm_str
  rpm_str = '\x00\x01\x02\x03' if rpm_percent > 80 else rpm_str
  rpm_str = '\x00\x01\x02\x03\x04' if rpm_percent > 90 else rpm_str

  try:
   fuel_percent = int(truck['fuel']/truck['fuelCapacity']*100)
  except ZeroDivisionError:
   fuel_percent = 0

  # Only 2 chars for fuel
  if fuel_percent >= 100:
    fuel_percent = 99

  fuel_percent_str = "F" + str(fuel_percent).rjust(2) + "%"

  cruise_control_on =truck['cruiseControlOn']
  cruise_control_speed = int(truck['cruiseControlSpeed'])
  cruise_control_str = str(cruise_control_speed).rjust(3) if cruise_control_on else "OFF"



  current_time = dateutil.parser.parse(game['time'])
  rest_time = dateutil.parser.parse(game['nextRestStopTime'])
  # seconds_until_stop = (current_time - rest_time).total_seconds()
  # hours_until_stop = int(seconds_until_stop // 3600)
  # minutes_until_stop = int(seconds_until_stop % 3600) // 60

  time_until_stop_str = str(rest_time.hour).zfill(2) + ':' + str(rest_time.minute).zfill(2)


  lcd.clear()
  lcd.message("%s|%s|%s  %s\n%s %s %s"%(cruise_control_str, speed_limit_str, speed_str, gear_str, fuel_percent_str, time_until_stop_str, rpm_str))
  lcd.ledRGB(color)
  sleep(0.1)
