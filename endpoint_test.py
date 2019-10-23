"""
Test module for the endpoint

WARNING: This makes real HTTP requests, so results may vary
"""


import pytest

import endpoint


def test_bad_urls():
    # Test 1: 404
    url1 = "http://www.example.com/404"
    assert endpoint.get(url1) == (400, "HTTP request failed")

    # Test 2: Wrong content type
    url2 = "http://www.example.com/"
    assert endpoint.get(url2) == (400, "URL has bad content type: 'text/html'")


def test_sample_images():
    # It looks as if the grey and teal images are being classified incorrectly,
    # however the problem is actually that the 16 named colours are not close
    # to the main colour of either of these images. This problem can be solved
    # by adding extra named colours.
    url_tmpl = (
        "https://pwintyimages.blob.core.windows.net/samples/stars/"
        "test-sample-{}.png"
    )

    code, data = endpoint.get(url_tmpl.format("black"))
    assert code == 200
    assert data["colours"] == ["black"]

    code, data = endpoint.get(url_tmpl.format("grey"))
    assert code == 200
    assert data["colours"] == ["navy", "teal"]

    code, data = endpoint.get(url_tmpl.format("teal"))
    assert code == 200
    assert data["colours"] == ["navy", "purple", "teal"]

    code, data = endpoint.get(url_tmpl.format("navy"))
    assert code == 200
    assert data["colours"] == ["navy"]


if __name__ == "__main__":
    pytest.main()
