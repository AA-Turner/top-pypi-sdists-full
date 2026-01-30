from ansitable import ANSITable, Column, Cell

table = ANSITable(
    Column("col1", headalign="<", headstyle="underlined"),  # CHANGE
    Column("column 2 has a big header", colalign="^", colstyle="bold"),  # CHANGE
    Column("column 3", colalign="<", colbgcolor="green"),  # CHANGE
    border="thick",
    bordercolor="blue",  # CHANGE
)

table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", Cell(-5.5, bgcolor="blue"), 6, bgcolor="yellow")  # CHANGE
table.row("ccccccc", 8.8, -9)
table.row("dddd", 8.8, -9)
table.print()
print(repr(table))
