import time
import random
class FlowMeter():
  PINTS_IN_A_LITER = 2.11338
  SECONDS_IN_A_MINUTE = 60
  MS_IN_A_SECOND = 1000.0
  displayFormat = 'america'
  beverage = 'beer'
  enabled = True
  clicks = 0
  lastClick = 0
  clickDelta = 0
  hertz = 0.0
  flow = 0 # in oz per second
  currPour = 0.0 # in oz
  totalPour = 0.0 # in oz

  def __init__(self, displayFormat, beverage):
    self.displayFormat = displayFormat
    self.beverage = beverage
    self.clicks = 0
    self.lastClick = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    self.clickDelta = 0
    self.hertz = 0.0
    self.flow = 0.0
    self.currPour = 0.0
    self.totalPour = 0.0
    self.enabled = True

  def update(self, currentTime):
    self.clicks += 1
    # get the time delta
    self.clickDelta = max((currentTime - self.lastClick), 1)
    # calculate the instantaneous speed
    if (self.enabled == True and self.clickDelta < 1000):
      self.hertz = FlowMeter.MS_IN_A_SECOND / self.clickDelta
      self.flow = self.hertz / (FlowMeter.SECONDS_IN_A_MINUTE * 7.5 / 33.81413)  # In oz per second
      instPour = self.flow * (self.clickDelta / FlowMeter.MS_IN_A_SECOND)  
      self.currPour += instPour
      self.totalPour += instPour
    # Update the last click
    self.lastClick = currentTime

  def getFormattedCurrPour(self):
    if(self.displayFormat == 'america'):
      return str(round(self.currPour,3)) + ' oz'
    else:
      return str(round(self.currPour * FlowMeter.PINTS_IN_A_LITER, 3)) + ' pints'
  
  def getFormattedTotalPour(self):
    if(self.displayFormat == 'america'):
      return str(round(self.totalPour,3)) + ' oz'
    else:
      return str(round(self.totalPour * FlowMeter.PINTS_IN_A_LITER, 3)) + ' pints'

  def clearCurrPour(self):
    self.currPour = 0;

  def clearTotalPour(self):
    self.totalPour = 0;
