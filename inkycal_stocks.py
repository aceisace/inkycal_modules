#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Stocks Module for Inky-Calendar Project

WIP
"""

#############################################################################
#                           Required imports (do not remove)
#############################################################################
# Required for setting up this module
from inkycal.modules.template import inkycal_module
from inkycal.custom import *


#############################################################################
#                           Built-in library imports
#############################################################################

# Built-in libraries go here

#############################################################################
#                         External library imports
#############################################################################

# For external libraries, which require installing,
# use try...except ImportError to check if it has been installed
# If it is not found, print a short message on how to install this dependency
try:
  import yfinance as yf
except ImportError:
  print('yfinance is not installed! Please install with:')
  print('pip3 install yfinance')


#############################################################################
#                         Filename + logging (do not remove)
#############################################################################

# Get the name of this file, set up logging for this filename
filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)
logger.setLevel(level=logging.INFO)

#############################################################################
#                         Class setup
#############################################################################

# info: you can change Simple to something else
# Please remember to keep the first letter a capital
# Avoid giving too long names to classes

class Stocks(inkycal_module):
  """ Stocks Class
  Explain what this module does...
  """

  # Initialise the class (do not remove)
  def __init__(self, section_size, section_config):
    """Initialize inkycal_rss module"""

    # Initialise this module via the inkycal_module template (required)
    super().__init__(section_size, section_config)

    # module name (required)
    self.name = self.__class__.__name__

    # module specific parameters (optional)
    self.do_something = True

    # give an OK message (optional)
    print('{0} loaded'.format(self.name))

#############################################################################
#                 Validation of module specific parameters                  #
#############################################################################

  def _validate(self):
    """Validate module-specific parameters"""
    # Check the type of module-specific parameters
    # This function is optional, but very useful for debugging.

    # Here, we are checking if do_something (from init) is True/False
    if not isinstance(self.do_something, bool):
      print('do_something has to be a boolean: True/False')


#############################################################################
#                       Generating the image                                #
#############################################################################

  def generate_image(self):
    """Generate image for this module"""

    # Define new image size with respect to padding (required)
    im_width = int(self.width - (self.width * 2 * self.margin_x))
    im_height = int(self.height - (self.height * 2 * self.margin_y))
    im_size = im_width, im_height

    # Use logger.info(), logger.debug(), logger.warning() to display
    # useful information for the developer
    logger.info('image size: {} x {} px'.format(im_width, im_height))

    # Create an image for black pixels and one for coloured pixels (required)
    im_black = Image.new('RGB', size = im_size, color = 'white')
    im_colour = Image.new('RGB', size = im_size, color = 'white')

    #################################################################
    
    parsed_tickers = []
    
    for ticker in tickers:         
          print('preparing data for {0}...'.format(ticker))

          yfTicker = yf.Ticker(ticker)

          try:
            stockInfo = yfTicker.info
            stockName = stockInfo['shortName']
          except Exception:
            stockName = ticker
            print('Error on getting ticker info! Using symbol as name.')

          stockHistory = yfTicker.history("2d")
          previousQuote = (stockHistory.tail(2)['Close'].iloc[0])
          currentQuote = (stockHistory.tail(1)['Close'].iloc[0])   
          currentGain = currentQuote-previousQuote       
          currentGainPercentage = (1-currentQuote/previousQuote)*-100

          tickerLine = '{}: {:.2f} {:+.2f} ({:+.2f}%)'.format(stockName, currentQuote, currentGain, currentGainPercentage)
          print('{}\n'.format(tickerLine))
          parsed_tickers.append(tickerLine)
    
    # Write/Draw something on the image
          
      """Write the correctly formatted text on the display"""
      for _ in range(len(parsed_tickers)):
        write(parsed_tickers[_])

      del parsed_tickers

    #   You can use these custom functions to help you create the image:
    # - write()               -> write text on the image
    # - get_fonts()           -> see which fonts are available
    # - get_system_tz()       -> Get the system's current timezone
    # - auto_fontsize()       -> Scale the fontsize to the provided height
    # - textwrap()            -> Split a paragraph into smaller lines
    # - internet_available()  -> Check if internet is available
    # - draw_border()         -> Draw a border around the specified area

    # If these aren't enough, take a look at python Pillow (imaging library)'s
    # documentation.

    
    #################################################################

    # Save image of black and colour channel in image-folder
    im_black.save(images+self.name+'.png', 'PNG')
    im_colour.save(images+self.name+'_colour.png', 'PNG')


# Check if the module is being run by itself
if __name__ == '__main__':
  print('running {0} in standalone mode'.format(filename))




################################################################################
# Last steps
# Wow, you made your own module for the inkycal project! Amazing :D
# To make sure this module can be used with inkycal, you need to edit 2 files:

# 1) Inkycal/modules/__init__.py
# Add this into the modules init file:
# from .filename import Class
# where filename is the name of your module
# where Class is the name of your class e.g. Simple in this case


# 2) Inkycal/__init__.py
# Before the line # Main file, add this:
# import inkycal.modules.filename
# Where the filename is the name of your file inside the modules folder

# How do I now import my module?
# from inkycal.modules import Class
# Where Class is the name of the class inside your module (e.g. Simple)
  
