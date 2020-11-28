#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tweets Module for Inky-Calendar Project

by https://github.com/worstface
"""
from inkycal.modules.template import inkycal_module
from inkycal.custom import *

try:
  import twint
except ImportError:
  print('twint is not installed! Please install with:')
  print('pip3 install twint')
  
try:
  import qrcode
except ImportError:
  print('qrcode is not installed! Please install with:')
  print('pip3 install qrcode[pil]')

filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)

class Tweets(inkycal_module):

  name = "Tweets - Displays Twitter tweets"

  # required parameters
  optional = {

    "username": {
        "label": "username to show tweets of "               
        },
    "search": {
        "label": "search term to show tweets of "               
        },
    "minlikes": {
        "label": "You can display any information by using "               
        }              
    }

  def __init__(self, config):

    super().__init__(config)

    config = config['config']
   
    self.username = config['username']
    self.search = config['search']
    self.minlikes = config['minlikes']

    # give an OK message
    print(f'{filename} loaded')
    
  def generate_image(self):
    """Generate image for this module"""
    
    def human_format(num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    # Define new image size with respect to padding
    im_width = int(self.width - (2 * self.padding_left))
    im_height = int(self.height - (2 * self.padding_top))
    im_size = im_width, im_height
    logger.info('image size: {} x {} px'.format(im_width, im_height))

    # Create an image for black pixels and one for coloured pixels (required)
    im_black = Image.new('RGB', size = im_size, color = 'white')
    im_colour = Image.new('RGB', size = im_size, color = 'white')

    # Check if internet is available
    if internet_available() == True:
      logger.info('Connection test passed')
    else:
      raise Exception('Network could not be reached :/')

    # Set some parameters for formatting feeds
    line_spacing = 1
    line_height = self.font.getsize('hg')[1] + line_spacing
    line_width = im_width
    max_lines = (im_height // (self.font.getsize('hg')[1] + line_spacing))

    logger.debug(f"max_lines: {max_lines}")

    # Calculate padding from top so the lines look centralised
    spacing_top = int( im_height % line_height / 2 )

    # Calculate line_positions
    line_positions = [
      (0, spacing_top + _ * line_height ) for _ in range(max_lines)]

    logger.debug(f'line positions: {line_positions}')
      
    logger.info(f'preparing twint configuration...')
    twintConfig = twint.Config()  
    
    if self.username:
        twintConfig.Username = self.username
    if self.search:
        twintConfig.Search = self.search
    if self.minlikes:    
        twintConfig.Min_likes = self.minlikes
        
    twintConfig.Limit = 20
    twintConfig.Store_object = True
    twintConfig.Hide_output = True

    logger.info(f'running twint search...')
    twint.run.Search(twintConfig)
    tweets = twint.output.tweets_list
    
    logger.info(f'preparing tweet image...')
    tweet_lines = []
    tweet_lines_colour = []
    
    lastTweet = tweets[0]
    
    tweetHeader = '{} @{}·{}'.format(lastTweet.name, lastTweet.username, lastTweet.timestamp)
    tweetText = '"{}"'.format(lastTweet.tweet)
    
    tweet_lines.append(tweetHeader)
    tweet_lines.append(tweetText)
    
    tweet_lines_colour.append(tweetHeader)
    
    textSpace = Image.new('RGBA', (528, 100), (255,255,255,255))
    materialFont = ImageFont.truetype(fonts['MaterialIcons-Regular'], size = 24)       
    
    ImageDraw.Draw(textSpace).text((100, 57), '\ue0cb', fill='black', font=materialFont)
    ImageDraw.Draw(textSpace).text((128, 54), human_format(lastTweet.replies_count), fill='black', font=self.font)
        
    ImageDraw.Draw(textSpace).text((200, 56), '\ue86a', fill='black', font=materialFont)
    ImageDraw.Draw(textSpace).text((228, 54), human_format(lastTweet.retweets_count), fill='black', font=self.font)
    
    ImageDraw.Draw(textSpace).text((300, 56), '\ue83a', fill='black', font=materialFont)
    ImageDraw.Draw(textSpace).text((328, 54), human_format(lastTweet.likes_count), fill='black', font=self.font) 

    im_black.paste(textSpace)
    im_colour.paste(textSpace)    
    
    logger.info(f'generating qr code...')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=4)
        
    qr.add_data(lastTweet.link)
    
    qrImage = qr.make_image(fill_color="black", back_color="white")
    qrSpace = Image.new('RGBA', (528, 100), (255,255,255,255))
    qrSpace.paste(qrImage,(430,0))
    im_black.paste(qrSpace)

    # Write/Draw something on the black image   
    for _ in range(len(tweet_lines)):
      if _+1 > max_lines:
        logger.error('Ran out of lines for parsed_ticker_colour')
        break
      write(im_black, line_positions[_], (line_width, line_height),
              tweet_lines[_], font = self.font, alignment= 'left')    

    # Write/Draw something on the colour image
    for _ in range(len(tweet_lines_colour)):
      if _+1 > max_lines:
        logger.error('Ran out of lines for parsed_tickers_colour')
        break
      write(im_colour, line_positions[_], (line_width, line_height),
              tweet_lines_colour[_], font = self.font, alignment= 'left')    

    # Save image of black and colour channel in image-folder
    return im_black, im_colour

if __name__ == '__main__':
  print(f'running {filename} in standalone/debug mode')