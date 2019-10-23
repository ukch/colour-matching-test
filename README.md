Colour Matching Test
--------------------

*By Joel Cross*

## Installation

1. Clone this repository
2. Get yourself a copy of Python 3.7, and [Pipenv](/pypa/pipenv)
3. Do `pipenv install --dev`


## Usage
There are two separate tests included with this project: the first will take
a set of images in a directory, and will generate an HTML report of the primary
colours detected in all the files in that directory. To run the report on the
sample files:

    `$ python report_generator.py photosets/example`

The second test is the unit tests of the endpoint itself. You can test these
by running `pytest` (make sure your python is able to make HTTP calls, or the
tests will fail)


## Assumptions

I have made a number of assumptions on this project, which I have attempted to
document below:

* This project is for the purpose of analysing images with one main colour
tone. Feeding in an image with a large number of shades (e.g. a photo) will
return unexpected results.
* Predefined colour references will be provided at a later date. I have used
the 16 base colours from the HTML 4.01 specification, which unfortunately do
not provide an accurate colour match for all of the example inputs (for
example, the 'grey' image is actually slightly blue in tone, and therefore
the algorithm considers it a half-way match between navy and teal, rather than
a grey). I do not consider this a bug, as a more expansive list of colours will
provide a more accurate result.


## Further potential enhancements

Aside from the obvious (connecting the endpoint to an actual web server), I
have identified a number of potential enhancements for this code:

* More error handling (e.g. what happens if the file is not a valid image file?)
* An improvement could be made so that the number of colours in the file is
reduced before analysis, if it is too large. This would have the benefit of
clustering similar colours together, thereby potentially resolving the problem
in my first assumption (see the previous section).


## Other considerations

**Scale**: If we were to take advantage of the asynchronous programming
capabilities of Python 3.7, we would be able to handle multiple requests at the
same time. We could make our HTTP requests using the
[AIOHTTP](https://aiohttp.readthedocs.io/en/stable/) library instead of
**requests**, but unfortunately the image-processing tasks must still be run in
a synchronous manner, due to the nature of the PIL library. Alternatively
(or additionally) we could use the endpoint to simply add a task to a queue,
which is then executed as and when the processor time is available. Finally,
from a devops point of view, we could add as many servers as we need to be able
to process the load.

**Efficiency**: I identified a potential effeciency improvement in the previous
section, which works by reducing the number of colours in the image to aid the
algorithm in determining which colour is in the majority (for example, an image
with multiple shades of the same colour would currently recognise the multiple
shades as different colours and not rank them as highly as, for example, the
background colour). Another potential effeciency improvement would be to use an
API that already exists elsewhere, for example the one at
[apicloud.me](http://apicloud.me/). In that case we would have less control over
the categorisation, but would not have to maintain the engine in-house.

**Resilience**: I have made no assumptions about how the endpoint could be
hosted. It is currently in a form where it would easily integrate into a Flask
or Django application, but it is equally suited to any other Python-based server
framework. I have written a basic testsuite that tests inputs, outputs and simple
error conditions, however the testsuite currently makes real HTTP calls, which
ideally should not happen (these should be mocked instead).


**Alerting/Monitoring**: At present, the application provides no logging output,
although that is easily remedied. An error-monitoring service such as Sentry
could be applied so that any errors in the endpoint will be picked up on.
Finally, an 'uptime checker' such as Pingdom could be configured to regularly
check on the server to ensure it is online and responding to requests.
