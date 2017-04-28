#!/usr/bin/env python
import re
import sys
prevLine = -1
code_arr = []
formatted = False

def add(line):
  # remove odd number white space in head of line
  m = re.search('^([ ]+)(.*)$', line)
  if m != None:
    space = m.group(1)
    if len(space)%2 == 1:
      space = space[1:]
      code = m.group(2)
      line = space + code
  # change "xx ,yy" to "xx, yy"
  line = re.sub(r'(.) ,', r'\1, ', line)
  code_arr.append(line)

filename = sys.argv[1]
with open(filename, "r+") as f:
  for line in f:
    line = line.replace("\r","").replace("\n",""  )
    # if line starts with long white spaces and a comma
    # remove the comma and put into the end of prev line
    m = re.search('^([ ]+),(.*)$', line)
    if m != None:
      space = m.group(1)
      code = m.group(2)
      if prevLine != -1:
        prevLine = prevLine + ","
        add(prevLine)
      formatted = True
      prevLine = space + code
    else:
      if prevLine != -1:
        add(prevLine)
      formatted = False
      prevLine = line

  # after loop ends add last line in buffer
  if prevLine != -1:
    add(prevLine)
  new_code = "\n".join(code_arr)+"\n" # add ending new line
  f.seek(0)
  f.write(new_code)
  f.truncate()