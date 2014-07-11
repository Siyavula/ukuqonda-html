import sys
import os

from lxml import etree


def HTML2XML(content):

    xhtml = etree.tostring(content, method='xml')

    return xhtml


def strip_elements(content):
    print("stripping tags: "), 
    tags_to_strip = ['colgroup',]

    for tag in tags_to_strip:
        print(tag), 
        etree.strip_elements(content, tag, with_tail=False)

    print('')

    return content



def add_alt(content):

    for img in content.findall('.//img'):
        if 'alt' not in img.attrib.keys():
            img.attrib['alt'] = img.attrib['src']

    return content



def cleanup_lists(content):

    removethese = []

    # lists
    for lists in ['ol', 'ul']:
        for thislist in content.findall('.//ol'):
            for i, child in enumerate(thislist):
                # move hr to previous li in this ol
                if child.tag == 'hr':
                    if i > 0:
                        if thislist[i-1].tag == 'li':
                            thislist[i-1].append(etree.Element('hr'))
                            removethese.append(child)
                        elif thislist[i-1].tag == 'hr':
                            removethese.append(child)


    for r in removethese:
        if r.tail is not None:
            if r.tail.strip() == '':
                r.getparent().remove(r)


    

    return content


if __name__ == "__main__":

    htmlfiles = [f for f in os.listdir(os.curdir) if f.strip().endswith('.html') and 'cleaned' in f]
    htmlfiles.sort()

    for hf in htmlfiles:
        print hf
        content = etree.HTML(open(hf, 'r').read())
        content = strip_elements(content)
        content = add_alt(content)
        content = cleanup_lists(content)


        xhtml = HTML2XML(content)
        xhtmloutput = hf.replace('.html', '.xhtml')

        with open(xhtmloutput, 'w') as output:
            output.write(xhtml)






    

