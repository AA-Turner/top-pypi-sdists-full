from textdraw import Box, render

if __name__ == '__main__':
    box = Box('Hello, world', style='italic', border_style='bold blue', line_style='double', padding=(1, 2, 1, 2))
    print(render([box]))
