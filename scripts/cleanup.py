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
        
        # Notes
        if (element.tag == 'div') and (element.attrib['class'].startswith('frame-')):
            if (element[0].tag == 'p') and (element[0].attrib['class'].startswith('Body-box-no-indent')):
                element.attrib['class'] = 'aside'

        # find these tables that contains bullets
        if (element.tag == 'table') and (element.attrib['class'] == 'Basic-Table'):
            bulletitems = []
            for li in element.iter('li'):
                if li.attrib['class'] == 'Body-bullet':
                    if (li[0].tag == 'span'):
                        bulletitems.append(li)

            if len(bulletitems) > 0:
                contents = [p for p in element.iter('p') if p.attrib['class'] == "Body-content-no-indent"]
                if len(contents) > 0:
                    note = etree.Element('div')
                    note.attrib['class'] = 'note'
                    for p in contents:
                        note.append(copy.deepcopy(p))
                    element.addprevious(note)
                    _elements_to_remove.append(element)

                else:
                    contents = [ul for ul in element.iter('ul')]
                    if len(contents) > 0:
                        note = etree.Element('div')
                        note.attrib['class'] = 'note'
                        for p in contents:
                            note.append(copy.deepcopy(p))
                        element.addprevious(note)
                        _elements_to_remove.append(element)


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

            elif element.attrib['class'] == 'Head-investigation':
                element.tag = 'h3'

def delete_empty_elements(element):

    elements_to_ignore = ['table', 'hr', 'td', 'col', 'img', 'figure', 'tbody', 'tr', 'head', 'link', 'meta', 'script']

    children = [c.tag not in elements_to_ignore for c in element.iter()]

    if all(children):
        if element.tag not in elements_to_ignore:
            text = "".join([t for t in element.itertext(with_tail=True)]).strip() 
            if element.tail is not None:
                text = text + element.tail.strip()
            if text == "":
                _elements_to_remove.append(element)

    


def delete_en_masse(html):
    ''' html as full etree element'''


    # strip <br/>
    etree.strip_tags(html, 'br')


    return html


def string_replace(html_as_string):

    # multiplication
    html_as_string = html_as_string.replace("&#195;&#151;" ,"\\times")
    html_as_string = html_as_string.replace("&#195;&#183;" ,"\\div")
    html_as_string = html_as_string.replace("<hr>" ,"<hr/>")
    html_as_string = html_as_string.replace("&#226;&#128;&#156;" ,'"')
    html_as_string = html_as_string.replace("&#226;&#128;&#157;" ,'"')
    html_as_string = html_as_string.replace("&#239;&#131;&#149;" ,'\\rightarrow')
    html_as_string = html_as_string.replace("&#226;&#136;&#146;" ,'-')
    html_as_string = html_as_string.replace("&#226;&#128;&#153;" ,"'")
    html_as_string = html_as_string.replace("&#226;&#128;&#153;" ,"'")
    html_as_string = html_as_string.replace("&#226;&#136;&#134;" ,"\\triangle}")
    html_as_string = html_as_string.replace(' xml:lang="en-US"' ,'')
    html_as_string = html_as_string.replace('<b/>' ,'')
    html_as_string = html_as_string.replace('<td class="cell-style-override-2">' ,'<td class="red">')
    html_as_string = html_as_string.replace('<td class="cell-style-override-3">' ,'<td class="blue">')
    html_as_string = html_as_string.replace('<td class="cell-style-override-4">' ,'<td class="yellow">')
    html_as_string = html_as_string.replace('<span class="char-style-override-3">&#226;&#128;&#162;	</span>' ,'')
    html_as_string = html_as_string.replace('<span class="char-style-override-29">&#226;&#128;&#162;	</span>' ,'')
    html_as_string = html_as_string.replace('<span class="char-style-override-37">&#226;&#128;&#162;	</span>' ,'')



    return html_as_string
   


def fix_bold_italics(element):
    #  fix bold / italics
    if element.tag == 'span':
        if 'class' in element.attrib.keys():
            if 'Bodytext-Bold' in element.attrib['class']:
                element.tag = 'b'
                etree.strip_attributes(element, 'class')
            
            elif 'Body-box-bold' in element.attrib['class']:
                element.tag = 'b'
                etree.strip_attributes(element, 'class')

            elif 'Bodytext-Italic' in element.attrib['class']:
                element.tag = 'i'
                etree.strip_attributes(element, 'class')

    if element.tag == 'p':
        if 'class' in element.attrib.keys():
            if 'Body-text-bold-head' in element.attrib['class']:
                element.tag = 'b'

def addStuff(html):
    head = html.find('.//head')
    css = etree.fromstring('<link href="basicstyles.css" rel="stylesheet" type="text/css"></link>')
    mathjax = etree.fromstring('<script type="text/javascript" src="mathjax/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>')
    head.append(css)
    head.append(mathjax)

    return html

if __name__ == "__main__":
    filename = sys.argv[1]

    html = etree.HTML(open(filename, 'r').read())

    for e in html.iter():
        replace_elements(e)
        delete_empty_elements(e)

    for e in html.iter():
        fix_bold_italics(e)
    
    # remove the marked elements
    for element in _elements_to_remove:
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)

    html = delete_en_masse(html)

    html = addStuff(html)

    html_as_string = etree.tostring(html, method='html')
    html_as_string = string_replace(html_as_string)

    print(html_as_string.encode('utf-8'))
