# Class that has the methods for the user data

class userManager:
  def __init__(self,main):
    """
    User data instance accessible thoruogh `tvtime.user.METHOD`
    """
    self.m = main

  def profile(self):
    """
    Get user profile data
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/profile").json()

  def friends(self):
    """
    Get user friend list
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/friends").json()

  def stats(self):
    """
    Get user stats
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/stats").json()

  def badges(self):
    """
    Get user badges list
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/badges").json()

  def calendar(self):
    """
    Get user calendar of upcoming shows
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/calendar").json()

  def notifications(self, page=0, limit=20):
    """
    Get user notifications. By default only 20, you can set different limit and use `page` accordingly
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/notifications?page={page}&limit={limit}").json()
