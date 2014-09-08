''' Let's fix the fucking html again
'''


from lxml import etree

import docopt

USAGE = '''Usage: fix_epub_xhtml_again.py <htmlfiles>...'''


def fix_bad_figures(html):

    htmltree = etree.HTML(html)

    for figure in htmltree.findall('.//figure'):
        figure = etree.strip_tags(figure, 'div', 'p', 'span')


    for figure in htmltree.findall('.//figure'):
        parent_tag = figure.getparent().tag

        # places they can not be in
        if parent_tag not in ['figure', 'ol', 'ul', 'span']:
            continue

        # if they're in a bad place, do something

        # in a list, add to previous li
        if parent_tag in ['ol', 'ul']:
            prev = figure.getprevious()
            if prev is None:
                continue

            if prev.tag == 'li':
                prev.append(figure)

    for figcaption in htmltree.findall('.//figcaption'):
        if figcaption.getparent().tag != 'figure':
            print('    ficaption not in figure, line :' + str(figcaption.sourceline))

    html = etree.tostring(htmltree, pretty_print=True)

    return html


if __name__ == "__main__":

    arguments = docopt.docopt(USAGE)

    for html_file in arguments['<htmlfiles>']:
        print(html_file)
        print("    Reading")
        with open(html_file) as hfile:
            html = hfile.read()
            print("    Fixing")
            html = fix_bad_figures(html)

        print("    Saving")
        with open(html_file, 'w') as hfile:
            hfile.write(html)
