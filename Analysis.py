import matplotlib.pyplot as plt
import os
import re

dirctory = 'data1'
files = os.listdir(dirctory)

files = [i for i in files if re.match('performance_', i)]
