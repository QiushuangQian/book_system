import re

temp = re.findall(r'-?\d+\.?\d*e?-?\d*?', '160.5 TWD')
print(temp)