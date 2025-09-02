import markdown
import codecs


def md_to_html(md_filename):
    html_filename = u"{fn}.html".format(fn=u'.'.join(md_filename.split(u'.')[:-1]))

    with codecs.open(html_filename, mode='w') as html_file:

        html_file.write("""<!DOCTYPE html>
<html>
	<meta charset="UTF-8" />
	<link rel="stylesheet" type="text/css" href="style.css" />
</head>

<body>
""")
        markdown.markdownFromFile(input=md_filename)
        markdown.markdownFromFile(input=md_filename,
                                  output=html_file,
                                  encoding=u'utf-8')

        html_file.write(u'</body>'
                        u'</html>'
                        )

md_to_html(u'tutorial.md')