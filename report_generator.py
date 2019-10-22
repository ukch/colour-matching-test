"""\
Generates an HTML report showing the detected main colours of all images in the
input directory.
"""

import argparse
import pathlib
import sys
import tempfile

from PIL import Image

import colour_matcher


REPORT_HEADER = """\
<!DOCTYPE html>
<html>
    <head>
        <title>Image Colours</title>
    </head>
    <body>
        <h1>Image Colours for '{dir}' directory</h1>
        <ul>
"""

REPORT_TEMPLATE = """\
<li>
    <img style="max-height: 300px" src="{url}" alt="{filename}" />
    <div>Main colours: <span>{colour}</span></div>
</li>
"""

REPORT_FOOTER = """\
        </ul>
    </body>
</html>
"""


def report_for_image(image):
    """
    Use the colour_matcher library to generate a colour report for the image
    """
    colours = colour_matcher.get_main_colours_from_image(image)
    return REPORT_TEMPLATE.format(
        url=f"file://{image.filename}",
        filename=pathlib.Path(image.filename).name,
        colour=colours,
    ).encode("utf-8")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir", type=pathlib.Path,
                        help="Directory containing the image files to process")
    args = parser.parse_args(argv)
    if not args.dir.is_dir():
        parser.error(f"'{args.dir}' is not a valid directory")
    with tempfile.NamedTemporaryFile(
        prefix="cmt-report-",
        suffix=".html",
        delete=False,
    ) as fh:
        print(f"Creating report file '{fh.name}'...")
        fh.write(REPORT_HEADER.format(dir=args.dir).encode("utf-8"))
        for filename in args.dir.iterdir():
            # TODO filter out non-image-files here
            fh.write(report_for_image(Image.open(filename)))
        fh.write(REPORT_FOOTER.encode("utf-8"))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
