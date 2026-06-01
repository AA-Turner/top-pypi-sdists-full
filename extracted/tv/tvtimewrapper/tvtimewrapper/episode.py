# Class that has the methods for the episodes data
from .exceptions import *

class episodeManager:
  def __init__(self,main):
    """
    Episode data instance accessible thoruogh `tvtime.episode.METHOD`
    """
    self.m = main
    self.reactions = {
      "great" : 1,
      "wow" : 3,
      "ok" : 6,
      "bad" : 7,
      "good" : 8
    }

  def _rewatchVal(self,v):
    return 1 if v else 0

  def markWatched(self, episode, is_rewatch=False):
    """
    Mark episode as watched. The required argument is the episode ID. You can also specify if it's a rewatch by setting `is_rewatch=True`
    """
    return self.m.session.post(f"{self.m.url}/watched_episodes/episode/{episode}?is_rewatch={self._rewatchVal(is_rewatch)}").json()

  def markUnwatched(self, episode):
    """
    Mark episode as not watched. The required argument is the episode ID. 
    """
    return self.m.session.delete(f"{self.m.url}/watched_episodes/episode/{episode}").json()

  def toWatch(self):
    """
    Returns list of episodes to watch.
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/to_watch").json()

  def watched(self, page=0, limit=30):
    """
    Returns list of episodes previously watched. By default is set to `limit=30` you can ask for more by spacifying a different
    value and proceed using `page` to go  back further.
    """
    return self.m.session.get(f"{self.m.url}/user/{self.m.userId}/watched_episodes?page={page}&limit={limit}&include_recent_watchers=1").json()

  def comment(self, episode, message):
    """
    Comment with plain text on a specific episode. Required arguments are both episode id and message.
    """
    data = {
      "episode_id": episode,
      "message" : message,
      "should_delete_old_comment" : "false"
    }
    return self.m.session.post(f"{self.m.url}/user/{self.m.userId}/comment_episode", data=data).json()

  def deleteComment(self, comment_id):
    """
    Delete your own comment by specifying the comment ID
    """
    return self.m.session.delete(f"{self.m.url}/user/{self.m.userId}/comment_episode?comment_id={comment_id}").json()

  def react(self, episode, reaction):
    """
    React to the episode with an emotion given episode ID and reaction type.
    This is the "star-meter" in the application. Availeble reactions: `great`, `wow`, `ok`, `bad`, `good`
    """
    if str(reaction).lower() not in self.reactions:
      raise TVTimeReactionNotExists(f"{reaction} is not a possible reaction.")
    data = {
      "episode_id": episode,
      "emotion_id" : self.reactions[reaction]
    }
    return self.m.session.post(f"{self.m.url}/user/{self.m.userId}/episode_emotion", data=data).json()

  def deleteReaction(self, episode):
    """
    Remove / Reset reaction to an episode, given episode ID
    """
    return self.m.session.delete(f"{self.m.url}/user/{self.m.userId}/episode_emotion?episode_id={episode}").json()

  def voteActor(self, episode, actor):
    """
    Vote actor on a specific episode given episode ID and actor ID
    """
    return self.m.session.put(f"{self.m.url}/user/{self.m.userId}/actor_vote?actor_id={actor}&episode_id={episode}").json()

  def deleteActorVote(self, episode, actor):
    """
    Reset vote actor on a specific episode given episode ID and actor ID
    """
    return self.m.session.delete(f"{self.m.url}/user/{self.m.userId}/actor_vote?actor_id={actor}&episode_id={episode}").json()
