#coding:utf-8
import xlrd
import sys
import numpy
import os.path

#输出整个Excel文件的内容
def print_workbook(wb):
  for s in wb.sheets():
    print("Sheet:"+ s.name)
    for r in range(s.nrows):
      strRow = ""
      for c in s.row(r):
        strRow += ("\t" + c.value)
      print("ROW[" + str(r) + "]:"+strRow)

#把一行转化为一个字符串
def row_to_str(row):
  strRow = ""
  for c in row:
        if isinstance(c, str):
              strRow += ("\t" + c)
        else:
              strRow += ("\t" + str(c.value))
  return strRow;

#打印diff结果报表
def print_report(result_file,file_name,column_name,report):
      file = open(result_file,'a')
      file.write("\n\n-----------------------------------------------------------------\n")
      modified_row = sum(map(lambda x : 'm' in x , report))
      add_row = sum(map(lambda x : '+' in x , report))
      delete_row = sum(map(lambda x : '-' in x , report))
      file.write("表名："+file_name+"， 修改 "+str(int(modified_row/2))+"行,  添加 "+str(add_row)+"行,  删除 "+str(delete_row)+"行  （包括错位的行）\n\n")
      file.write(column_name+"\n")

      for o in report:
            if isinstance(o, list):
                  for i in o:
                        file.write("\t" + i + "\n")
            else:
              file.write(o + "\n")

#diff两个Sheet
def diff_sheet(sheet1, sheet2):
  nr1 = sheet1.nrows # 总行数
  nr2 = sheet2.nrows
  nr = max(nr1, nr2)
  report = []
  for r in range(nr):
    row1 = None;
    row2 = None;
    if r<nr1:
      row1 = sheet1.row(r) # 获取单元格值类型和内容
    if r<nr2:
      row2 = sheet2.row(r) # 获取单元格值类型和内容

    diff = 0; # 0:equal, 1: not equal, 2: row2 is more, 3: row2 is less
    if row1==None and row2!=None:
      diff = 2
      report.append("+ Row 修改后[第" + str(r+1) + "行]: " + row_to_str(row2))
    if row1==None and row2==None:
      diff = 0
    if row1!=None and row2==None:
      diff = 3
      report.append("- Row 修改前[第" + str(r+1) + "行]: " + row_to_str(row1))
    if row1!=None and row2!=None:
      # diff the two rows
      reportRow = diff_row(row1, row2)
      if len(reportRow)>0:
        report.append("m Row 修改前[第" + str(r+1) + "行]: " + row_to_str(row1))
        report.append("m Row 修改后[第" + str(r+1) + "行]: " + row_to_str(row2))
        # report.append(reportRow)

  return report;

#diff两行
def diff_row(row1, row2):
  nc1 = len(row1)
  nc2 = len(row2)
  nc = max(nc1, nc2)
  report = []
  for c in range(nc):
    ce1 = None;
    ce2 = None;
    if c<nc1:
      ce1 = row1[c]
    if c<nc2:
      ce2 = row2[c]
    
    diff = 0; # 0:equal, 1: not equal, 2: row2 is more, 3: row2 is less
    if ce1==None and ce2!=None:
      diff = 2
      report.append("+ Column 修改后[第" + str(c+1) + "列]: " + str(ce2.value))
    if ce1==None and ce2==None:
      diff = 0
    if ce1!=None and ce2==None:
      diff = 3
      report.append("- Column 修改前[第" + str(c+1) + "列]: " + str(ce1.value))
    if ce1!=None and ce2!=None:
      if ce1.value == ce2.value:
        diff = 0
      else:
        diff = 1
        report.append("m Column 修改前[第" + str(c+1) + "列]: " + str(ce1.value))
        report.append("m Column 修改后[第" + str(c+1) + "列]: " + str(ce2.value))

  return report

if __name__=='__main__':
  file1 = sys.argv[1]
  file2 = sys.argv[2]
  result_file = sys.argv[3]

  wb1 = xlrd.open_workbook(file1)
  wb2 = xlrd.open_workbook(file2)
  file_name = os.path.basename(file1)
  column_name = "列名：                        " + row_to_str(wb1.sheet_by_index(0).row_values(2))
  #diff两个文件的第一个sheet
  report = diff_sheet(wb1.sheet_by_index(0), wb2.sheet_by_index(0))
  #打印diff结果
  print_report(result_file,file_name,column_name,report)