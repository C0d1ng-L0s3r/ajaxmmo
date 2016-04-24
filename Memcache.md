data = Messages.gql()

memcache.add("messages", data, 60)



from google.appengine.api import memcache

def get\_height(x,y):

> height = memcache.get(x + "" + y)
> if height is not None:
> > return height

> else:
> > height = get\_height\_from\_image\_map(x,y)
> > if not memcache.add(x + "" + y, height, 10):
> > > logging.error("Memcache set failed.")

> > return height

"""use one object with all the tiles the user knows.