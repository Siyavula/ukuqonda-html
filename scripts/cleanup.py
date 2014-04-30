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


    if element.tag == 'span':
        if 'class' in element.attrib.keys():
            if 'Bodytext-Bold' in element.attrib['class']:
                element.tag = 'b'
                element.attrib['class'] = ''

            elif 'Bodytext-Italic' in element.attrib['class']:
                element.tag = 'i'
                element.attrib['class'] = ''


    # headers
    if (element.tag == 'p'):
        if element.attrib['class'] is not None:
            if "Head-A" in element.attrib['class']:
                element.tag = "h1"
                del element.attrib['class']

            elif "Head-B" in element.attrib['class']:
                element.tag = "h2"
                del element.attrib['class']

            elif "Head-investigation--after-b-head-" in element.attrib['class']:
                element.tag = 'h3'

def delete_empty_elements(element):

    elements_to_ignore = ['table', 'hr', 'td', 'col', 'img', 'figure', 'tbody', 'tr']

    if element.tag not in elements_to_ignore:
        text = "".join([t for t in element.itertext(with_tail=True)]).strip() 
        if element.tail is not None:
            text = text + element.tail.strip()
        if text == "":
            _elements_to_remove.append(element)

    





def string_replace(html_as_string):

    # multiplication
    html_as_string = html_as_string.replace("&#195;&#151;" ,"\\times")
    html_as_string = html_as_string.replace("&#226;&#128;&#156;" ,'"')
    html_as_string = html_as_string.replace("&#226;&#128;&#157;" ,'"')
    html_as_string = html_as_string.replace("&#239;&#131;&#149;" ,'\\rightarrow')
    html_as_string = html_as_string.replace(' xml:lang="en-US"' ,'')



    return html_as_string
   


if __name__ == "__main__":
    filename = sys.argv[1]

    html = etree.HTML(open(filename, 'r').read())

    for e in html.iter():
        replace_elements(e)
        delete_empty_elements(e)
    
    # remove the marked elements
    for element in _elements_to_remove:
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)

    html_as_string = etree.tostring(html)
    html_as_string = string_replace(html_as_string)

    print(html_as_string)
