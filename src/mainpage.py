import datetime

from models import Tile
from models import Unit

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from google.appengine.api import images


#from django.utils import simplejson


class MainPage(webapp.RequestHandler):
  def get(self):
    head = """<html><head><title>Mainpage</title>"""
    head = head + """<script src="/static/jquery-1.2.6.min.js" type="text/javascript"></script>"""
    head = head + """<script src="/static/default.js" type="text/javascript"></script>"""
    head = head + """<link href="/static/default.css" rel="stylesheet" type="text/css" /></head>"""
    head = head + """<body>"""
    
    self.response.out.write(head)
    
    self.response.out.write("""
          </div>
        </body>
      </html>""")
    
class GetTiles(webapp.RequestHandler):
  def get(self):

    # should get the tiles, within proximity of units.
    # foreach unit, get tiles within range of the unit
    # in this instance limit it to 1 unit only
    units = Unit.gql("where user = :1 limit 1", users.get_current_user() )

    alltiles = []
    
    json = "{tiles: ["
    
    for unit in units:
        fov = 3 # fov is how many tiles a unit can see around it
        xleft = unit.x - fov
        xright = unit.x + fov
        ytop = unit.y - fov
        ybottom = unit.y + fov
        
        firstnode = True   
        
        for x in range(xleft, xright):
            for y in range(ytop, ybottom):
                # read pixel in heightmap using pil
                
#                im = Image.open("genesis.png")
#                #im.mode = "L"
#                pix = im.load()
#                
#                size = im.size
#                
#                firstnode = True
#                id = 0
#                json = ""
#                
#                f=open('terrain.json', 'a')
#                
#                for x in range(0, size[0]):
#                   for y in range(0, size[1]):
#                
                
                tiles = Tile.gql("""where x = :1 and y = :2""", x, y )
                for tile in tiles:
                    if firstnode == False:
                        json = json + ","
                    json = json + "{"
                    json = json + "x:'" + str(tile.x) + "',"
                    json = json + "y:'" + str(tile.y) + "',"
                    json = json + "id:'" + str(tile.key().id()) + "'"
                    json = json + "}"
                    firstnode = False
    json = json + "]}"    
            
    self.response.out.write(json)

class GetUnits(webapp.RequestHandler):
    def get(self):
        units = Unit.gql("where user = :1 limit 1", users.get_current_user() )
        firstnode = True
        
        json = "{units: ["
        for unit in units:
            if firstnode == False:
                json = json + ","
            json = json + "{"
            json = json + "x:'" + str(unit.x) + "',"
            json = json + "y:'" + str(unit.y) + "',"
            json = json + "id:'" + str(unit.key().id()) + "'"
            json = json + "}"
            firstnode = False
        json = json + "]}"
            
        self.response.out.write(json)
        
    
class InitTile(webapp.RequestHandler):
  def post(self):
    tile = Tile()
    tile.x = int(self.request.get("x"))
    tile.y = int(self.request.get("y"))
    tile.height = int(self.request.get("height"))
    tile.type = int(self.request.get("type"))
    tile.put()
    
    
class InitUnit(webapp.RequestHandler):
  def post(self):
    unit = Unit()
    unit.x = int(self.request.get("x"))
    unit.y = int(self.request.get("y"))
    unit.user = users.get_current_user()
    unit.put()
    
    
class ClickOnTile(webapp.RequestHandler):
  def post(self):

    tile = Tile.get_by_id(int(self.request.get("id"))) #.all()
    tile.type = 0
    tile.put()
    
    self.response.out.write("success ")
    
class MenuAction(webapp.RequestHandler):
    def post(selfself):
        # get the name of the clicked menu action
        action = self.request.get("action")
        
        # process the action
        
        