import sys
import os

from lxml import etree



html_template = r'''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{title}</title>
  <link href="basicstyles.css" rel="stylesheet" type="text/css" />
  <!--<script type="text/javascript" src=
  "mathjax/MathJax.js?config=TeX-AMS-MML_HTMLorMML">-->
</script>
</head>

<body>
    {content}
</body>
</html>
'''

def strip_whitespace_from_title(title):
    ''' Strip multiple whitespaces from a string'''

    stripped = " ".join(title.split())

    return stripped


if __name__ == "__main__":

    xhtml_source = open(sys.argv[1], 'r').read()
    xhtml = etree.HTML(xhtml_source)
    
    for h1 in xhtml.findall('.//h1'):
        title = strip_whitespace_from_title(" ".join([t.strip() for t in h1.itertext()]))
        filename = title.replace(' ', '-') + '.html'
        content = []
        parent = h1.getparent()
        for child in parent:
            content.append(etree.tostring(child))
            
        htmlcontents = html_template.format(content="".join(content), title=title)

        with open('temp-{filename}'.format(filename=filename), 'w') as f:
            f.write(htmlcontents)



