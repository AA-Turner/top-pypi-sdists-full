import logging
from PIL import Image
import io
import requests

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Assuming getRequest is defined in globalImports, import it explicitly

def fetch_image(uri, max_size=(200, 200)):
    """
    Fetches an image from the given URI, verifies its integrity,
    resizes it, and returns the processed image data as bytes.
    """
    logging.info(f"Fetching image from URI: {uri}")
    try:
        # Extract the image URL from the URI
        image_url = get_img_url(uri)
        if not image_url:
            logging.error("Image URL could not be retrieved.")
            return None

        # Fetch the image content
        content = get_image_content(image_url)
        if not content:
            logging.error("Image content could not be retrieved.")
            return None

        # Open and verify the image
        image_data = io.BytesIO(content)
        img = Image.open(image_data)
        img.verify()  # Verify image integrity

        # Re-open the image for processing after verification
        image_data.seek(0)
        img = Image.open(image_data)
        img.thumbnail(max_size)  # Resize image

        # Save the processed image to a bytes buffer
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        return bio.getvalue()

    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.RequestException as req_err:
        logging.error(f"Request exception: {req_err}")
    except Image.UnidentifiedImageError:
        logging.error("Failed to identify the image file.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return None  # Return None if any exception occurs

def get_image_content(image_url):
    """
    Fetches the content from the image URL and ensures it's an image.
    Returns the content bytes if valid, else raises an error.
    """
    try:
        response = requests.get(url=image_url, data={}, result='content')
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            logging.error(f"URI does not point to an image. Content-Type: {content_type}")
            raise ValueError("Non-image content")

        return response.content

    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching image content: {http_err}")
        raise
    except requests.RequestException as req_err:
        logging.error(f"Request exception while fetching image content: {req_err}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in get_image_content: {e}")
        raise

def get_img_url(uri):
    """
    Extracts the image URL from the given URI by retrieving image variables.
    """
    try:
        uri_vars = get_image_vars(uri)
        # Assuming uri_vars is a dictionary after parsing JSON
        return uri_vars.get('image')
    except Exception as e:
        logging.error(f"Error extracting image URL from URI vars: {e}")
        return None

def get_image_vars(uri):
    """
    Fetches and parses the image variables from the given URI.
    Assumes the response is in JSON format.
    """
    try:
        response = requests.get(url=uri, data={})
        response.raise_for_status()
        return response.json()  # Parse response as JSON
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching image vars: {http_err}")
        raise
    except requests.RequestException as req_err:
        logging.error(f"Request exception while fetching image vars: {req_err}")
        raise
    except ValueError as ve:
        logging.error(f"JSON decoding failed: {ve}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in get_image_vars: {e}")
        raise

# Removed get_image_data as it is redundant with fetch_image
