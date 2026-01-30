from ansitable import ANSITable, Column, Cell

table = ANSITable("col1", "column 2 has a big header", "column 3")
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", Cell(-5.5, bgcolor="blue"), 6, bgcolor="yellow")
table.row("ccccccc", 8.8, 9)
table.print()
