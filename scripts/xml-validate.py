import sys
import os

from lxml import etree


def is_valid_XML(content):
    try:
        xml = etree.XML(content)
        return True
    except:
        return False


def is_valid_HTML(content):
    try:
        html = etree.HTML(content)
        return True
    except:
        return False


def HTML2XML(content):

    html = etree.HTML(content)

    xhtml = etree.tostring(html, method='xml')

    return xhtml


if __name__ == "__main__":

    htmlfiles = [f for f in os.listdir(os.curdir) if f.strip().endswith('html')]
    htmlfiles.sort()

    for hf in htmlfiles:
        content = open(hf, 'r').read()
        print hf
        print "  XML:  ", is_valid_XML(content)
        print " HTML:  ",  is_valid_HTML(content)




    

