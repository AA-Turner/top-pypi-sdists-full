"""
nx_channel_tools — comprehensive per-app tool catalogs for the channel/commerce connectors.

Auto-assembled from verified per-app API research (workflow wmw753k93). Each app exposes 15-31 REAL tools
spanning its whole API surface (read + write), so /connected shows a real toolset instead of "0 tools" and the
host-agent can dispatch them. Execution routes by SUBSTRATE:
  - local_keychain_token : the CLI calls the app API DIRECTLY with a local Keychain token.
  - shared_oauth_vault   : connection truth lives in Nexplora's shared web/CLI vault; execution
                           fails closed until a scoped server route is enabled.
  - bos_bridge           : the token is SERVER-SIDE (Nexplora BOS); execution goes through POST
                           /api/business-os/<app>/call (eBay live via nx_ebay_tools; others pending their proxy).
  - server_dispatch      : runs via the Nexplora server dispatch (Google Workspace).

HONEST BY CONSTRUCTION: endpoints are real; a write on a credit-blocked/paywalled tier (e.g. X 402) or an
un-deployed BOS proxy returns the REAL error / a clear "pending" — it NEVER fabricates success.
"""

CHANNEL_TOOL_CATALOG = {
  "x": {
    "substrate": "shared_oauth_vault",
    "display_name": "X (Twitter)",
    "tools": [
      {
        "name": "x_post_tweet",
        "description": "Create (publish) a tweet as the authenticated user. Text, reply settings, and attached media/poll/quote go in the body. This is the exact call NX's XChannel.publish_text() makes.",
        "category": "tweets",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/tweets",
        "args": [
          "text:string"
        ],
        "scopes": "tweet.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_reply_tweet",
        "description": "Reply to an existing tweet — create-tweet endpoint with reply.in_reply_to_tweet_id in the body.",
        "category": "tweets",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/tweets",
        "args": [
          "text:string",
          "in_reply_to_tweet_id:string"
        ],
        "scopes": "tweet.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_quote_tweet",
        "description": "Post a quote tweet by referencing another tweet's id in quote_tweet_id in the create-tweet body.",
        "category": "tweets",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/tweets",
        "args": [
          "text:string",
          "quote_tweet_id:string"
        ],
        "scopes": "tweet.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_delete_tweet",
        "description": "Delete a tweet the authenticated user owns, by id.",
        "category": "tweets",
        "method": "DELETE",
        "endpoint": "https://api.twitter.com/2/tweets/{id}",
        "args": [
          "id:string"
        ],
        "scopes": "tweet.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_get_tweet",
        "description": "Look up a single tweet by id with optional expansions/fields (author, metrics, referenced tweets, media).",
        "category": "tweets",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/tweets/{id}",
        "args": [
          "id:string"
        ],
        "scopes": "tweet.read users.read",
        "kind": "read"
      },
      {
        "name": "x_get_tweets_bulk",
        "description": "Look up multiple tweets in one call via a comma-separated list of ids (up to 100).",
        "category": "tweets",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/tweets",
        "args": [
          "ids:string"
        ],
        "scopes": "tweet.read users.read",
        "kind": "read"
      },
      {
        "name": "x_get_me",
        "description": "Get the authenticated user's own profile (id, username, name, metrics). Resolves the author id needed for reply/timeline/like calls.",
        "category": "users",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/me",
        "args": [],
        "scopes": "users.read tweet.read",
        "kind": "read"
      },
      {
        "name": "x_get_user_by_id",
        "description": "Look up a user by numeric id, with optional user.fields.",
        "category": "users",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}",
        "args": [
          "id:string"
        ],
        "scopes": "users.read tweet.read",
        "kind": "read"
      },
      {
        "name": "x_get_user_by_username",
        "description": "Look up a user by @handle (without the @).",
        "category": "users",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/by/username/{username}",
        "args": [
          "username:string"
        ],
        "scopes": "users.read tweet.read",
        "kind": "read"
      },
      {
        "name": "x_get_user_tweets",
        "description": "Get a user's recent authored tweets (their timeline), paginated.",
        "category": "timelines",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}/tweets",
        "args": [
          "id:string"
        ],
        "scopes": "tweet.read users.read",
        "kind": "read"
      },
      {
        "name": "x_get_user_mentions",
        "description": "Get tweets mentioning a given user (mentions timeline).",
        "category": "timelines",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}/mentions",
        "args": [
          "id:string"
        ],
        "scopes": "tweet.read users.read",
        "kind": "read"
      },
      {
        "name": "x_get_home_timeline",
        "description": "Get the authenticated user's reverse-chronological home timeline.",
        "category": "timelines",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}/timelines/reverse_chronological",
        "args": [
          "id:string"
        ],
        "scopes": "tweet.read users.read",
        "kind": "read"
      },
      {
        "name": "x_search_recent",
        "description": "Search tweets from the last 7 days matching a query (operators like from:, #hashtag, keyword).",
        "category": "search",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/tweets/search/recent",
        "args": [
          "query:string"
        ],
        "scopes": "tweet.read users.read",
        "kind": "read"
      },
      {
        "name": "x_like_tweet",
        "description": "Like a tweet as the authenticated user. Body carries the target tweet_id.",
        "category": "likes",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/users/{id}/likes",
        "args": [
          "id:string",
          "tweet_id:string"
        ],
        "scopes": "like.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_unlike_tweet",
        "description": "Remove a like from a tweet the authenticated user previously liked.",
        "category": "likes",
        "method": "DELETE",
        "endpoint": "https://api.twitter.com/2/users/{id}/likes/{tweet_id}",
        "args": [
          "id:string",
          "tweet_id:string"
        ],
        "scopes": "like.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_get_liked_tweets",
        "description": "List tweets a given user has liked.",
        "category": "likes",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}/liked_tweets",
        "args": [
          "id:string"
        ],
        "scopes": "tweet.read users.read like.read",
        "kind": "read"
      },
      {
        "name": "x_retweet",
        "description": "Retweet a tweet as the authenticated user. Body carries the target tweet_id.",
        "category": "retweets",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/users/{id}/retweets",
        "args": [
          "id:string",
          "tweet_id:string"
        ],
        "scopes": "tweet.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_unretweet",
        "description": "Undo a retweet the authenticated user previously made.",
        "category": "retweets",
        "method": "DELETE",
        "endpoint": "https://api.twitter.com/2/users/{id}/retweets/{source_tweet_id}",
        "args": [
          "id:string",
          "source_tweet_id:string"
        ],
        "scopes": "tweet.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_follow_user",
        "description": "Follow another user as the authenticated user. Body carries target_user_id.",
        "category": "follows",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/users/{id}/following",
        "args": [
          "id:string",
          "target_user_id:string"
        ],
        "scopes": "follows.write follows.read users.read",
        "kind": "write"
      },
      {
        "name": "x_unfollow_user",
        "description": "Unfollow a user the authenticated user currently follows.",
        "category": "follows",
        "method": "DELETE",
        "endpoint": "https://api.twitter.com/2/users/{source_user_id}/following/{target_user_id}",
        "args": [
          "source_user_id:string",
          "target_user_id:string"
        ],
        "scopes": "follows.write follows.read users.read",
        "kind": "write"
      },
      {
        "name": "x_get_followers",
        "description": "List the followers of a given user.",
        "category": "follows",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}/followers",
        "args": [
          "id:string"
        ],
        "scopes": "users.read follows.read tweet.read",
        "kind": "read"
      },
      {
        "name": "x_get_following",
        "description": "List the accounts a given user follows.",
        "category": "follows",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}/following",
        "args": [
          "id:string"
        ],
        "scopes": "users.read follows.read tweet.read",
        "kind": "read"
      },
      {
        "name": "x_bookmark_tweet",
        "description": "Add a tweet to the authenticated user's bookmarks. Body carries tweet_id.",
        "category": "bookmarks",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/users/{id}/bookmarks",
        "args": [
          "id:string",
          "tweet_id:string"
        ],
        "scopes": "bookmark.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_remove_bookmark",
        "description": "Remove a tweet from the authenticated user's bookmarks.",
        "category": "bookmarks",
        "method": "DELETE",
        "endpoint": "https://api.twitter.com/2/users/{id}/bookmarks/{tweet_id}",
        "args": [
          "id:string",
          "tweet_id:string"
        ],
        "scopes": "bookmark.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_get_bookmarks",
        "description": "List the authenticated user's bookmarked tweets.",
        "category": "bookmarks",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/users/{id}/bookmarks",
        "args": [
          "id:string"
        ],
        "scopes": "bookmark.read tweet.read users.read",
        "kind": "read"
      },
      {
        "name": "x_create_list",
        "description": "Create a new List owned by the authenticated user (name required; optional description/private in body).",
        "category": "lists",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/lists",
        "args": [
          "name:string"
        ],
        "scopes": "list.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_add_list_member",
        "description": "Add a user to a List the authenticated user owns. Body carries user_id.",
        "category": "lists",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/lists/{id}/members",
        "args": [
          "id:string",
          "user_id:string"
        ],
        "scopes": "list.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_get_list_tweets",
        "description": "Get the timeline of tweets from members of a List.",
        "category": "lists",
        "method": "GET",
        "endpoint": "https://api.twitter.com/2/lists/{id}/tweets",
        "args": [
          "id:string"
        ],
        "scopes": "tweet.read list.read users.read",
        "kind": "read"
      },
      {
        "name": "x_block_user",
        "description": "Block another user as the authenticated user. Body carries target_user_id. (X has restricted v2 block writes on some tiers — verify availability.)",
        "category": "blocks_mutes",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/users/{id}/blocking",
        "args": [
          "id:string",
          "target_user_id:string"
        ],
        "scopes": "block.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_mute_user",
        "description": "Mute another user as the authenticated user. Body carries target_user_id.",
        "category": "blocks_mutes",
        "method": "POST",
        "endpoint": "https://api.twitter.com/2/users/{id}/muting",
        "args": [
          "id:string",
          "target_user_id:string"
        ],
        "scopes": "mute.write tweet.read users.read",
        "kind": "write"
      },
      {
        "name": "x_upload_media",
        "description": "Upload an image/video and get a media_id to attach to a tweet. On the v1.1 media host (upload.twitter.com/1.1/media/upload.json, multipart INIT/APPEND/FINALIZE); X is migrating to a v2 POST /2/media/upload. Needs media.w",
        "category": "media",
        "method": "POST",
        "endpoint": "https://upload.twitter.com/1.1/media/upload.json",
        "args": [
          "media:binary",
          "media_category:string"
        ],
        "scopes": "media.write tweet.write users.read",
        "kind": "write"
      }
    ]
  },
  "youtube": {
    "substrate": "server_dispatch",
    "display_name": "YouTube",
    "tools": [
      {
        "name": "youtube_upload_video",
        "description": "Upload a new video to the authenticated channel (resumable upload). Two-step: initiate an upload session with snippet+status metadata, then PUT the media bytes to the returned session URL. Sets title, description, tags, ",
        "category": "videos",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        "args": [
          "title:string",
          "description:string",
          "privacyStatus:string",
          "categoryId:string",
          "tags:array",
          "mediaFilePath:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.upload",
        "kind": "write"
      },
      {
        "name": "youtube_update_video",
        "description": "Update metadata of an existing video you own — title, description, tags, categoryId, or privacyStatus. Must send the full part being modified (snippet and/or status) since the API replaces the part.",
        "category": "videos",
        "method": "PUT",
        "endpoint": "https://www.googleapis.com/youtube/v3/videos?part=snippet,status",
        "args": [
          "videoId:string",
          "title:string",
          "description:string",
          "tags:array",
          "categoryId:string",
          "privacyStatus:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube",
        "kind": "write"
      },
      {
        "name": "youtube_delete_video",
        "description": "Permanently delete a video you own from the channel.",
        "category": "videos",
        "method": "DELETE",
        "endpoint": "https://www.googleapis.com/youtube/v3/videos?id={videoId}",
        "args": [
          "videoId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube",
        "kind": "write"
      },
      {
        "name": "youtube_set_thumbnail",
        "description": "Upload and set a custom thumbnail image for a video you own (channel must be verified).",
        "category": "videos",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={videoId}",
        "args": [
          "videoId:string",
          "imageFilePath:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.upload",
        "kind": "write"
      },
      {
        "name": "youtube_list_my_videos",
        "description": "List the authenticated channel's own uploads (search with forMine=true, or page the uploads playlist resolved from channels.contentDetails.relatedPlaylists.uploads).",
        "category": "videos",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/search?part=snippet&forMine=true&type=video&order=date&maxResults={maxResults}",
        "args": [
          "maxResults:string",
          "pageToken:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_get_video",
        "description": "Get full details for one or more videos by ID — snippet, statistics (views/likes/comments), contentDetails (duration), status.",
        "category": "videos",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,status&id={videoId}",
        "args": [
          "videoId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_search",
        "description": "Search public YouTube for videos, channels, or playlists by keyword, with optional ordering (relevance/date/viewCount/rating) and result-type filter.",
        "category": "discovery",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type={type}&order={order}&maxResults={maxResults}",
        "args": [
          "query:string",
          "type:string",
          "order:string",
          "maxResults:string",
          "pageToken:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_get_my_channel",
        "description": "Get the authenticated user's own channel — id, title, description, custom URL, branding. Uses mine=true.",
        "category": "channel",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,brandingSettings&mine=true",
        "args": [],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_get_channel_stats",
        "description": "Get channel statistics — subscriber count, total view count, video count — for the authenticated channel (mine=true) or any channel by id.",
        "category": "channel",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true",
        "args": [
          "channelId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_update_channel_branding",
        "description": "Update the channel's branding settings — channel description, keywords, default language, unsubscribed trailer. Sends the brandingSettings part.",
        "category": "channel",
        "method": "PUT",
        "endpoint": "https://www.googleapis.com/youtube/v3/channels?part=brandingSettings",
        "args": [
          "channelId:string",
          "description:string",
          "keywords:string",
          "unsubscribedTrailer:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube",
        "kind": "write"
      },
      {
        "name": "youtube_list_playlists",
        "description": "List playlists owned by the authenticated channel (mine=true) or by a given channelId.",
        "category": "playlists",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&mine=true&maxResults={maxResults}",
        "args": [
          "maxResults:string",
          "channelId:string",
          "pageToken:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_create_playlist",
        "description": "Create a new playlist on the authenticated channel with a title, description, and privacy status.",
        "category": "playlists",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/youtube/v3/playlists?part=snippet,status",
        "args": [
          "title:string",
          "description:string",
          "privacyStatus:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube",
        "kind": "write"
      },
      {
        "name": "youtube_add_playlist_item",
        "description": "Add a video to a playlist you own by referencing the playlistId and the video's resourceId.",
        "category": "playlists",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet",
        "args": [
          "playlistId:string",
          "videoId:string",
          "position:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube",
        "kind": "write"
      },
      {
        "name": "youtube_list_playlist_items",
        "description": "List the videos contained in a playlist by playlistId.",
        "category": "playlists",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={playlistId}&maxResults={maxResults}",
        "args": [
          "playlistId:string",
          "maxResults:string",
          "pageToken:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_list_comment_threads",
        "description": "List top-level comment threads on a video (or across the channel via allThreadsRelatedToChannelId), ordered by time or relevance.",
        "category": "comments",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId={videoId}&order={order}&maxResults={maxResults}",
        "args": [
          "videoId:string",
          "order:string",
          "maxResults:string",
          "pageToken:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_insert_comment_thread",
        "description": "Post a new top-level comment on a video (creates a comment thread).",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet",
        "args": [
          "videoId:string",
          "textOriginal:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.force-ssl",
        "kind": "write"
      },
      {
        "name": "youtube_reply_to_comment",
        "description": "Reply to an existing comment by supplying its parentId and the reply text.",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/youtube/v3/comments?part=snippet",
        "args": [
          "parentId:string",
          "textOriginal:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.force-ssl",
        "kind": "write"
      },
      {
        "name": "youtube_set_comment_moderation",
        "description": "Moderate a comment — set it to published, heldForReview, or rejected (and optionally ban the author).",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/youtube/v3/comments/setModerationStatus?id={commentId}&moderationStatus={moderationStatus}",
        "args": [
          "commentId:string",
          "moderationStatus:string",
          "banAuthor:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.force-ssl",
        "kind": "write"
      },
      {
        "name": "youtube_list_captions",
        "description": "List the caption tracks available for a video you own.",
        "category": "captions",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={videoId}",
        "args": [
          "videoId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.force-ssl",
        "kind": "read"
      },
      {
        "name": "youtube_insert_caption",
        "description": "Upload a new caption/subtitle track for a video you own (resumable media upload of the caption file with language + name).",
        "category": "captions",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/upload/youtube/v3/captions?part=snippet",
        "args": [
          "videoId:string",
          "language:string",
          "name:string",
          "captionFilePath:string",
          "isDraft:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.force-ssl",
        "kind": "write"
      },
      {
        "name": "youtube_list_subscriptions",
        "description": "List the channels the authenticated user is subscribed to (mine=true).",
        "category": "subscriptions",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet,contentDetails&mine=true&maxResults={maxResults}",
        "args": [
          "maxResults:string",
          "pageToken:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_subscribe_channel",
        "description": "Subscribe the authenticated user to a channel by its channelId.",
        "category": "subscriptions",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet",
        "args": [
          "channelId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube",
        "kind": "write"
      },
      {
        "name": "youtube_list_live_broadcasts",
        "description": "List the authenticated channel's live broadcasts, filterable by status (active/upcoming/completed).",
        "category": "live",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/youtube/v3/liveBroadcasts?part=snippet,contentDetails,status&broadcastStatus={broadcastStatus}&maxResults={maxResults}",
        "args": [
          "broadcastStatus:string",
          "maxResults:string",
          "pageToken:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube.readonly",
        "kind": "read"
      },
      {
        "name": "youtube_create_live_broadcast",
        "description": "Schedule a new live broadcast with a title, scheduled start time, and privacy status (then bind a liveStream and transition it live).",
        "category": "live",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/youtube/v3/liveBroadcasts?part=snippet,status,contentDetails",
        "args": [
          "title:string",
          "scheduledStartTime:string",
          "privacyStatus:string"
        ],
        "scopes": "https://www.googleapis.com/auth/youtube",
        "kind": "write"
      },
      {
        "name": "youtube_analytics_query",
        "description": "Query the YouTube Analytics API for channel performance — metrics (views, estimatedMinutesWatched, averageViewDuration, subscribersGained, likes, comments, estimatedRevenue) over a date range, optionally split by dimensi",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://youtubeanalytics.googleapis.com/v2/reports?ids=channel==MINE&startDate={startDate}&endDate={endDate}&metrics={metrics}&dimensions={dimensions}",
        "args": [
          "startDate:string",
          "endDate:string",
          "metrics:string",
          "dimensions:string",
          "filters:string",
          "sort:string"
        ],
        "scopes": "https://www.googleapis.com/auth/yt-analytics.readonly",
        "kind": "read"
      }
    ]
  },
  "tiktok": {
    "substrate": "bos_bridge",
    "display_name": "TikTok",
    "tools": [
      {
        "name": "tiktok_query_creator_info",
        "description": "Query the authenticated creator's posting eligibility and account settings before publishing — privacy-level options, whether comments/duet/stitch are allowed, max video duration, and nickname. Required first step before",
        "category": "posting",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/post/publish/creator_info/query/",
        "args": [],
        "scopes": "video.publish",
        "kind": "read"
      },
      {
        "name": "tiktok_post_video_init",
        "description": "Initialize a video post/upload. For PULL_FROM_URL supply a public video_url; for FILE_UPLOAD supply video_size/chunk info. Returns a publish_id used to poll status. This is the exact call the server's tiktok-adapter alre",
        "category": "posting",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/post/publish/video/init/",
        "args": [
          "post_info:object",
          "source_info:object"
        ],
        "scopes": "video.publish",
        "kind": "write"
      },
      {
        "name": "tiktok_post_video_inbox_init",
        "description": "Initialize a video upload to the creator's TikTok inbox as a DRAFT (no audit required, un-audited apps allowed). Creator finishes/publishes in-app. This is the endpoint the server tiktok-adapter.post() calls today (sourc",
        "category": "posting",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/",
        "args": [
          "source_info:object",
          "post_info:object"
        ],
        "scopes": "video.upload",
        "kind": "write"
      },
      {
        "name": "tiktok_post_photo_init",
        "description": "Initialize a photo (image carousel) post via the Content Posting API. Supply image URLs, title, description, cover index, and privacy level. Returns a publish_id.",
        "category": "posting",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/post/publish/content/init/",
        "args": [
          "post_info:object",
          "source_info:object",
          "post_mode:string",
          "media_type:string"
        ],
        "scopes": "video.publish",
        "kind": "write"
      },
      {
        "name": "tiktok_post_publish_status",
        "description": "Poll the status of a video/photo publish by publish_id — returns PROCESSING / PUBLISH_COMPLETE / FAILED plus the resulting post id. Second step of every publish flow.",
        "category": "posting",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/post/publish/status/fetch/",
        "args": [
          "publish_id:string"
        ],
        "scopes": "video.publish",
        "kind": "read"
      },
      {
        "name": "tiktok_get_user_info",
        "description": "Get the authenticated user's profile: open_id, union_id, avatar, display name, bio, profile deep link, verification status, and (with stats fields) follower_count/following_count/likes_count/video_count.",
        "category": "user",
        "method": "GET",
        "endpoint": "https://open.tiktokapis.com/v2/user/info/?fields=open_id,union_id,avatar_url,display_name,bio_description,profile_deep_link,is_verified,follower_count,following_count,likes_count,video_count",
        "args": [
          "fields:string"
        ],
        "scopes": "user.info.basic,user.info.profile,user.info.stats",
        "kind": "read"
      },
      {
        "name": "tiktok_list_my_videos",
        "description": "List the authenticated creator's published videos (paginated via cursor/max_count). Returns per-video id, title, cover_image_url, share_url, duration, create_time and engagement fields. The server pullMetrics path alread",
        "category": "videos",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/video/list/?fields=id,title,cover_image_url,share_url,video_description,duration,height,width,create_time,like_count,comment_count,share_count,view_count",
        "args": [
          "max_count:integer",
          "cursor:integer",
          "fields:string"
        ],
        "scopes": "video.list",
        "kind": "read"
      },
      {
        "name": "tiktok_query_videos",
        "description": "Fetch full details for specific videos by their video ids (up to 20) — used to refresh analytics for known posts. Returns the same rich fields as the list endpoint for the requested ids.",
        "category": "videos",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/video/query/?fields=id,title,cover_image_url,share_url,video_description,duration,create_time,like_count,comment_count,share_count,view_count",
        "args": [
          "filters:object",
          "fields:string"
        ],
        "scopes": "video.list",
        "kind": "read"
      },
      {
        "name": "tiktok_get_video_insights",
        "description": "Video-level analytics/insights (impressions, reach, profile views, engagement, audience) via the TikTok Business API metrics endpoint. Requires a Business account and business-scoped token; not available on the basic Dis",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/video/list/",
        "args": [
          "business_id:string",
          "video_ids:array",
          "fields:array"
        ],
        "scopes": "video.list,business.get",
        "kind": "read"
      },
      {
        "name": "tiktok_get_account_insights",
        "description": "Account-level analytics for a Business account — follower growth, profile views, likes/comments/shares totals, and audience demographics over a date range — via the TikTok Business API.",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/get/",
        "args": [
          "business_id:string",
          "fields:array",
          "start_date:string",
          "end_date:string"
        ],
        "scopes": "business.get",
        "kind": "read"
      },
      {
        "name": "tiktok_list_video_comments",
        "description": "List comments on one of the creator's videos (Business API / limited-access; not exposed on the basic Display API tier). Returns comment id, text, like_count, reply_count, create_time, and commenter info.",
        "category": "comments",
        "method": "GET",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/comment/list/",
        "args": [
          "business_id:string",
          "video_id:string",
          "cursor:integer",
          "count:integer"
        ],
        "scopes": "business.get,comment.list",
        "kind": "read"
      },
      {
        "name": "tiktok_reply_to_comment",
        "description": "Post a reply to a comment on the creator's own video (Business API, comment.manage). Write action — moderating/replying to audience comments. Requires Business account and audited app.",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/comment/reply/create/",
        "args": [
          "business_id:string",
          "video_id:string",
          "comment_id:string",
          "text:string"
        ],
        "scopes": "comment.manage",
        "kind": "write"
      },
      {
        "name": "tiktok_hide_comment",
        "description": "Hide (or unhide) a comment on the creator's own video via the Business API comment-management endpoint. Write moderation action.",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/comment/update/",
        "args": [
          "business_id:string",
          "comment_id:string",
          "action:string"
        ],
        "scopes": "comment.manage",
        "kind": "write"
      },
      {
        "name": "tiktok_like_comment",
        "description": "Like or unlike a comment on the creator's own video via the Business API. Write engagement action.",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/comment/like/create/",
        "args": [
          "business_id:string",
          "comment_id:string",
          "action:string"
        ],
        "scopes": "comment.manage",
        "kind": "write"
      },
      {
        "name": "tiktok_get_follower_count",
        "description": "Get the authenticated creator's follower and following COUNTS (TikTok's public Display API exposes counts via user/info stats fields, not a full follower LIST). Read-only.",
        "category": "audience",
        "method": "GET",
        "endpoint": "https://open.tiktokapis.com/v2/user/info/?fields=follower_count,following_count",
        "args": [
          "fields:string"
        ],
        "scopes": "user.info.stats",
        "kind": "read"
      },
      {
        "name": "tiktok_list_followers",
        "description": "List follower accounts of a Business account (Business API only; requires business.get scope and business_id — NOT available on the basic Display API). Returns follower open_ids/handles paginated by cursor.",
        "category": "audience",
        "method": "GET",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/get/followers/",
        "args": [
          "business_id:string",
          "cursor:integer",
          "count:integer"
        ],
        "scopes": "business.get",
        "kind": "read"
      },
      {
        "name": "tiktok_list_following",
        "description": "List accounts the Business account is following (Business API only; requires business.get and business_id — not on the basic Display API). Paginated by cursor.",
        "category": "audience",
        "method": "GET",
        "endpoint": "https://business-api.tiktok.com/open_api/v1.3/business/get/followings/",
        "args": [
          "business_id:string",
          "cursor:integer",
          "count:integer"
        ],
        "scopes": "business.get",
        "kind": "read"
      },
      {
        "name": "tiktok_refresh_access_token",
        "description": "Refresh the creator's TikTok access token using the stored refresh token. Server-side only (uses client_key + client_secret); the CLI never sees the token. This is the token endpoint the server oauth-config already targe",
        "category": "auth",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/oauth/token/",
        "args": [
          "grant_type:string",
          "refresh_token:string",
          "client_key:string",
          "client_secret:string"
        ],
        "scopes": "",
        "kind": "write"
      },
      {
        "name": "tiktok_revoke_access",
        "description": "Revoke the creator's TikTok access token, disconnecting the account. Write/destructive account action.",
        "category": "auth",
        "method": "POST",
        "endpoint": "https://open.tiktokapis.com/v2/oauth/revoke/",
        "args": [
          "client_key:string",
          "client_secret:string",
          "token:string"
        ],
        "scopes": "",
        "kind": "write"
      },
      {
        "name": "tiktok_get_connection_status",
        "description": "Read whether TikTok is connected for the signed-in operator (server BOS connection state), reused from the existing bridge. Reads /api/business-os/connections and checks for platform=='tiktok'. This is the one path fully",
        "category": "account",
        "method": "GET",
        "endpoint": "https://api.nexplora.ai/api/business-os/connections",
        "args": [],
        "scopes": "",
        "kind": "read"
      },
      {
        "name": "tiktok_distribute_post",
        "description": "LIVE TODAY: publish a TikTok video through the existing server distribute route, which routes to tiktok-adapter.post() → inbox/video/init. Supply brandId, videoUrl and caption. This is the only TikTok write path currentl",
        "category": "posting",
        "method": "POST",
        "endpoint": "https://api.nexplora.ai/api/business-os/distribute",
        "args": [
          "brandId:string",
          "platform:string",
          "action:string",
          "videoUrl:string",
          "caption:string"
        ],
        "scopes": "video.upload",
        "kind": "write"
      }
    ]
  },
  "meta": {
    "substrate": "bos_bridge",
    "display_name": "Meta (Instagram/Facebook)",
    "tools": [
      {
        "name": "meta_list_pages",
        "description": "List the Facebook Pages the connected user manages, with per-page access tokens, category, and tasks. Used in lib/social/connectors/meta-pages.ts. This is the prerequisite call — page-scoped actions need the page access_",
        "category": "pages",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/me/accounts",
        "args": [
          "fields:string",
          "limit:string"
        ],
        "scopes": "pages_show_list",
        "kind": "read"
      },
      {
        "name": "meta_get_page",
        "description": "Get details/metadata for one Facebook Page (name, category, fan_count/followers, about, link, verification status).",
        "category": "pages",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}",
        "args": [
          "page_id:string",
          "fields:string"
        ],
        "scopes": "pages_show_list,pages_read_engagement",
        "kind": "read"
      },
      {
        "name": "meta_list_page_posts",
        "description": "List posts published by a Facebook Page (message, created_time, permalink, id). Uses /{pageId}/published_posts as in lib/social/connectors/meta-page-posts.ts.",
        "category": "pages",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}/published_posts",
        "args": [
          "page_id:string",
          "fields:string",
          "limit:string",
          "since:string",
          "until:string"
        ],
        "scopes": "pages_read_engagement,pages_show_list",
        "kind": "read"
      },
      {
        "name": "meta_get_page_feed",
        "description": "Read the Page's feed timeline including posts by the Page and (with permission) visitor posts.",
        "category": "pages",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}/feed",
        "args": [
          "page_id:string",
          "fields:string",
          "limit:string"
        ],
        "scopes": "pages_read_engagement",
        "kind": "read"
      },
      {
        "name": "meta_create_page_post",
        "description": "Publish a text/link post to a Facebook Page feed. This is the one action wired server-side today via /api/business-os/distribute -> facebook-adapter.post (POST /{pageId}/feed with message+link).",
        "category": "pages",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}/feed",
        "args": [
          "page_id:string",
          "message:string",
          "link:string",
          "published:boolean"
        ],
        "scopes": "pages_manage_posts",
        "kind": "write"
      },
      {
        "name": "meta_create_page_photo_post",
        "description": "Publish a photo post to a Facebook Page by supplying an image URL (or uploaded photo) plus a caption.",
        "category": "pages",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}/photos",
        "args": [
          "page_id:string",
          "url:string",
          "caption:string",
          "published:boolean"
        ],
        "scopes": "pages_manage_posts",
        "kind": "write"
      },
      {
        "name": "meta_delete_page_post",
        "description": "Delete a post the Page previously published, by post id.",
        "category": "pages",
        "method": "DELETE",
        "endpoint": "https://graph.facebook.com/v20.0/{post_id}",
        "args": [
          "post_id:string"
        ],
        "scopes": "pages_manage_posts",
        "kind": "write"
      },
      {
        "name": "meta_get_post_insights",
        "description": "Get engagement insights for a single Page post (impressions, reach, reactions, clicks, video views).",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{post_id}/insights",
        "args": [
          "post_id:string",
          "metric:string"
        ],
        "scopes": "pages_read_engagement",
        "kind": "read"
      },
      {
        "name": "meta_get_page_insights",
        "description": "Pull Page-level daily insights (page_impressions, page_post_engagements, reactions). Exact metric set used in facebook-adapter.ts pullMetrics; some page_* metrics are deprecated in newer Graph versions — see notes.",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}/insights",
        "args": [
          "page_id:string",
          "metric:string",
          "period:string",
          "since:string",
          "until:string"
        ],
        "scopes": "pages_read_engagement",
        "kind": "read"
      },
      {
        "name": "meta_list_page_comments",
        "description": "List comments on a Page post for moderation/reply.",
        "category": "comments",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{post_id}/comments",
        "args": [
          "post_id:string",
          "fields:string",
          "limit:string",
          "order:string"
        ],
        "scopes": "pages_read_engagement",
        "kind": "read"
      },
      {
        "name": "meta_reply_page_comment",
        "description": "Post a public reply comment on a Page post or reply to an existing comment.",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/{object_id}/comments",
        "args": [
          "object_id:string",
          "message:string"
        ],
        "scopes": "pages_manage_engagement",
        "kind": "write"
      },
      {
        "name": "meta_list_page_conversations",
        "description": "List a Page's Messenger conversation threads (inbox), with participants and updated_time.",
        "category": "messaging",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}/conversations",
        "args": [
          "page_id:string",
          "platform:string",
          "fields:string",
          "limit:string"
        ],
        "scopes": "pages_messaging,pages_read_engagement",
        "kind": "read"
      },
      {
        "name": "meta_get_conversation_messages",
        "description": "Read messages within a specific Page Messenger conversation thread.",
        "category": "messaging",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{conversation_id}/messages",
        "args": [
          "conversation_id:string",
          "fields:string",
          "limit:string"
        ],
        "scopes": "pages_messaging,pages_read_engagement",
        "kind": "read"
      },
      {
        "name": "meta_send_page_message",
        "description": "Send a Messenger message from the Page to a user (within the 24h window / message tags). Aligned with lib/channel-adapters/meta-messenger/outbound-dispatch.ts.",
        "category": "messaging",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}/messages",
        "args": [
          "page_id:string",
          "recipient:object",
          "message:object",
          "messaging_type:string"
        ],
        "scopes": "pages_messaging",
        "kind": "write"
      },
      {
        "name": "meta_ig_get_account",
        "description": "Get the Instagram Business/Creator account linked to a Page (ig_id, username, followers_count, media_count) via the Page's instagram_business_account edge.",
        "category": "instagram",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{page_id}",
        "args": [
          "page_id:string",
          "fields:string"
        ],
        "scopes": "instagram_basic,pages_show_list",
        "kind": "read"
      },
      {
        "name": "meta_ig_list_media",
        "description": "List an Instagram Business account's published media (posts/reels) with caption, media_type, permalink, timestamp.",
        "category": "instagram",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{ig_user_id}/media",
        "args": [
          "ig_user_id:string",
          "fields:string",
          "limit:string"
        ],
        "scopes": "instagram_basic",
        "kind": "read"
      },
      {
        "name": "meta_ig_create_media_container",
        "description": "Step 1 of IG publishing: create a media container from an image_url or video_url plus caption. Returns a creation_id used by media_publish.",
        "category": "instagram",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/{ig_user_id}/media",
        "args": [
          "ig_user_id:string",
          "image_url:string",
          "video_url:string",
          "caption:string",
          "media_type:string"
        ],
        "scopes": "instagram_content_publish,instagram_basic",
        "kind": "write"
      },
      {
        "name": "meta_ig_publish_media",
        "description": "Step 2 of IG publishing: publish a previously-created media container (creation_id) to the Instagram feed.",
        "category": "instagram",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/{ig_user_id}/media_publish",
        "args": [
          "ig_user_id:string",
          "creation_id:string"
        ],
        "scopes": "instagram_content_publish",
        "kind": "write"
      },
      {
        "name": "meta_ig_get_media_insights",
        "description": "Get insights for a single Instagram media object (impressions, reach, likes, comments, saves, video views).",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{ig_media_id}/insights",
        "args": [
          "ig_media_id:string",
          "metric:string"
        ],
        "scopes": "instagram_manage_insights,instagram_basic",
        "kind": "read"
      },
      {
        "name": "meta_ig_list_media_comments",
        "description": "List comments on an Instagram media object for moderation/reply.",
        "category": "comments",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/{ig_media_id}/comments",
        "args": [
          "ig_media_id:string",
          "fields:string",
          "limit:string"
        ],
        "scopes": "instagram_basic,instagram_manage_comments",
        "kind": "read"
      },
      {
        "name": "meta_ig_reply_comment",
        "description": "Reply to a comment on an Instagram media object.",
        "category": "comments",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/{ig_comment_id}/replies",
        "args": [
          "ig_comment_id:string",
          "message:string"
        ],
        "scopes": "instagram_manage_comments",
        "kind": "write"
      },
      {
        "name": "meta_list_ad_campaigns",
        "description": "List Marketing API ad campaigns under an ad account (name, status, objective, budget). Uses /{adAccountId}/campaigns as in lib/marketing/connectors/meta-marketing.ts.",
        "category": "ads",
        "method": "GET",
        "endpoint": "https://graph.facebook.com/v20.0/act_{ad_account_id}/campaigns",
        "args": [
          "ad_account_id:string",
          "fields:string",
          "limit:string"
        ],
        "scopes": "ads_read",
        "kind": "read"
      },
      {
        "name": "meta_create_ad_creative",
        "description": "Create an ad creative under an ad account (used by lib/nx-cloud-gates/provider-execution/marketing-executors.ts -> act_{adAccount}/adcreatives).",
        "category": "ads",
        "method": "POST",
        "endpoint": "https://graph.facebook.com/v20.0/act_{ad_account_id}/adcreatives",
        "args": [
          "ad_account_id:string",
          "name:string",
          "object_story_spec:object"
        ],
        "scopes": "ads_management",
        "kind": "write"
      }
    ]
  },
  "google_workspace": {
    "substrate": "server_dispatch",
    "display_name": "Google Workspace",
    "tools": [
      {
        "name": "gmail_get_profile",
        "description": "Read the operator's Gmail profile — email address, total message count, total thread count. This is the one PROVEN-LIVE path (nx_channels.gmail_profile() → dispatch tool 'gmail').",
        "category": "gmail",
        "method": "GET",
        "endpoint": "https://gmail.googleapis.com/gmail/v1/users/me/profile",
        "args": [],
        "scopes": "https://www.googleapis.com/auth/gmail.readonly",
        "kind": "read"
      },
      {
        "name": "gmail_list_messages",
        "description": "List/search messages in the operator's mailbox. Supports Gmail query syntax (from:, subject:, is:unread, after:) and label filtering; returns message ids + thread ids for follow-up gets.",
        "category": "gmail",
        "method": "GET",
        "endpoint": "https://gmail.googleapis.com/gmail/v1/users/me/messages?q={query}&labelIds={labelId}&maxResults={n}",
        "args": [
          "query:string",
          "labelId:string",
          "maxResults:integer"
        ],
        "scopes": "https://www.googleapis.com/auth/gmail.readonly",
        "kind": "read"
      },
      {
        "name": "gmail_get_message",
        "description": "Get one message by id — headers, snippet, body, labels. format=full|metadata|minimal.",
        "category": "gmail",
        "method": "GET",
        "endpoint": "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}?format={format}",
        "args": [
          "id:string",
          "format:string"
        ],
        "scopes": "https://www.googleapis.com/auth/gmail.readonly",
        "kind": "read"
      },
      {
        "name": "gmail_send_message",
        "description": "Send an email from the operator's Gmail (RFC822 base64url raw). WRITE + approval-gated: fails closed without a valid per-session SessionApproval (personal.gmail.send).",
        "category": "gmail",
        "method": "POST",
        "endpoint": "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        "args": [
          "to:string",
          "subject:string",
          "body:string",
          "approval:object"
        ],
        "scopes": "https://www.googleapis.com/auth/gmail.send",
        "kind": "write"
      },
      {
        "name": "gmail_create_draft",
        "description": "Create a draft message (not sent) in the operator's mailbox. Body is the same base64url RFC822 raw as send.",
        "category": "gmail",
        "method": "POST",
        "endpoint": "https://gmail.googleapis.com/gmail/v1/users/me/drafts",
        "args": [
          "to:string",
          "subject:string",
          "body:string"
        ],
        "scopes": "https://www.googleapis.com/auth/gmail.compose",
        "kind": "write"
      },
      {
        "name": "gmail_list_labels",
        "description": "List all Gmail labels (system + user) with ids, useful to resolve label ids for filtered message listing.",
        "category": "gmail",
        "method": "GET",
        "endpoint": "https://gmail.googleapis.com/gmail/v1/users/me/labels",
        "args": [],
        "scopes": "https://www.googleapis.com/auth/gmail.readonly",
        "kind": "read"
      },
      {
        "name": "calendar_list_calendars",
        "description": "List the calendars on the operator's calendar list (id, summary, primary flag, access role).",
        "category": "calendar",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/calendar/v3/users/me/calendarList",
        "args": [],
        "scopes": "https://www.googleapis.com/auth/calendar.readonly",
        "kind": "read"
      },
      {
        "name": "calendar_list_events",
        "description": "List events on a calendar within a time window (timeMin/timeMax RFC3339). Defaults to primary calendar.",
        "category": "calendar",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events?timeMin={timeMin}&timeMax={timeMax}&maxResults={n}&singleEvents=true&orderBy=startTime",
        "args": [
          "calendarId:string",
          "timeMin:string",
          "timeMax:string",
          "maxResults:integer"
        ],
        "scopes": "https://www.googleapis.com/auth/calendar.readonly",
        "kind": "read"
      },
      {
        "name": "calendar_create_event",
        "description": "Create a calendar event (summary, start/end, attendees, location). WRITE + approval-gated (calendar.events.create).",
        "category": "calendar",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events",
        "args": [
          "calendarId:string",
          "summary:string",
          "start:object",
          "end:object",
          "attendees:array"
        ],
        "scopes": "https://www.googleapis.com/auth/calendar.events",
        "kind": "write"
      },
      {
        "name": "calendar_update_event",
        "description": "Update an existing event by id (time change, attendee add, description). WRITE + approval-gated (calendar.events.update).",
        "category": "calendar",
        "method": "PATCH",
        "endpoint": "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events/{eventId}",
        "args": [
          "calendarId:string",
          "eventId:string",
          "patch:object"
        ],
        "scopes": "https://www.googleapis.com/auth/calendar.events",
        "kind": "write"
      },
      {
        "name": "calendar_delete_event",
        "description": "Delete an event by id from a calendar. WRITE + approval-gated.",
        "category": "calendar",
        "method": "DELETE",
        "endpoint": "https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events/{eventId}",
        "args": [
          "calendarId:string",
          "eventId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/calendar.events",
        "kind": "write"
      },
      {
        "name": "drive_list_files",
        "description": "List/search Drive files. Supports the Drive query language (name contains, mimeType=, 'folderId' in parents) and fields projection.",
        "category": "drive",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/drive/v3/files?q={query}&fields=files(id,name,mimeType,parents)&pageSize={n}",
        "args": [
          "query:string",
          "pageSize:integer"
        ],
        "scopes": "https://www.googleapis.com/auth/drive.readonly",
        "kind": "read"
      },
      {
        "name": "drive_get_file",
        "description": "Get a single Drive file's metadata by id (name, mimeType, parents, modifiedTime, size).",
        "category": "drive",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/drive/v3/files/{fileId}?fields=id,name,mimeType,parents,modifiedTime,size",
        "args": [
          "fileId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/drive.readonly",
        "kind": "read"
      },
      {
        "name": "drive_download_file",
        "description": "Download a Drive file's binary content (alt=media). For Google-native docs use export instead.",
        "category": "drive",
        "method": "GET",
        "endpoint": "https://www.googleapis.com/drive/v3/files/{fileId}?alt=media",
        "args": [
          "fileId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/drive.readonly",
        "kind": "read"
      },
      {
        "name": "drive_create_file",
        "description": "Create a Drive file/metadata (JSON metadata create; a folder = mimeType application/vnd.google-apps.folder). WRITE + approval-gated (drive.file.create). Binary content uses the upload endpoint /upload/drive/v3/files?uplo",
        "category": "drive",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/drive/v3/files",
        "args": [
          "name:string",
          "mimeType:string",
          "parents:array"
        ],
        "scopes": "https://www.googleapis.com/auth/drive",
        "kind": "write"
      },
      {
        "name": "drive_create_folder",
        "description": "Create a Drive folder (drive_create_file with mimeType application/vnd.google-apps.folder). WRITE + approval-gated.",
        "category": "drive",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/drive/v3/files",
        "args": [
          "name:string",
          "parents:array"
        ],
        "scopes": "https://www.googleapis.com/auth/drive",
        "kind": "write"
      },
      {
        "name": "drive_share_file",
        "description": "Share a Drive file by creating a permission (role reader/writer, type user/anyone). WRITE + approval-gated (drive.permissions.share_external is the highest-risk id).",
        "category": "drive",
        "method": "POST",
        "endpoint": "https://www.googleapis.com/drive/v3/files/{fileId}/permissions",
        "args": [
          "fileId:string",
          "role:string",
          "type:string",
          "emailAddress:string"
        ],
        "scopes": "https://www.googleapis.com/auth/drive",
        "kind": "write"
      },
      {
        "name": "docs_create_document",
        "description": "Create a new Google Doc (title). Returns the documentId. WRITE + approval-gated.",
        "category": "docs",
        "method": "POST",
        "endpoint": "https://docs.googleapis.com/v1/documents",
        "args": [
          "title:string"
        ],
        "scopes": "https://www.googleapis.com/auth/documents",
        "kind": "write"
      },
      {
        "name": "docs_get_document",
        "description": "Get a Google Doc's structured content by id (title + body structural elements).",
        "category": "docs",
        "method": "GET",
        "endpoint": "https://docs.googleapis.com/v1/documents/{documentId}",
        "args": [
          "documentId:string"
        ],
        "scopes": "https://www.googleapis.com/auth/documents.readonly",
        "kind": "read"
      },
      {
        "name": "docs_append_text",
        "description": "Append/insert text into a Doc via batchUpdate (insertText request at an index). WRITE + approval-gated.",
        "category": "docs",
        "method": "POST",
        "endpoint": "https://docs.googleapis.com/v1/documents/{documentId}:batchUpdate",
        "args": [
          "documentId:string",
          "requests:array"
        ],
        "scopes": "https://www.googleapis.com/auth/documents",
        "kind": "write"
      },
      {
        "name": "sheets_read_values",
        "description": "Read a cell range from a spreadsheet (A1 notation, e.g. Sheet1!A1:D20). Returns the values matrix.",
        "category": "sheets",
        "method": "GET",
        "endpoint": "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}",
        "args": [
          "spreadsheetId:string",
          "range:string"
        ],
        "scopes": "https://www.googleapis.com/auth/spreadsheets.readonly",
        "kind": "read"
      },
      {
        "name": "sheets_append_values",
        "description": "Append rows to a sheet range (values:append, valueInputOption=USER_ENTERED). WRITE + approval-gated (spreadsheets.update).",
        "category": "sheets",
        "method": "POST",
        "endpoint": "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}:append?valueInputOption=USER_ENTERED",
        "args": [
          "spreadsheetId:string",
          "range:string",
          "values:array"
        ],
        "scopes": "https://www.googleapis.com/auth/spreadsheets",
        "kind": "write"
      },
      {
        "name": "sheets_update_values",
        "description": "Overwrite a cell range with new values (values.update, PUT, valueInputOption=USER_ENTERED). WRITE + approval-gated.",
        "category": "sheets",
        "method": "PUT",
        "endpoint": "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}?valueInputOption=USER_ENTERED",
        "args": [
          "spreadsheetId:string",
          "range:string",
          "values:array"
        ],
        "scopes": "https://www.googleapis.com/auth/spreadsheets",
        "kind": "write"
      },
      {
        "name": "sheets_create_spreadsheet",
        "description": "Create a new spreadsheet (title + optional sheet grid). Returns spreadsheetId. WRITE + approval-gated.",
        "category": "sheets",
        "method": "POST",
        "endpoint": "https://sheets.googleapis.com/v4/spreadsheets",
        "args": [
          "title:string"
        ],
        "scopes": "https://www.googleapis.com/auth/spreadsheets",
        "kind": "write"
      }
    ]
  },
  "google_ads": {
    "substrate": "bos_bridge",
    "display_name": "Google Ads",
    "tools": [
      {
        "name": "google_ads_list_accessible_customers",
        "description": "List the Google Ads customer accounts (resource names like customers/1234567890) the authenticated operator can access. The entry point — every other call needs a customer_id from here.",
        "category": "accounts",
        "method": "GET",
        "endpoint": "https://googleads.googleapis.com/v17/customers:listAccessibleCustomers",
        "args": [],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_get_customer",
        "description": "Fetch one Google Ads account's details (descriptive name, currency, time zone, manager flag, test-account flag).",
        "category": "accounts",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_list_campaigns",
        "description": "List campaigns for a customer (id, name, status, advertising_channel_type, budget, start/end dates) via GAQL over the campaign resource.",
        "category": "campaigns",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "status:string",
          "limit:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_get_campaign_metrics",
        "description": "Run an arbitrary GAQL report — impressions, clicks, cost_micros, conversions, ctr, average_cpc, roas — segmented by date/device/network for a customer. The core reporting tool.",
        "category": "reporting",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "query:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_search_stream",
        "description": "Stream large GAQL result sets (all rows in one chunked response, no paging) — used for big keyword/search-term/geo reports that exceed a single search page.",
        "category": "reporting",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:searchStream",
        "args": [
          "customer_id:string",
          "query:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_list_ad_groups",
        "description": "List ad groups under a customer/campaign (id, name, status, type, cpc_bid_micros) via GAQL over the ad_group resource.",
        "category": "ad_groups",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "campaign_id:string",
          "limit:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_list_ads",
        "description": "List ads under a customer/ad group (ad_group_ad resource: ad.id, ad.type, status, final_urls, headlines/descriptions) via GAQL.",
        "category": "ads",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "ad_group_id:string",
          "limit:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_list_keywords",
        "description": "List keyword criteria under a customer/ad group (ad_group_criterion where type=KEYWORD: text, match_type, status, bids, quality_score) via GAQL.",
        "category": "keywords",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "ad_group_id:string",
          "limit:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_list_budgets",
        "description": "List campaign budgets for a customer (campaign_budget: id, name, amount_micros, delivery_method, explicitly_shared) via GAQL.",
        "category": "budgets",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "limit:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_list_conversion_actions",
        "description": "List conversion actions configured for the customer (conversion_action: id, name, category, status, type, counting_type) via GAQL — the tracked goals reporting rolls up into.",
        "category": "conversions",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "limit:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_get_search_terms_report",
        "description": "GAQL report over the search_term_view — the actual user queries that triggered ads, with impressions/clicks/cost/conversions. Drives negative-keyword decisions.",
        "category": "reporting",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/googleAds:search",
        "args": [
          "customer_id:string",
          "campaign_id:string",
          "date_range:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      },
      {
        "name": "google_ads_create_budget",
        "description": "Create a shared/campaign budget (name, amount_micros, delivery_method) — prerequisite for creating a campaign. Returns the campaign_budget resource name. WRITE.",
        "category": "budgets",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/campaignBudgets:mutate",
        "args": [
          "customer_id:string",
          "name:string",
          "amount_micros:string",
          "delivery_method:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_update_budget",
        "description": "Change a campaign budget's amount_micros or delivery_method via an update operation + field_mask. WRITE.",
        "category": "budgets",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/campaignBudgets:mutate",
        "args": [
          "customer_id:string",
          "budget_id:string",
          "amount_micros:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_create_campaign",
        "description": "Create a campaign (name, advertising_channel_type e.g. SEARCH, status, campaign_budget resource, bidding strategy, start/end dates). WRITE.",
        "category": "campaigns",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/campaigns:mutate",
        "args": [
          "customer_id:string",
          "name:string",
          "channel_type:string",
          "budget_resource:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_pause_campaign",
        "description": "Pause a campaign — update mutate setting status=PAUSED with field_mask=status on campaigns/{campaign_id}. WRITE.",
        "category": "campaigns",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/campaigns:mutate",
        "args": [
          "customer_id:string",
          "campaign_id:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_enable_campaign",
        "description": "Enable/resume a campaign — update mutate setting status=ENABLED with field_mask=status on campaigns/{campaign_id}. WRITE.",
        "category": "campaigns",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/campaigns:mutate",
        "args": [
          "customer_id:string",
          "campaign_id:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_create_ad_group",
        "description": "Create an ad group under a campaign (name, campaign resource, status, type, cpc_bid_micros). WRITE.",
        "category": "ad_groups",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/adGroups:mutate",
        "args": [
          "customer_id:string",
          "name:string",
          "campaign_resource:string",
          "cpc_bid_micros:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_pause_ad_group",
        "description": "Pause or enable an ad group — update mutate on adGroups/{ad_group_id} setting status with field_mask=status. WRITE.",
        "category": "ad_groups",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/adGroups:mutate",
        "args": [
          "customer_id:string",
          "ad_group_id:string",
          "status:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_create_ad",
        "description": "Create an ad in an ad group (ad_group_ad: responsive search ad headlines/descriptions + final_urls, status). WRITE.",
        "category": "ads",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/adGroupAds:mutate",
        "args": [
          "customer_id:string",
          "ad_group_resource:string",
          "headlines:string",
          "descriptions:string",
          "final_urls:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_pause_ad",
        "description": "Pause, enable, or remove an ad — mutate on adGroupAds/{ad_group_id}~{ad_id} (update status with field_mask, or remove op). WRITE.",
        "category": "ads",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/adGroupAds:mutate",
        "args": [
          "customer_id:string",
          "ad_group_id:string",
          "ad_id:string",
          "status:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_add_keyword",
        "description": "Add a keyword criterion to an ad group (ad_group_criterion: keyword.text + keyword.match_type BROAD/PHRASE/EXACT, cpc_bid_micros). WRITE.",
        "category": "keywords",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/adGroupCriteria:mutate",
        "args": [
          "customer_id:string",
          "ad_group_resource:string",
          "keyword_text:string",
          "match_type:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_add_negative_keyword",
        "description": "Add a negative keyword to an ad group or campaign (ad_group_criterion / campaign_criterion with negative=true) to exclude search terms. WRITE.",
        "category": "keywords",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/adGroupCriteria:mutate",
        "args": [
          "customer_id:string",
          "ad_group_resource:string",
          "keyword_text:string",
          "match_type:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_remove_keyword",
        "description": "Remove a keyword criterion from an ad group — a remove operation on adGroupCriteria/{ad_group_id}~{criterion_id}. WRITE.",
        "category": "keywords",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}/adGroupCriteria:mutate",
        "args": [
          "customer_id:string",
          "ad_group_id:string",
          "criterion_id:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "write"
      },
      {
        "name": "google_ads_generate_keyword_ideas",
        "description": "Get keyword ideas + search-volume/competition/bid estimates from the Keyword Planner (KeywordPlanIdeaService) for seed keywords or a URL. Read-only planning tool.",
        "category": "planning",
        "method": "POST",
        "endpoint": "https://googleads.googleapis.com/v17/customers/{customer_id}:generateKeywordIdeas",
        "args": [
          "customer_id:string",
          "keyword_seed:string",
          "language:string",
          "geo_target:string"
        ],
        "scopes": "https://www.googleapis.com/auth/adwords",
        "kind": "read"
      }
    ]
  },
  "snapchat": {
    "substrate": "bos_bridge",
    "display_name": "Snapchat",
    "tools": [
      {
        "name": "snapchat_list_organizations",
        "description": "List the business organizations the connected user can access (top of the Ads API hierarchy). Returns org id, name, type, and roles — the entry point to discover ad accounts.",
        "category": "account",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/me/organizations",
        "args": [],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_list_ad_accounts",
        "description": "List all ad accounts under an organization. Returns ad_account id, name, currency, timezone, funding source, and status — needed as the parent id for campaigns, audiences, catalogs, and stats.",
        "category": "account",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/organizations/{organization_id}/adaccounts",
        "args": [
          "organization_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_get_ad_account",
        "description": "Get one ad account by id — full details including status, currency, timezone, funding sources, and advertiser info.",
        "category": "account",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}",
        "args": [
          "ad_account_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_list_campaigns",
        "description": "List all campaigns in an ad account. Returns campaign id, name, status (ACTIVE/PAUSED), objective, daily/lifetime budget, and start/end times.",
        "category": "campaigns",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/campaigns",
        "args": [
          "ad_account_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_create_campaign",
        "description": "Create a new advertising campaign in an ad account. Body carries campaigns[] with name, status, objective, and optional start_time/end_time and lifetime/daily budget micro amounts.",
        "category": "campaigns",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/campaigns",
        "args": [
          "ad_account_id:string",
          "name:string",
          "status:string",
          "start_time:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_update_campaign",
        "description": "Update existing campaigns (name, status pause/resume, budget, schedule). PUT carries campaigns[] each with the campaign id and changed fields.",
        "category": "campaigns",
        "method": "PUT",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/campaigns",
        "args": [
          "ad_account_id:string",
          "id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_delete_campaign",
        "description": "Permanently delete a campaign by id (also removes its child ad squads and ads). Destructive.",
        "category": "campaigns",
        "method": "DELETE",
        "endpoint": "https://adsapi.snapchat.com/v1/campaigns/{campaign_id}",
        "args": [
          "campaign_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_list_ad_squads",
        "description": "List ad squads (ad sets) under a campaign — the targeting + budget + bid + schedule layer. Returns squad id, name, status, targeting spec, bid_micro, and optimization_goal.",
        "category": "ad_squads",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/campaigns/{campaign_id}/adsquads",
        "args": [
          "campaign_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_create_ad_squad",
        "description": "Create an ad squad (ad set) under a campaign with targeting, placement, bid strategy, optimization goal, budget, and schedule. Body carries adsquads[].",
        "category": "ad_squads",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/campaigns/{campaign_id}/adsquads",
        "args": [
          "campaign_id:string",
          "name:string",
          "type:string",
          "targeting:object",
          "bid_micro:string",
          "billing_event:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_update_ad_squad",
        "description": "Update ad squads (pause/resume via status, change bid, budget, targeting, or schedule). PUT carries adsquads[] each with the squad id and changed fields.",
        "category": "ad_squads",
        "method": "PUT",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/adsquads",
        "args": [
          "ad_account_id:string",
          "id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_list_ads",
        "description": "List ads under an ad squad. Returns ad id, name, status, creative_id, review_status, and type.",
        "category": "ads",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/adsquads/{ad_squad_id}/ads",
        "args": [
          "ad_squad_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_create_ad",
        "description": "Create an ad inside an ad squad, binding a creative to the squad. Body carries ads[] with name, status, creative_id, and type.",
        "category": "ads",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/adsquads/{ad_squad_id}/ads",
        "args": [
          "ad_squad_id:string",
          "name:string",
          "status:string",
          "creative_id:string",
          "type:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_update_ad",
        "description": "Update ads (pause/resume via status, swap creative, rename). PUT carries ads[] each with the ad id and changed fields.",
        "category": "ads",
        "method": "PUT",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/ads",
        "args": [
          "ad_account_id:string",
          "id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_list_creatives",
        "description": "List creatives in an ad account (the renderable ad units — Single Image/Video, Story, Collection, etc.). Returns creative id, name, type, headline, and linked media/top-snap ids.",
        "category": "creatives",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/creatives",
        "args": [
          "ad_account_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_create_creative",
        "description": "Create a creative in an ad account from uploaded media (top_snap_media_id) plus type, headline, brand_name, and call_to_action / attachment. Body carries creatives[].",
        "category": "creatives",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/creatives",
        "args": [
          "ad_account_id:string",
          "name:string",
          "type:string",
          "top_snap_media_id:string",
          "headline:string",
          "brand_name:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_create_media",
        "description": "Register a media container (IMAGE or VIDEO) in an ad account. Returns a media id used by the upload step and then referenced by a creative. Body carries media[] with name, type, ad_account_id.",
        "category": "media",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/media",
        "args": [
          "ad_account_id:string",
          "name:string",
          "type:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_upload_media_file",
        "description": "Upload the actual asset bytes to a registered media id (multipart/form-data file field). Small files use this single-part endpoint; large videos use the chunked /media/{id}/multipart flow.",
        "category": "media",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/media/{media_id}/upload",
        "args": [
          "media_id:string",
          "file:binary"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_list_media",
        "description": "List media assets in an ad account with upload/processing status (PENDING_UPLOAD/READY) and file metadata (type, dimensions, duration).",
        "category": "media",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/media",
        "args": [
          "ad_account_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_get_campaign_stats",
        "description": "Get performance stats for a campaign — impressions, spend, swipes, conversions, etc. TOTAL over a window, or time-series with granularity=DAY/HOUR plus start_time/end_time; fields chosen via 'fields'.",
        "category": "stats",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/campaigns/{campaign_id}/stats",
        "args": [
          "campaign_id:string",
          "granularity:string",
          "start_time:string",
          "end_time:string",
          "fields:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_get_ad_account_stats",
        "description": "Get account-level rollup stats (spend, impressions, swipes, conversions) for an ad account over a window — TOTAL or time-series with granularity + start_time/end_time.",
        "category": "stats",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/stats",
        "args": [
          "ad_account_id:string",
          "granularity:string",
          "fields:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_get_ad_stats",
        "description": "Get per-ad performance stats (impressions, spend, swipe-ups, video views, conversions) — TOTAL or time-series. Use to compare creatives head-to-head.",
        "category": "stats",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/ads/{ad_id}/stats",
        "args": [
          "ad_id:string",
          "granularity:string",
          "fields:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_list_audience_segments",
        "description": "List Snap Audience Match (SAM) audience segments in an ad account — the 'audiences' surface. Returns segment id, name, source_type, status, and approximate size.",
        "category": "audiences",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/segments",
        "args": [
          "ad_account_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_create_audience_segment",
        "description": "Create a SAM audience segment (e.g. customer-list / engagement audience) in an ad account. Body carries segments[] with name, source_type, retention_in_days, ad_account_id.",
        "category": "audiences",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/adaccounts/{ad_account_id}/segments",
        "args": [
          "ad_account_id:string",
          "name:string",
          "source_type:string",
          "retention_in_days:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_add_audience_users",
        "description": "Add hashed user identifiers (email/phone/IDFA/GAID, SHA-256) to a SAM segment for customer-list matching. Body carries users[] with schema + hashed data.",
        "category": "audiences",
        "method": "POST",
        "endpoint": "https://adsapi.snapchat.com/v1/segments/{segment_id}/users",
        "args": [
          "segment_id:string",
          "schema:array",
          "data:array"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "write"
      },
      {
        "name": "snapchat_list_catalogs",
        "description": "List product catalogs owned by an organization (for Dynamic Ads / Collection ads). Returns catalog id, name, source, and product count.",
        "category": "catalogs",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/organizations/{organization_id}/catalogs",
        "args": [
          "organization_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_get_targeting_options",
        "description": "Look up available targeting dimension values (interests, demographics, geo, devices) to build an ad squad's targeting spec — e.g. list interest categories under the SL012 taxonomy.",
        "category": "targeting",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/targeting/interests/{taxonomy}",
        "args": [
          "taxonomy:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      },
      {
        "name": "snapchat_get_funding_sources",
        "description": "List an organization's funding sources (credit cards, lines of credit, coupons) with balance/spend-cap details — needed to understand ad-account budget capacity.",
        "category": "billing",
        "method": "GET",
        "endpoint": "https://adsapi.snapchat.com/v1/organizations/{organization_id}/fundingsources",
        "args": [
          "organization_id:string"
        ],
        "scopes": "snapchat-marketing-api",
        "kind": "read"
      }
    ]
  },
  "ebay": {
    "substrate": "bos_bridge",
    "display_name": "eBay",
    "tools": [
      {
        "name": "ebay_browse_search_items",
        "description": "Search the eBay marketplace catalog for live listings by keyword, category, or filter (Browse API). Returns item summaries with itemId, title, price, condition, seller.",
        "category": "browse",
        "method": "GET",
        "endpoint": "https://api.ebay.com/buy/browse/v1/item_summary/search?q={q}&category_ids={category_ids}&filter={filter}&limit={limit}&offset={offset}",
        "args": [
          "q:string",
          "category_ids:string",
          "filter:string",
          "limit:string",
          "offset:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope (application token; Browse works with app-level OAuth)",
        "kind": "read"
      },
      {
        "name": "ebay_browse_get_item",
        "description": "Get full details for one marketplace listing by eBay item ID (Browse API) — description, aspects, images, price, shipping, seller, availability.",
        "category": "browse",
        "method": "GET",
        "endpoint": "https://api.ebay.com/buy/browse/v1/item/{item_id}",
        "args": [
          "item_id:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope",
        "kind": "read"
      },
      {
        "name": "ebay_list_inventory",
        "description": "List the seller's active inventory items / product listings (Inventory API). Returns SKU, title, quantity, condition, pricing. WIRED today via /ebay/call op list_inventory.",
        "category": "inventory",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/inventory_item?limit={limit}&offset={offset}",
        "args": [
          "limit:string",
          "offset:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_get_inventory_item",
        "description": "Get one inventory item / listing by seller SKU (Inventory API). WIRED today via /ebay/call op get_inventory_item.",
        "category": "inventory",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}",
        "args": [
          "sku:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_create_or_update_inventory_item",
        "description": "Create or replace an inventory item record by SKU — product aspects, condition, quantity, images (Inventory API, full-resource PUT). Server proxy exists in ebay-adapter.ts (PUT inventory_item) but is not yet a /ebay/call",
        "category": "inventory",
        "method": "PUT",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}",
        "args": [
          "sku:string",
          "product:object",
          "condition:string",
          "availability:object"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "kind": "write"
      },
      {
        "name": "ebay_create_offer",
        "description": "Create an offer that ties an inventory item (SKU) to price, marketplace, category, listing policies — the sellable listing draft (Inventory API). Returns offerId. (needs proxy op)",
        "category": "inventory",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/offer",
        "args": [
          "sku:string",
          "marketplaceId:string",
          "format:string",
          "pricingSummary:object",
          "categoryId:string",
          "listingPolicies:object"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "kind": "write"
      },
      {
        "name": "ebay_publish_offer",
        "description": "Publish an offer to make it a live eBay listing, returning the listingId (Inventory API). This is the action that puts an item on sale. (needs proxy op)",
        "category": "inventory",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/publish",
        "args": [
          "offer_id:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "kind": "write"
      },
      {
        "name": "ebay_get_offers",
        "description": "List offers for a given SKU (Inventory API) — shows price, status (PUBLISHED/UNPUBLISHED), listingId, marketplace. (needs proxy op)",
        "category": "inventory",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/offer?sku={sku}&marketplace_id={marketplace_id}&limit={limit}&offset={offset}",
        "args": [
          "sku:string",
          "marketplace_id:string",
          "limit:string",
          "offset:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_withdraw_offer",
        "description": "End a single published listing by withdrawing its offer (Inventory API) — removes the item from sale but keeps the offer for relisting. (needs proxy op)",
        "category": "inventory",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/withdraw",
        "args": [
          "offer_id:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "kind": "write"
      },
      {
        "name": "ebay_bulk_update_price_quantity",
        "description": "Bulk-update price and available quantity across up to 25 SKUs/offers in one call (Inventory API) — repricing and restock. (needs proxy op)",
        "category": "inventory",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/bulk_update_price_quantity",
        "args": [
          "requests:array"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "kind": "write"
      },
      {
        "name": "ebay_list_inventory_locations",
        "description": "List the seller's inventory / fulfillment locations — warehouses and stores used for ship-from and in-store pickup (Inventory API). (needs proxy op)",
        "category": "inventory",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/location?limit={limit}&offset={offset}",
        "args": [
          "limit:string",
          "offset:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_create_inventory_location",
        "description": "Create a merchant inventory location (warehouse/store) by merchantLocationKey — required before publishing offers that ship from it (Inventory API). (needs proxy op)",
        "category": "inventory",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/inventory/v1/location/{merchant_location_key}",
        "args": [
          "merchant_location_key:string",
          "location:object",
          "name:string",
          "merchantLocationStatus:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "kind": "write"
      },
      {
        "name": "ebay_list_seller_orders",
        "description": "List recent buyer orders for the seller (Fulfillment API) — order IDs, buyer, line items, totals, fulfillment status. Supports filter expressions. WIRED today via /ebay/call op list_seller_orders.",
        "category": "orders",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/fulfillment/v1/order?limit={limit}&filter={filter}",
        "args": [
          "limit:string",
          "filter:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_get_order",
        "description": "Get full details for one order by order ID (Fulfillment API) — line items, pricing, buyer, shipping address, payment, fulfillment status. WIRED today via /ebay/call op get_order.",
        "category": "orders",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/fulfillment/v1/order/{order_id}",
        "args": [
          "order_id:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_create_shipping_fulfillment",
        "description": "Mark order line items shipped by creating a shipping fulfillment with tracking number and carrier (Fulfillment API) — this is the ship-confirm / tracking-upload action. (needs proxy op)",
        "category": "orders",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/fulfillment/v1/order/{order_id}/shipping_fulfillment",
        "args": [
          "order_id:string",
          "lineItems:array",
          "trackingNumber:string",
          "shippingCarrierCode:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
        "kind": "write"
      },
      {
        "name": "ebay_get_shipping_fulfillments",
        "description": "List all shipping fulfillments (shipments + tracking) recorded against one order (Fulfillment API). (needs proxy op)",
        "category": "orders",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/fulfillment/v1/order/{order_id}/shipping_fulfillment",
        "args": [
          "order_id:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_issue_refund",
        "description": "Issue a full or partial refund against an order (Fulfillment API) — buyer reimbursement for returns/cancellations. (needs proxy op)",
        "category": "orders",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/fulfillment/v1/order/{order_id}/issue_refund",
        "args": [
          "order_id:string",
          "reasonForRefund:string",
          "refundItems:array",
          "orderLevelRefundAmount:object"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
        "kind": "write"
      },
      {
        "name": "ebay_get_seller_standards_profile",
        "description": "Get the seller standards / performance profile (Analytics API) — seller level (Top Rated/Above Standard), transaction defect rate, late shipment rate. WIRED today via /ebay/call op get_seller_analytics.",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/analytics/v1/seller_standards_profile",
        "args": [],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_get_traffic_report",
        "description": "Get the listing traffic report (Analytics API) — impressions, click-through, listing views, sales conversion over a date range and dimension. (needs proxy op)",
        "category": "analytics",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/analytics/v1/traffic_report?dimension={dimension}&metric={metric}&filter={filter}",
        "args": [
          "dimension:string",
          "metric:string",
          "filter:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_list_ad_campaigns",
        "description": "List Promoted Listings ad campaigns (Marketing API) — name, status, funding model, budget, dates. WIRED today via /ebay/call op list_campaigns.",
        "category": "marketing",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/marketing/v1/ad_campaign?campaign_status={status}&limit={limit}",
        "args": [
          "status:string",
          "limit:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_get_ad_campaign",
        "description": "Get one Promoted Listings ad campaign by campaign ID (Marketing API). WIRED today via /ebay/call op get_campaign.",
        "category": "marketing",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/marketing/v1/ad_campaign/{campaign_id}",
        "args": [
          "campaign_id:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_create_ad_campaign",
        "description": "Create a Promoted Listings ad campaign (Marketing API) — funding model (COST_PER_SALE), budget, marketplace, start/end dates. (needs proxy op)",
        "category": "marketing",
        "method": "POST",
        "endpoint": "https://api.ebay.com/sell/marketing/v1/ad_campaign",
        "args": [
          "campaignName:string",
          "marketplaceId:string",
          "fundingStrategy:object",
          "startDate:string",
          "endDate:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.marketing",
        "kind": "write"
      },
      {
        "name": "ebay_list_promotions",
        "description": "List seller marketing promotions (Marketing API) — discount codes, order discounts, volume pricing, sale events. WIRED today via /ebay/call op list_promotions.",
        "category": "marketing",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/marketing/v1/promotion?marketplace_id={marketplace_id}&limit={limit}",
        "args": [
          "marketplace_id:string",
          "limit:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_get_promotion",
        "description": "Get one marketing promotion by promotion ID (Marketing API). WIRED today via /ebay/call op get_promotion.",
        "category": "marketing",
        "method": "GET",
        "endpoint": "https://api.ebay.com/sell/marketing/v1/promotion/{promotion_id}",
        "args": [
          "promotion_id:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
        "kind": "read"
      },
      {
        "name": "ebay_get_category_suggestions",
        "description": "Get suggested leaf categories for a product query from the default category tree (Commerce Taxonomy API) — needed to pick the categoryId when creating an offer. (needs proxy op; also needs a get_default_category_tree_id ",
        "category": "catalog",
        "method": "GET",
        "endpoint": "https://api.ebay.com/commerce/taxonomy/v1/category_tree/{category_tree_id}/get_category_suggestions?q={q}",
        "args": [
          "category_tree_id:string",
          "q:string"
        ],
        "scopes": "https://api.ebay.com/oauth/api_scope",
        "kind": "read"
      }
    ]
  }
}

# ── helpers + honest-by-construction executor ────────────────────────────────
import json
import re as _re

_URL_ARG_BAD = _re.compile(r"[?#%\\s]|\\.\\.")


def _norm(slug):
    return (slug or "").strip().lower()


def _ph(tpl):
    return _re.findall(r"\\{([a-zA-Z0-9_]+)\\}", tpl or "")


def _argname(a):
    return str(a).split(":", 1)[0].strip()


def catalog_for(slug):
    return CHANNEL_TOOL_CATALOG.get(_norm(slug))


def tool_count(slug):
    c = catalog_for(slug)
    return len(c["tools"]) if c else 0


def tool_names(slug):
    c = catalog_for(slug)
    return [t["name"] for t in c["tools"]] if c else []


def find_tool(slug, name):
    c = catalog_for(slug)
    if not c:
        return None
    for t in c["tools"]:
        if t["name"] == name:
            return t
    return None


def has_tool(slug, name):
    return find_tool(slug, name) is not None


def all_catalog_slugs():
    return list(CHANNEL_TOOL_CATALOG.keys())


# ── Real liveness probe ──────────────────────────────────────────────────────
# Read-tool heuristic + a genuine per-connector ping, mirroring
# nx_mcp_tools._health_probe. /connected uses this so channel/commerce connectors
# show LIVE only when a real tool call reached their provider — not a blind label.
_LIVE_READ_HINTS = ("list", "get_", "_get", "search", "me", "current", "status",
                    "connected", "whoami", "profile", "account", "orgs", "projects",
                    "teams", "bases", "boards", "spaces", "info", "fetch", "read",
                    "show", "recent", "self", "user")
_LIVE_WRITE = ("post", "send", "create", "delete", "update", "upload", "publish",
               "charge", "remove", "reply", "quote", "add_", "init", "cancel",
               "pause", "resume", "archive", "draft", "set_", "start", "stop")


def _read_tool_candidates(names, limit=4):
    """Rank non-destructive read tools to probe with (best first). Returns a short
    list so live_ping can retry when a picked tool is unmapped on a partial op-map."""
    ranked, seen = [], set()
    for n in names:  # explicit read verbs first
        low = (n or "").lower()
        if any(k in low for k in _LIVE_READ_HINTS) and not any(w in low for w in _LIVE_WRITE):
            if n not in seen:
                ranked.append(n); seen.add(n)
    for n in names:  # then any other non-write tool
        if not any(w in (n or "").lower() for w in _LIVE_WRITE) and n not in seen:
            ranked.append(n); seen.add(n)
    if not ranked and names:
        ranked = [names[0]]
    return ranked[:limit]


def _first_read_tool(names):
    """Single best read tool to probe with (kept for callers/tests)."""
    c = _read_tool_candidates(names, limit=1)
    return c[0] if c else None


def _channel_display_name(slug):
    c = catalog_for(slug)
    if c:
        for k in ("label", "name", "display", "title"):
            v = c.get(k)
            if v:
                return str(v)
    return _norm(slug).replace("_", " ").title()


def live_ping(slug):
    """Fire ONE non-destructive read tool through the connector's real substrate and
    classify liveness. Returns a row shaped like nx_mcp_tools._health_probe:
      {"slug","name","status": "live"|"notconnected"|"reconnect"|"down","tools","hint"}.
    A provider response — data, a param-validation reply, or the
    UNTRUSTED_INTEGRATION_DATA wall — means the connector reached its provider == LIVE.
    'not_connected' == the platform is not linked yet. HONEST: never fakes live."""
    names = tool_names(slug)
    total = len(names)
    disp = _channel_display_name(slug)
    if not names:
        return {"slug": slug, "name": disp, "status": "down", "tools": 0, "hint": "no tools"}

    def _row(status, hint=""):
        return {"slug": slug, "name": disp, "status": status, "tools": total, "hint": hint}

    last = _row("down", "no probe")
    for read in _read_tool_candidates(names):
        try:
            r = call(slug, read, {})
        except Exception as e:
            last = _row("down", "%s: %s" % (type(e).__name__, str(e)[:40]))
            continue
        if isinstance(r, dict) and r.get("ok") is True:
            return _row("live")
        body = str(r.get("detail") or r.get("error") or r.get("body") or "") if isinstance(r, dict) else str(r)
        low = body.lower()
        # Reached the provider (validation/wall) → live.
        if ("missing_arg" in low or "missing_param" in low or "required" in low
                or "untrusted_integration_data" in low or "needs_input" in low
                or "provide" in low):
            return _row("live")
        if "not_connected" in low or "not connected" in low:
            return _row("notconnected", "connect the platform")
        if ("401" in body or "unauthor" in low or "expired" in low
                or "not_authenticated" in low or "not authenticated" in low
                or "reconnect" in low or "re-connect" in low):
            return _row("reconnect", "/integrations %s" % _norm(slug))
        # This specific candidate tool isn't wired (partial op-map, or its dispatch route/op
        # isn't mapped) — record it and try the NEXT candidate read tool. If every candidate is
        # unwired, `last` carries the honest reason and we fall through to it.
        if ("unknown_tool" in low or "server_dispatch_pending" in low
                or "bos_proxy_pending" in low or "dispatch_route_not_deployed" in low
                or "bos_proxy_not_deployed" in low or "not wired" in low):
            last = _row("down", body[:44] or "tool not wired")
            continue
        # pending substrate / config gap (missing dev token, etc.)
        last = _row("down", body[:44])
    return last


def _load_local_token(slug):
    try:
        import nx_channels
        conn = nx_channels.connector_for_service(slug)
        t = conn._load_token() if (conn is not None and hasattr(conn, "_load_token")) else None
        return (t or {}).get("access_token") if isinstance(t, dict) else None
    except Exception:
        return None


def _call_local(slug, spec, args):
    """Direct local-token API call (X). Honest: returns the REAL HTTP result, never a fake success."""
    import requests
    tok = _load_local_token(slug)
    if not tok:
        return {"ok": False, "detail": "not_connected", "hint": "connect %s first" % slug}
    need = [_argname(a) for a in spec.get("args", [])]
    missing = [k for k in need if not str(args.get(k, "")).strip()]
    if missing:
        return {"ok": False, "detail": "missing_arg:" + ",".join(missing)}
    url = spec["endpoint"]
    placeholders = _ph(url)
    for k in placeholders:
        v = str(args.get(k, ""))
        if _URL_ARG_BAD.search(v):
            return {"ok": False, "detail": "bad_arg:%s" % k}
    try:
        url = url.format(**{k: args.get(k, "") for k in placeholders})
    except Exception:
        return {"ok": False, "detail": "bad_url_args"}
    method = spec.get("method", "GET").upper()
    body = {k: v for k, v in args.items() if k not in placeholders}
    headers = {"Authorization": "Bearer " + tok, "Content-Type": "application/json"}
    try:
        kw = {"headers": headers, "timeout": 25}
        if method == "GET":
            kw["params"] = body
        elif body:
            kw["json"] = body
        r = requests.request(method, url, **kw)
        try:
            data = r.json() if r.content else {}
        except Exception:
            data = {}
        if 200 <= r.status_code < 300:
            return {"ok": True, "status": r.status_code, "text": (r.text or "")[:1200]}
        detail = "http_%d" % r.status_code
        if isinstance(data, dict) and (data.get("title") or data.get("detail") or data.get("errors")):
            detail = "%s:%s" % (detail, str(data.get("title") or data.get("detail") or data.get("errors"))[:120])
        return {"ok": False, "detail": detail, "body": (r.text or "")[:300]}
    except Exception as e:
        return {"ok": False, "detail": "request_failed:%s" % type(e).__name__}


def _call_shared_oauth(slug, spec, args):
    """Never look for a second local token after a shared-vault connect."""
    try:
        import nx_channels
        connector = nx_channels.connector_for_service(slug)
        if connector is None or not connector.is_connected():
            return {"ok": False, "detail": "not_connected",
                    "hint": "connect %s once in Nexplora or NX" % slug}
    except Exception:
        return {"ok": False, "detail": "connection_status_unavailable"}
    return {
        "ok": False,
        "detail": "server_execution_not_available",
        "hint": "%s is connected in the shared Nexplora vault, but this scoped provider action is not enabled yet" % slug,
    }


# BOS-bridged apps whose scoped /api/business-os/<app>/call proxy is DEPLOYED (or deploy-pending on an open PR).
# Listing an app here routes it to the server. This is SAFE even before the route ships: _call_bos trusts ONLY
# our proxy's JSON envelope ({ok,status,data}) — a non-existent path returns the SPA-fallback (HTML, no 'ok' key),
# which _call_bos reports as honest "bos_proxy_not_deployed", never a fake success. So an app added here while its
# route is still in review goes live automatically the moment that route deploys, with zero further CLI change.
#   meta / google_ads: proxies added in nexplora-v2 PR #312 (Meta Graph v20 + Google Ads v17). Live on merge;
#   honest-pending until then. Both require operator platform grants (Meta App Review / Google Ads dev token).
_BOS_PROXY_LIVE = {"ebay", "youtube", "tiktok", "meta", "google_ads"}


def _call_bos(slug, spec, args):
    """BOS-bridged apps: the token is SERVER-SIDE, so execution goes through a scoped Nexplora BOS proxy
    (POST /api/business-os/<app>/call {operation, params}). eBay routes via nx_ebay_tools; YouTube (+ future
    apps) route generically. Bridged apps WITHOUT a deployed proxy return honest 'bos_proxy_pending' WITHOUT
    calling — and even for a live app, only a proper JSON {ok:true} from the proxy counts as success, so a
    200 SPA-fallback on a not-yet-deployed route is NEVER misread as success. Never fakes."""
    s = _norm(slug)
    if s == "ebay":
        try:
            import nx_ebay_tools
            return nx_ebay_tools.call(spec["name"], args)  # its 9 deployed tools execute; unknown names get an honest server error
        except Exception as e:
            return {"ok": False, "detail": "ebay_proxy_error:%s" % type(e).__name__}
    if s not in _BOS_PROXY_LIVE:
        return {"ok": False, "detail": "bos_proxy_pending",
                "hint": "%s's token is server-side (Nexplora BOS); its /api/business-os/%s/call proxy isn't deployed yet" % (slug, s)}
    # Live proxy: POST {operation, params}. The operation is the catalog tool name; the server maps it to the API.
    import requests
    try:
        import nx_message
        base = nx_message._auth_base()
        cfg = nx_message._load_config() or {}
    except Exception:
        import os
        base = os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"
        cfg = {}
    token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
    if not token:
        return {"ok": False, "detail": "not_signed_in"}
    try:
        r = requests.post(base.rstrip("/") + "/api/business-os/%s/call" % s,
                          json={"operation": spec["name"], "params": args},
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=30)
        try:
            d = r.json() if r.content else {}
        except Exception:
            d = None
        # Only OUR proxy's JSON envelope ({ok, status, data, error?}) is trusted. A non-JSON body or a missing
        # 'ok' key means the route isn't really answering (SPA-fallback / not deployed) — never fake success.
        if not isinstance(d, dict) or "ok" not in d:
            return {"ok": False, "detail": "bos_proxy_not_deployed",
                    "hint": "%s's /api/business-os/%s/call isn't returning the proxy JSON yet (deploy pending)" % (slug, s)}
        if d.get("ok"):
            return {"ok": True, "status": d.get("status"), "text": json.dumps(d.get("data"))[:1200]}
        return {"ok": False, "detail": d.get("error") or ("http_%d" % r.status_code),
                "body": json.dumps(d.get("data") or {})[:300]}
    except Exception as e:
        return {"ok": False, "detail": "request_failed:%s" % type(e).__name__}


# Google Workspace tools whose personal server route is DEPLOYED. Same fake-proofing as _BOS_PROXY_LIVE:
# _call_dispatch trusts ONLY the route's {ok,...} JSON envelope, so an un-deployed route (SPA-fallback) is
# reported as honest "dispatch_route_not_deployed", never a fake success. Route mints the per-send approval
# server-side (the operator's explicit send IS the approval), so the CLI does not send the `approval` arg.
#   gmail_send_message -> /api/personal/gmail-send (nexplora-v2 PR #327). Live once merged AND the operator
#   reconnects Google in NX so the token carries gmail.send (google config.ts now requests it at connect).
_DISPATCH_ROUTES = {
    "gmail_send_message": "/api/personal/gmail-send",
    # Full e2e Gmail client — one route, N ops (op carried in the payload). Live once nexplora-v2 PR #337
    # deploys AND the operator reconnects Google granting gmail.modify (+ gmail.settings.basic for filters).
    "gmail_crud": "/api/personal/gmail",
    # Full e2e Google Workspace clients — one route per service, N ops (op carried in the payload). Same fake-proof
    # {ok} envelope as gmail_crud: an un-deployed route is honest-pending, never a fabricated success. Live once the
    # matching nexplora-v2 personal route deploys AND the operator reconnects Google granting the service scope
    # (calendar.events / drive / documents / spreadsheets). DIRECT built-ins — NOT on any 'USER'/'google' server.
    "calendar_crud": "/api/personal/google-calendar",
    "drive_crud": "/api/personal/google-drive",
    "docs_crud": "/api/personal/google-docs",
    "sheets_crud": "/api/personal/google-sheets",
    "google_chat_crud": "/api/personal/google-chat",
    "google_meet_crud": "/api/personal/google-meet",
    "google_forms_crud": "/api/personal/google-forms",
    "google_tasks_crud": "/api/personal/google-tasks",
    # Bespoke personal connectors — Slack / Twilio / Calendly / Typeform, one route per provider, N ops (op
    # carried in the payload). Same fake-proof {ok} envelope: an un-deployed route is honest-pending, never a
    # fabricated success. Live once the matching nexplora-v2 personal route deploys AND the operator connects
    # the provider (BYOK). DIRECT built-ins — NOT on any 'USER'/'slack'/'twilio'/'calendly'/'typeform' server.
    "slack_crud": "/api/personal/slack",
    "twilio_crud": "/api/personal/twilio",
    "calendly_crud": "/api/personal/calendly",
    "typeform_crud": "/api/personal/typeform",
    # Bespoke personal connectors — Notion / Dropbox / Airtable, one route per provider, N ops (op carried in the
    # payload). Same fake-proof {ok} envelope: an un-deployed route is honest-pending, never a fabricated success.
    # Live once the matching nexplora-v2 personal route deploys AND the operator connects the provider (BYOK OAuth).
    # DIRECT built-ins — NOT on any 'USER'/'notion'/'dropbox'/'airtable' server.
    "notion_crud": "/api/personal/notion",
    "dropbox_crud": "/api/personal/dropbox",
    "airtable_crud": "/api/personal/airtable",
    "confluence_crud": "/api/personal/confluence",
    "box_crud": "/api/personal/box",
    "onedrive_crud": "/api/personal/onedrive",
    "coda_crud": "/api/personal/coda",
    "sharepoint_crud": "/api/personal/sharepoint",
    "smartsheet_crud": "/api/personal/smartsheet",
    "jira_crud": "/api/personal/jira",
    "linear_crud": "/api/personal/linear",
    "monday_crud": "/api/personal/monday",
    "asana_crud": "/api/personal/asana",
    "trello_crud": "/api/personal/trello",
    "zoom_crud": "/api/personal/zoom",
    "miro_crud": "/api/personal/miro",
    "height_crud": "/api/personal/height",
    "youtrack_crud": "/api/personal/youtrack",
    "github_crud": "/api/personal/github",
    "gitlab_crud": "/api/personal/gitlab",
    "vercel_crud": "/api/personal/vercel",
    "cloudflare_crud": "/api/personal/cloudflare",
    "supabase_crud": "/api/personal/supabase",
    "netlify_crud": "/api/personal/netlify",
    "sentry_crud": "/api/personal/sentry",
    "pagerduty_crud": "/api/personal/pagerduty",
    "launchdarkly_crud": "/api/personal/launchdarkly",
    "atlas_crud": "/api/personal/atlas",
    "planetscale_crud": "/api/personal/planetscale",
    "neon_crud": "/api/personal/neon",
    "digitalocean_crud": "/api/personal/digitalocean",
    "fly_crud": "/api/personal/fly",
    "render_crud": "/api/personal/render",
    "railway_crud": "/api/personal/railway",
    "heroku_crud": "/api/personal/heroku",
    "newrelic_crud": "/api/personal/newrelic",
    "datadog_crud": "/api/personal/datadog",
    "grafana_crud": "/api/personal/grafana",
    "opsgenie_crud": "/api/personal/opsgenie",
    "snowflake_crud": "/api/personal/snowflake",
    "databricks_crud": "/api/personal/databricks",
    "bigquery_crud": "/api/personal/bigquery",
    "servicenow_crud": "/api/personal/servicenow",
    "terraform_crud": "/api/personal/terraform",
    "upstash_crud": "/api/personal/upstash",
    "outlook_crud": "/api/personal/outlook",
    "outlook_calendar_crud": "/api/personal/outlook-calendar",
    "teams_crud": "/api/personal/teams",
    "excel_crud": "/api/personal/excel",
    "word_crud": "/api/personal/word",
    "powerpoint_crud": "/api/personal/powerpoint",
    "onenote_crud": "/api/personal/onenote",
    "bookings_crud": "/api/personal/bookings",
    "bitbucket_crud": "/api/personal/bitbucket",
    "circleci_crud": "/api/personal/circleci",
    "split_crud": "/api/personal/split",
    "anthropic_crud": "/api/personal/anthropic",
    "openai_crud": "/api/personal/openai",
    "mistral_crud": "/api/personal/mistral",
    "cohere_crud": "/api/personal/cohere",
    "huggingface_crud": "/api/personal/huggingface",
    "gemini_crud": "/api/personal/gemini",
    "replicate_crud": "/api/personal/replicate",
    "elevenlabs_crud": "/api/personal/elevenlabs",
    "together_crud": "/api/personal/together",
    "groq_crud": "/api/personal/groq",
    "openrouter_crud": "/api/personal/openrouter",
    "stability_crud": "/api/personal/stability",
    "fireworks_crud": "/api/personal/fireworks",
    "mailchimp_crud": "/api/personal/mailchimp",
    "klaviyo_crud": "/api/personal/klaviyo",
    "sendgrid_crud": "/api/personal/sendgrid",
    "buffer_crud": "/api/personal/buffer",
    "stripe_crud": "/api/personal/stripe",
    "shopify_crud": "/api/personal/shopify",
    "quickbooks_crud": "/api/personal/quickbooks",
    "xero_crud": "/api/personal/xero",
    "auth0_crud": "/api/personal/auth0",
    "okta_crud": "/api/personal/okta",
    "clerk_crud": "/api/personal/clerk",
    "vanta_crud": "/api/personal/vanta",
    "zendesk_crud": "/api/personal/zendesk",
    "intercom_crud": "/api/personal/intercom",
    "freshdesk_crud": "/api/personal/freshdesk",
    "front_crud": "/api/personal/front",
    "hubspot_crud": "/api/personal/hubspot",
    "salesforce_crud": "/api/personal/salesforce",
    "pipedrive_crud": "/api/personal/pipedrive",
    "posthog_crud": "/api/personal/posthog",
    "figma_crud": "/api/personal/figma",
    "greenhouse_crud": "/api/personal/greenhouse",
    "docusign_crud": "/api/personal/docusign",
    "discord_crud": "/api/personal/discord",
    "mixpanel_crud": "/api/personal/mixpanel",
    "amplitude_crud": "/api/personal/amplitude",
    "segment_crud": "/api/personal/segment",
    "lever_crud": "/api/personal/lever",
    "convertkit_crud": "/api/personal/convertkit",
    "canva_crud": "/api/personal/canva",
    "pulumi_crud": "/api/personal/pulumi",
    "hootsuite_crud": "/api/personal/hootsuite",
    "bamboohr_crud": "/api/personal/bamboohr",
    "workable_crud": "/api/personal/workable",
    "komodor_crud": "/api/personal/komodor",
    "beehiiv_crud": "/api/personal/beehiiv",
}


# Individual Google Workspace catalog tools → (personal route, the route's own op). The catalog explodes
# each service into per-op tools (gmail_list_messages) while each route takes {op, …params}; this table is
# the bridge. Tools with NO matching route op (e.g. gmail_get_profile — the gmail route has no 'profile'
# case) are intentionally OMITTED so they stay honest-pending rather than fake a call. Read probes for
# /connected fire the mapped read tools; writes carry the operator's explicit action (route mints approval).
_DISPATCH_TOOL_MAP = {
    "gmail_list_messages":       ("/api/personal/gmail", "list"),
    "gmail_get_message":         ("/api/personal/gmail", "get"),
    "gmail_send_message":        ("/api/personal/gmail", "send"),
    "gmail_create_draft":        ("/api/personal/gmail", "draft"),
    "gmail_list_labels":         ("/api/personal/gmail", "labels_list"),
    "calendar_list_calendars":   ("/api/personal/google-calendar", "calendars_list"),
    "calendar_list_events":      ("/api/personal/google-calendar", "events_list"),
    "calendar_create_event":     ("/api/personal/google-calendar", "event_create"),
    "calendar_update_event":     ("/api/personal/google-calendar", "event_update"),
    "calendar_delete_event":     ("/api/personal/google-calendar", "event_delete"),
    "drive_list_files":          ("/api/personal/google-drive", "files_list"),
    "drive_get_file":            ("/api/personal/google-drive", "file_get"),
    "drive_download_file":       ("/api/personal/google-drive", "file_download"),
    "drive_create_file":         ("/api/personal/google-drive", "file_create"),
    "drive_create_folder":       ("/api/personal/google-drive", "folder_create"),
    "drive_share_file":          ("/api/personal/google-drive", "permission_create"),
    "docs_create_document":      ("/api/personal/google-docs", "create"),
    "docs_get_document":         ("/api/personal/google-docs", "get"),
    "docs_append_text":          ("/api/personal/google-docs", "text_append"),
    "sheets_read_values":        ("/api/personal/google-sheets", "values_get"),
    "sheets_append_values":      ("/api/personal/google-sheets", "values_append"),
    "sheets_update_values":      ("/api/personal/google-sheets", "values_update"),
    "sheets_create_spreadsheet": ("/api/personal/google-sheets", "spreadsheet_create"),
}

# YouTube reuses the SHARED Google connection (server_dispatch → /api/personal/youtube), NOT a
# separate OAuth — the one Google grant carries youtube.readonly/youtube/upload. Every youtube_*
# tool routes with op = the tool name (the route switches on it). Loop avoids 25 identical lines.
for _yt in (
    "youtube_upload_video", "youtube_update_video", "youtube_delete_video", "youtube_set_thumbnail",
    "youtube_list_my_videos", "youtube_get_video", "youtube_search", "youtube_get_my_channel",
    "youtube_get_channel_stats", "youtube_update_channel_branding", "youtube_list_playlists",
    "youtube_create_playlist", "youtube_add_playlist_item", "youtube_list_playlist_items",
    "youtube_list_comment_threads", "youtube_insert_comment_thread", "youtube_reply_to_comment",
    "youtube_set_comment_moderation", "youtube_list_captions", "youtube_insert_caption",
    "youtube_list_subscriptions", "youtube_subscribe_channel", "youtube_list_live_broadcasts",
    "youtube_create_live_broadcast", "youtube_analytics_query",
):
    _DISPATCH_TOOL_MAP[_yt] = ("/api/personal/youtube", _yt)


def _call_dispatch(slug, spec, args):
    """Google Workspace: runs via the Nexplora server dispatch. A wired tool POSTs to its deployed personal
    route (token lives server-side, BYOK OAuth); un-wired tools stay honest-pending. Never fakes."""
    name = spec.get("name", "") if isinstance(spec, dict) else ""
    # Individual catalog tools carry their route + the route's own op via _DISPATCH_TOOL_MAP; legacy
    # *_crud keys resolve straight to a route (op already in the args). Unmapped → honest-pending.
    _dispatch_op = None
    _tm = _DISPATCH_TOOL_MAP.get(name)
    if _tm:
        route, _dispatch_op = _tm
    else:
        route = _DISPATCH_ROUTES.get(name)
    if not route:
        return {"ok": False, "detail": "server_dispatch_pending",
                "hint": "%s runs via the Nexplora server dispatch; %s isn't wired to a deployed route yet" % (slug, name or "this tool")}
    import requests
    try:
        import nx_message
        base = nx_message._auth_base()
        cfg = nx_message._load_config() or {}
    except Exception:
        import os
        base = os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"
        cfg = {}
    token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
    if not token:
        return {"ok": False, "detail": "not_signed_in"}
    payload = {k: v for k, v in (args or {}).items() if k != "approval"}  # route mints the approval
    if _dispatch_op and "op" not in payload:
        payload["op"] = _dispatch_op  # the route's op vocabulary (body.op)
    try:
        r = requests.post(base.rstrip("/") + route, json=payload,
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=30)
        try:
            d = r.json() if r.content else {}
        except Exception:
            d = None
        if not isinstance(d, dict) or "ok" not in d:
            return {"ok": False, "detail": "dispatch_route_not_deployed",
                    "hint": "%s isn't returning the route JSON yet (deploy pending: nexplora-v2 PR #327)" % route}
        if d.get("ok"):
            return {"ok": True, "status": d.get("status", 200), "text": json.dumps(d.get("result") or d.get("data") or {})[:1200]}
        err = d.get("error") or "dispatch_failed"
        hint = "reconnect Google in NX so the token carries gmail.send" if err == "gmail_unauthorized" else None
        return {"ok": False, "detail": err, "hint": hint}
    except Exception as e:
        return {"ok": False, "detail": "request_failed:%s" % type(e).__name__}


def call(slug, tool, args=None):
    """Execute a catalog tool, routed by the app's substrate. HONEST — real HTTP result or a clear pending/failure;
    NEVER a fabricated success. Returns {ok, text|status}/{ok:False, detail, hint?, body?}."""
    args = args if isinstance(args, dict) else {}
    spec = find_tool(slug, tool)
    if not spec:
        return {"ok": False, "detail": "unknown_tool:%s.%s" % (_norm(slug), tool)}
    sub = (catalog_for(slug) or {}).get("substrate")
    if sub == "local_keychain_token":
        return _call_local(slug, spec, args)
    if sub == "shared_oauth_vault":
        return _call_shared_oauth(slug, spec, args)
    if sub == "bos_bridge":
        return _call_bos(slug, spec, args)
    if sub == "server_dispatch":
        return _call_dispatch(slug, spec, args)
    return {"ok": False, "detail": "no_substrate:%s" % sub}
