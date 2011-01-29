import htmlentitydefs
import re
from datetime import datetime
from email.utils import parsedate

PLUGIN_TITLE               = 'PokerStars.tv'
PLUGIN_PREFIX              = '/video/pokerstars-tv'

# URLS
BASE_URL                   = 'http://www.pokerstars.tv'
CHANNELS_URL               = '%s/poker-channels' % BASE_URL
SCHEDULE_URL               = '%s/docs-pokerstarstv-schedule.html' % BASE_URL

# Default artwork and icon(s)
PLUGIN_ARTWORK             = 'art-default.png'
PLUGIN_ICON_DEFAULT        = 'icon-default.png'

###############################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, L('pokerstars.tv'), PLUGIN_ICON_DEFAULT, PLUGIN_ARTWORK)
  Plugin.AddViewGroup('Channels', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('ChannelDetails', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('ChannelVideos', viewMode='InfoList', mediaType='items')
  HTTP.CacheTime = CACHE_1HOUR

###################################################################################################
# MENUS
###################################################################################################
def MainMenu():
  dir = MediaContainer(title1=PLUGIN_TITLE,viewGroup='Channels')
  dir.Append(
    Function( DirectoryItem( Spotlight, 'Spotlight', thumb=R(PLUGIN_ICON_DEFAULT) ) )
  )
  
  channels = HTML.ElementFromURL( CHANNELS_URL, errors='ignore').xpath('//*/div[@id="template"]/ul/li/div[@class="content clearfix"]/a[@class="logo"]')
  for channel in channels:
    url      = channel.get('href')
    img      = channel.xpath('.//img')
    name     = img[0].get('alt').replace(' logo', '')
    thumb_url = img[0].get('src')
    # Log( url )
    # Log( name )
    # Log( thumb_url ) 
    dir.Append(
      Function(
        DirectoryItem( 
          ChannelDetails,
          name,
          thumb=Function(GetThumb, thumb_url=thumb_url)
        ),
        url=url,
        name=name,
        thumb_url=thumb_url
      )
    )
  return dir
  
###################################################################################################
def ChannelDetails(sender,url,name,thumb_url):
  dir = MediaContainer(title1=L('pokerstars.tv'),title2=name,viewGroup='ChannelDetails')
  # url = url.replace('-2.html', '-full-episodes.html')
  # Log( 'Getting episodes from: ' + BASE_URL + url )
  # episodes = HTML.ElementFromURL( BASE_URL + url ).xpath()
  the_url = BASE_URL + url
  # Log( 'Getting details from: ' + the_url )
  sections = HTML.ElementFromURL(the_url, errors='ignore').xpath('//*/div[@id="template"]/div[@id="clm-one"]/div/ul/li/a')
  for section in sections:
    url          = section.get('href')
    section_name = section.text.strip()
    dir.Append(
      Function(
        DirectoryItem(
          ChannelVideos,
          section_name,
          thumb=Function(GetThumb, thumb_url=thumb_url)
        ),
        url=url,
        channel_name=name,
        name=section_name
      )
    )
  
  return dir
  
###################################################################################################
def ChannelVideos(sender,url,channel_name,name):
  dir = MediaContainer(title1=channel_name,title2=name,viewGroup='ChannelVideos')
  videos = GetChannelVideos( url )
  
  for video in videos:
    dir.Append(
      WebVideoItem(
        BASE_URL + video['url'],
        title=video['title'],
        thumb=Function(GetThumb, thumb_url=video['thumb_url'] + '?maxwidth=512&maxheight=512')
      )
    )
    # Log( video['title'] )
    # Log( video['url'] )
    # Log( video['thumb_url'] )
  return dir
  
###################################################################################################
def Spotlight(sender):
  dir = MediaContainer(title1=L('pokerstars.tv'),title2=L('spotlight'),viewGroup='ChannelVideos')
  highlights = HTML.ElementFromURL(SCHEDULE_URL, errors='ignore').xpath('//*/div[@id="template"]/div[@id="clm-two"]/div/div[@class="content spotlight"]/ul/li')
    
  for highlight in highlights:
    title     = highlight.xpath('.//h3/a')[0].text.strip()
    link      = highlight.xpath('.//a[@class="thumb"]')[0]
    url       = link.get('href')
    thumb_url = link.xpath('.//img')[0].get('src')
    desc      = highlight.xpath('.//a[2]')[0].text.strip()
    is_video  = ( url.find('poker-video') != -1 )
    
    if is_video:
      dir.Append(
        WebVideoItem(
          BASE_URL + url,
          title=title,
          thumb=Function(GetThumb, thumb_url=thumb_url),
          summary=desc
        )
      )
    else:
      dir.Append(
        Function(
          DirectoryItem( 
            ChannelDetails,
            title,
            thumb=Function(GetThumb, thumb_url=thumb_url)
          ),
          url=url,
          name=title,
          thumb_url=thumb_url
        )
      )
  
  return dir

###################################################################################################
# HELPERS
###################################################################################################
def GetThumb(thumb_url):
  data = HTTP.Request(thumb_url)
  if data:
    return DataObject(data, 'image/png')
  else:
    return Redirect(R(PLUGIN_ICON_DEFAULT))
    
def GetChannelVideos(url, is_sub_page=False ):
  videos = []
  the_url = BASE_URL + url
  # Log('Getting videos from:' + the_url)
  page = HTML.ElementFromURL(the_url, errors='ignore')
  video_elements = page.xpath( '//*/div[@id="clm-two"]/div[2]/div[@class="content clearfix"]/div[@class="results_vidList"]/ul[@class="videos"]/li/a' )
  for video in video_elements:
    thumb_span = video.xpath('.//span[@class="thumb"]')[0]
    title_span = video.xpath('.//strong[@class="name"]')[0]
    
    videos.append({
      'title': title_span.text.strip(),
      'url': video.get('href'),
      'thumb_url': re.sub( r'.*url\(([^\?)]+).*', r'\1', thumb_span.get('style') ) # ?maxwidth=84&maxheight=999
    })
  
  if is_sub_page == False:
    # see if there are any other pages
    last_page = page.xpath( '//*/div[@id="clm-two"]/div[2]/div[@class="content clearfix"]/div[@class="results_vidList"]/ul[@class="pag"]/li[@class="last"]/a' ) #[0].text.strip
  
    if len(last_page):
      last_page = last_page[0]
      pages_url = re.sub( r'\?.*', '', url ) + re.sub( r'[0-9]+$', '', last_page.get('href') )
      # Log( 'Pages URL: ' + pages_url )
      total_pages = int(last_page.text.strip())
      # Log( 'Total pages: ' + str( total_pages ) )
      i = 2
      while (i <= total_pages):
        videos.extend( GetChannelVideos( pages_url + str(i), True ))
        # Log( 'Processing page: ' + i )
        i = i + 1

  return videos