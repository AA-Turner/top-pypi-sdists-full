# -*- coding: utf-8 -*-
"""simple csv reader and writer"""

import csv
import pyloco 

class CsvReadWrite(pyloco.Task):

    def __init__(self, parent):

        self.add_data_argument("data", help="input csv file")

        self.add_option_argument("-o", "--output",
                                 help="output csv file")
        self.add_option_argument("--in-delimiter", default=",",
                                 help="input csv delimiter")
        self.add_option_argument("--out-delimiter", default=",",
                                 help="output csv delimiter")

        self.register_forward("data", help="data to be forwarded to next task")

    def perform(self, targs):

        outdata = []

        with open(targs.data, "r", newline="") as csvin:
            reader = csv.reader(csvin, delimiter=targs.in_delimiter)

            if targs.output:
                with open(targs.output, "w", newline="") as csvout:
                    writer = csv.writer(csvout, delimiter=targs.out_delimiter)

                    for row in reader:
                        outdata.append(row)
                        writer.writerow(row)
            else:
                for row in reader:
                    outdata.append(row)
                    print(targs.out_delimiter.join(row))

        self.add_forward(data=outdata)
