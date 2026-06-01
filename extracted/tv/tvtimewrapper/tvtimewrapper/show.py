# Class that has the methods for the shows data

class showManager:
  def __init__(self,main):
    """
    Show data instance accessible thoruogh `tvtime.show.METHOD`
    """
    self.m = main

  def search(self, query, limit=10):
    """
    Allows to search for shows by name. By default the `limit` is set to 10 results, you can ask for more.
    """
    return self.m.session.get(f"{self.m.url}/show?q={query}&limit={limit}").json()

  def actors(self, show):
    """
    Returns list of actors given show ID as argument
    """
    return self.m.session.get(f"{self.m.url}/show/{show}/actors").json()
  
  def myShows(self):
    """
    Returns list of all the user TV shows split by categories. At the current time:
    - not_started_yet
    - coming_soon
    - watching
    - up_to_date
    - finished
    - all_time_favorites
    - stopped_watching
    - for_later
    """
    return self.m.session.get(f"{self.m.url}/my_shows").json()
  
  def followed(self):
    """
    Returns detailed list of all the "Followed" TV shows
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/followed_shows").json()
  
  def forLater(self):
    """
    Returns detailed list of shows that were set as "For later"
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/for_later").json()