"""The HTTP endpoint"""

# TODO hook this endpoint up to an HTTP server (ie. Django)
# TODO do not allow unauthorized requests to be made

from io import BytesIO

from PIL import Image
import requests

import colour_matcher


def _basic_check(response):
    if not response.ok:
        raise requests.exceptions.HTTPError(response.status_code)
    return response


def get(url):
    # Basic type checking
    try:
        head = _basic_check(requests.head(url))
    except requests.RequestException:
        return 400, "HTTP request failed"
    content_type = head.headers.get("Content-Type", "").split(";")[0]
    if not content_type.startswith("image/"):
        return 400, f"URL has bad content type: '{content_type}'"

    # Get the body
    try:
        response = _basic_check(requests.get(url))
    except requests.RequestException:
        return 400, "HTTP request failed"
    image = Image.open(BytesIO(response.content))
    colours_full = colour_matcher.get_main_colours_from_image(image)
    colours, distances = zip(*colours_full)
    return 200, {
        "colours": list(colours),
        "distances": list(distances),
    }
