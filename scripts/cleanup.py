import sys
import os

from lxml import etree



if __name__ == "__main__":
    filename = sys.argv[1]

    html = etree.HTML(open(filename, 'r').read())

    print html
