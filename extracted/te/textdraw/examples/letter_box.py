from textdraw import BoundingBox, Box, Pixel, PixelGroup, Point, TextPath, duplicate_shifted, multipath, render


class LetterBox:
    def __init__(self, letter: str, x: int, y: int):
        self.box = Box(letter, (x, y), padding=(0, 1, 0, 1))
        self.c_right = self.box.bbox.center_right + Point(1, 0)
        self.c_left = self.box.bbox.center_left - Point(1, 0)
        self.c_top = self.box.bbox.top_center + Point(0, 1)
        self.c_bottom = self.box.bbox.bottom_center - Point(0, 1)
        barrier = Pixel('⎚', style='blinkfast red', weight=None)
        self.barriers = PixelGroup(
            [
                barrier.duplicate(self.c_left - Point(0, 1)),
                barrier.duplicate(self.c_left + Point(0, 1)),
                barrier.duplicate(self.c_right - Point(0, 1)),
                barrier.duplicate(self.c_right + Point(0, 1)),
                barrier.duplicate(self.c_bottom - Point(1, 0)),
                barrier.duplicate(self.c_bottom + Point(1, 0)),
                barrier.duplicate(self.c_top - Point(1, 0)),
                barrier.duplicate(self.c_top + Point(1, 0)),
            ]
        )


if __name__ == '__main__':
    a = LetterBox('a', 0, 0)
    b = LetterBox('b', 20, -8)
    c = LetterBox('c', 3, -10)
    bbox = BoundingBox.wrap([a.box, b.box, c.box])
    bbox.top += 7
    bbox.bottom -= 7
    bbox.left -= 7
    bbox.right += 7

    all_barriers = [a.barriers, b.barriers, c.barriers, a.box, b.box, c.box]
    paths = []
    paths.append(
        TextPath(
            a.c_right,
            b.c_top,
            style='dimmed',
            weight=20,
            bend_penalty=20,
            environment=paths,
            barriers=all_barriers,
            bbox=bbox,
        )
    )
    paths.append(
        TextPath(
            a.c_bottom,
            b.c_left,
            style='green',
            weight=20,
            bend_penalty=20,
            environment=paths,
            barriers=all_barriers,
            bbox=bbox,
        )
    )

    paths.append(
        TextPath(
            a.c_left,
            c.c_top,
            style='blue',
            weight=20,
            bend_penalty=20,
            environment=paths,
            barriers=all_barriers,
            bbox=bbox,
        )
    )

    paths.append(
        TextPath(
            b.c_bottom,
            c.c_left,
            style='red',
            line_style='double',
            weight=20,
            bend_penalty=20,
            environment=paths,
            barriers=all_barriers,
            bbox=bbox,
        )
    )
    shared_paths = multipath(
        [c.c_bottom, b.c_left, a.c_top],
        [a.c_right, c.c_right, b.c_right],
        style='yellow',
        line_style='heavy',
        bend_penalty=20,
        environment=paths,
        barriers=all_barriers,
        bbox=bbox,
        optimize=True,
    )
    objs = [a.box, b.box, c.box, *paths, *shared_paths]
    bbox = BoundingBox.wrap(objs)
    objs_shifted = duplicate_shifted(
        [*objs, a.barriers, b.barriers, c.barriers],
        Point(bbox.width + 3, 0),
    )
    print(render([*objs, *objs_shifted]))
