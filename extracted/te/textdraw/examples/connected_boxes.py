from textdraw import Box, Pixel, TextPath, render, Point

if __name__ == '__main__':
    a = Box('A', (-20, 10), border_style='green', padding=(0, 1, 0, 1))
    b = Box('B', (0, 0), border_style='red', padding=(0, 1, 0, 1))
    print(a.bbox)
    start_node = Pixel('', a.bbox.bottom_right + Point(1, 0), style='red')
    end_node = Pixel('◼', b.bbox.top_left - Point(1, 0), style='green')
    path = TextPath(
        a.bbox.bottom_right + Point(1, -1),
        b.bbox.top_left - Point(2, 0),
        style='dimmed',
        start_direction='up',
        end_direction='right',
        bend_penalty=20,
    )
    print(render([a, b, start_node, end_node, path]))
