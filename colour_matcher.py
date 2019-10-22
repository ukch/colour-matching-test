"""The main colour matching module"""

import colorsys
from operator import itemgetter

import numpy as np


class Colour:
    def __init__(self, name=None):
        self.name = name
        self._rgb = None
        self._hsv = None

    @classmethod
    def from_rgb(cls, rgb, **kwargs):
        self = cls(**kwargs)
        self._rgb = np.array(rgb)
        return self

    @property
    def rgb(self):
        if self._rgb is None:
            return ValueError("No RGB value")
        return self._rgb

    @property
    def hsv(self):
        if self._hsv is None:
            self._hsv = np.array(colorsys.rgb_to_hsv(*self.rgb))
        return self._hsv

    def distance_from(self, other):
        return np.linalg.norm(self.hsv - other.hsv)


# TODO add the 16 named colours from the HTML 4.01 specification
NAMED_COLOURS = frozenset([
    Colour.from_rgb([000, 000, 000], name="black"),
    Colour.from_rgb([128, 128, 128], name="grey"),
    Colour.from_rgb([000, 000, 128], name="navy"),
    Colour.from_rgb([000, 128, 128], name="teal"),
])


def get_main_colour_from_image(image):
    pixel_count = np.product(image.size)
    colour_list = sorted(image.getcolors(pixel_count),
                         key=itemgetter(0), reverse=True)
    main_colour = Colour.from_rgb(colour_list[0][1])
    distances = {}
    for colour in NAMED_COLOURS:
        distance = main_colour.distance_from(colour)
        if distance == 0:
            # Colour is exact so no need to keep looking
            return colour.name
        else:
            distances[colour.name] = distance
    return min(distances.items(), key=itemgetter(1))[0]
