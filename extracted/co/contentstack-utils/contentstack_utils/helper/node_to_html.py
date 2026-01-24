from contentstack_utils.render.options import Options


class NodeToHtml:

    @staticmethod
    def text_node_to_html(node, option: Options):
        """
        accepts node type,
        on the basis of the node type, generates string
        :rtype: str
        """
        node_text = node['text']
        if 'superscript' in node:
            node_text = option.render_mark('superscript', node_text)
        if 'subscript' in node:
            node_text = option.render_mark('subscript', node_text)
        if 'inlineCode' in node:
            node_text = option.render_mark('inlineCode', node_text)
        if 'strikethrough' in node:
            node_text = option.render_mark('strikethrough', node_text)
        if 'underline' in node:
            node_text = option.render_mark('underline', node_text)
        if 'italic' in node:
            node_text = option.render_mark('italic', node_text)
        if 'bold' in node:
            node_text = option.render_mark('bold', node_text)
        return node_text
