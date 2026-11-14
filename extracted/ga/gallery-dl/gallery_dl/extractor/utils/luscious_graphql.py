# -*- coding: utf-8 -*-

# Copyright 2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

AlbumGet = """
query AlbumGet($id: ID!) {
  album {
    get(id: $id) {
      ... on Album {
        ...AlbumStandard
        cover_variants {
          width
          height
          size
          url
          target_width
        }
      }
      ... on MutationError {
        errors {
          code
          message
          name
        }
      }
    }
  }
}

fragment AlbumStandard on Album {
  __typename
  id
  title
  labels
  description
  created
  modified
  like_status
  number_of_favorites
  number_of_dislikes
  moderation_status
  marked_for_deletion
  marked_for_processing
  number_of_pictures
  number_of_animated_pictures
  number_of_duplicates
  slug
  is_manga
  is_protected
  url
  download_url
  permissions
  cover {
    width
    height
    size
    url
  }
  created_by {
    id
    url
    name
    display_name
    user_title
    avatar_url
  }
  content {
    id
    title
    url
  }
  language {
    id
    title
    url
  }
  tags {
    category
    text
    url
    count
  }
  genres {
    id
    title
    url
    acts_as_warning
  }
  audiences {
    id
    title
    url
  }
  is_featured
  featured_date
  featured_by {
    id
    url
    name
    display_name
    user_title
    avatar_url
  }
  original_owner {
    id
    url
    name
    display_name
    user_title
    avatar_url
  }
}
"""

PictureListInsideAlbum = """
query PictureListInsideAlbum($input: PictureInAlbumListInput!) {
  picture {
    list_in_album(input: $input) {
      info {
        ...FacetCollectionInfo
      }
      items {
        __typename
        id
        title
        description
        created
        like_status
        number_of_comments
        number_of_favorites
        moderation_status
        width
        height
        resolution
        aspect_ratio
        url_to_original
        url_to_video
        is_animated
        position
        permissions
        url
        tags {
          category
          text
          url
        }
        thumbnails {
          width
          height
          size
          url
          target_width
        }
      }
    }
  }
}

fragment FacetCollectionInfo on FacetCollectionInfo {
  page
  has_next_page
  has_previous_page
  total_items
  total_pages
  items_per_page
  url_complete
}
"""

AlbumList = """
query AlbumList($input: AlbumListInput!) {
  album {
    list(input: $input) {
      info {
        ...FacetCollectionInfo
      }
      items {
        ...AlbumInSearchList
      }
    }
  }
}

fragment FacetCollectionInfo on FacetCollectionInfo {
  page
  has_next_page
  has_previous_page
  total_items
  total_pages
  items_per_page
  url_complete
}

fragment AlbumInSearchList on Album {
  __typename
  id
  title
  description
  created
  modified
  like_status
  moderation_status
  number_of_favorites
  number_of_dislikes
  number_of_pictures
  number_of_animated_pictures
  number_of_duplicates
  slug
  is_manga
  url
  download_url
  labels
  permissions
  cover {
    width
    height
    size
    url
  }
  created_by {
    id
    url
    name
    display_name
    user_title
    avatar_url
  }
  language {
    id
    title
    url
  }
  tags {
    category
    text
    url
    count
  }
  genres {
    id
    title
    url
    acts_as_warning
  }
}
"""
