import sys
import os

from lxml import etree
import copy


_elements_to_remove = []

def replace_elements(element):
    # replace some elements with <hr/> only.
    hr = etree.Element('hr')
    hr.tail = '\n'
    if 'class' in element.attrib.keys():
        if (element.tag == "div") and ("Basic-Text-Frame" in element.attrib['class']):
            if (element[0].tag == 'p'):
                if element[0].attrib['class'] == "x-Answer-text-dotted-last-line--COPY-LINE-":
                    element.addprevious(copy.deepcopy(hr))
                    _elements_to_remove.append(element)

        for c in ["x--Answer-text-dotted-last-line para-style-override-", "x--Answer-text-dotted-last-line", "x--Answer-text-dotted-line-below"]:
            if (element.tag == "p") and (c in element.attrib['class']):
                if element.text is not None:
                    #if element.text.strip() in [".", ""]:
                    element.addprevious(copy.deepcopy(hr))
                    _elements_to_remove.append(element)

                else:
                    if len(element) == 1:
                        if element[0].tag == 'span':
                            element.addprevious(copy.deepcopy(hr))
                            _elements_to_remove.append(element)



    
   


if __name__ == "__main__":
    filename = sys.argv[1]

    html = etree.HTML(open(filename, 'r').read())

    for e in html.iter():
        replace_elements(e)

    # remove the marked elements
    for element in _elements_to_remove:
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)

    print(etree.tostring(html))
