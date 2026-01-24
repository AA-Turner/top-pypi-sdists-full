from contentstack_utils.helper.metadata import Metadata


def _title_or_uid(_obj: dict) -> str:
    _title = ""
    if _obj is not None:
        if 'title' in _obj and len(_obj['title']) != 0:
            _title = _obj['title']
        elif 'uid' in _obj:
            _title = _obj['uid']
    return _title


def _asset_title_or_uid(_obj: dict) -> str:
    _title = ""
    if _obj is not None:
        if 'title' in _obj and len(_obj['title']) != 0:
            _title = _obj['title']
        elif 'filename' in _obj:
            _title = _obj['filename']
        elif 'uid' in _obj:
            _title = _obj['uid']
    return _title


class Options:

    @staticmethod
    def render_options(_obj: dict, metadata: Metadata):
        if metadata.style_type.value == 'block':
            _content_type_uid = ''
            if '_content_type_uid' in _obj:
                _content_type_uid = _obj['_content_type_uid']
            return '<div><p>' + _title_or_uid(_obj) \
                   + '</p><div><p>Content type: <span>' + _content_type_uid \
                   + '</span></p></div>'
        if metadata.style_type.value == 'inline':
            return '<span>' + _title_or_uid(_obj) + '</span>'
        if metadata.style_type.value == 'link':
            return '<a href=' + _obj['url'] + '>' + _title_or_uid(_obj) + '</a>'
        if metadata.style_type.value == 'display':
            return '<img src=' + _obj['url'] + ' alt=' \
                   + _asset_title_or_uid(_obj) + '/>'
        if metadata.style_type.value == 'download':
            return '<a href=' + _obj['url'] + '>' + _asset_title_or_uid(_obj) + '</a>'

    @staticmethod
    def render_mark(mark_type: str, render_text: str):
        if mark_type == 'superscript':
            return "<sup>" + render_text + "</sup>"
        if mark_type == 'subscript':
            return "<sub>" + render_text + "</sub>"
        if mark_type == 'inlineCode':
            return "<span>" + render_text + "</span>"
        if mark_type == 'strikethrough':
            return "<strike>" + render_text + "</strike>"
        if mark_type == 'underline':
            return "<u>" + render_text + "</u>"
        if mark_type == 'italic':
            return "<em>" + render_text + "</em>"
        if mark_type == 'bold':
            return "<strong>" + render_text + "</strong>"
        else:
            return render_text
        pass

    @staticmethod
    def render_node(node_type, node_obj: dict, callback):
        inner_html = callback(node_obj['children'])
        if node_type == 'p':
            return "<p>" + inner_html + "</p>"
        if node_type == 'a':
            return "<a href=\"{}\">{}</a>".format(node_obj["attrs"]["url"], inner_html)
        if node_type == 'img':
            return "<img src=\"{}\" />{}".format(node_obj["attrs"]["src"], inner_html)
        if node_type == 'embed':
            return "<iframe src={}>{}</iframe>".format(node_obj["attrs"]["src"], inner_html)
        if node_type == 'h1':
            return "<h1>" + inner_html + "</h1>"
        if node_type == 'h2':
            return "<h2>" + inner_html + "</h2>"
        if node_type == 'h3':
            return "<h3>" + inner_html + "</h3>"
        if node_type == 'h4':
            return "<h4>" + inner_html + "</h4>"
        if node_type == 'h5':
            return "<h5>" + inner_html + "</h5>"
        if node_type == 'h6':
            return "<h6>" + inner_html + "</h6>"
        if node_type == 'ol':
            return "<ol>" + inner_html + "</ol>"
        if node_type == 'ul':
            return "<ul>" + inner_html + "</ul>"
        if node_type == 'li':
            return "<li>" + inner_html + "</li>"
        if node_type == 'hr':
            return "<hr />"
        if node_type == 'table':
            return "<table>" + inner_html + "</table>"
        if node_type == 'thead':
            return "<thead>" + inner_html + "</thead>"
        if node_type == 'tbody':
            return "<tbody>" + inner_html + "</tbody>"
        if node_type == 'tfoot':
            return "<tfoot>" + inner_html + "</tfoot>"
        if node_type == 'tr':
            return "<tr>" + inner_html + "</tr>"
        if node_type == 'th':
            return "<th>" + inner_html + "</th>"
        if node_type == 'td':
            return "<td>" + inner_html + "</td>"
        if node_type == 'blockquote':
            return "<blockquote>" + inner_html + "</blockquote>"
        if node_type == 'code':
            return "<code>" + inner_html + "</code>"
        if node_type == 'fragment':
            return "<fragment>" + inner_html + "</fragment>"
        if node_type == 'reference':
            if node_obj['attrs']['type'] == 'asset':
                return "<img src=\"{}\" alt=\"{}\" class=\"{}\"  />{}".format(node_obj["attrs"]["asset-link"], node_obj["attrs"]["alt"], node_obj["attrs"]["class-name"], inner_html)
            else:
                return inner_html
        if node_type == 'doc':
            return inner_html
        else:
            return inner_html
