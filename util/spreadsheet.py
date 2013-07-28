#!/usr/bin/env python

import xlwt


def write_spreadsheet(data, sheet_name, out_file):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(sheet_name)

    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])

    workbook.save(out_file)
