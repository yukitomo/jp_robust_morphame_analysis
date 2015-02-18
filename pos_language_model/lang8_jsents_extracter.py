#!/usr/bin/python
#-*-coding:utf-8-*-
#2015-02-16 Yuki Tomo

import json
import re

lang8_file = open('/Users/yukitomo/Research/jp_robust_morphame_analysis/data/lang-8-20111007-2.0/lang-8-20111007-L1-v2.dat', 'r')

hira = re.compile(ur"[あ-ん]")

for line in lang8_file:
	#print line
	try:
		load_obj = json.loads(line)

		if load_obj[2] == "Japanese":
			for string in load_obj[4]:
				#print string.encode('utf-8')
				if hira.search(string):
					print string.encode('utf-8')
					#print " "
	except:
		pass

lang8_file.close()

"""
>>> import json
>>> json.load(open('/Users/yukitomo/Research/jp_robust_morphame_analysis/data/lang-8-20111007-2.0/lang-8-20111007-L1-v2-Japanese.dat', 'r'))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/__init__.py", line 290, in load
    **kw)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/__init__.py", line 338, in loads
    return _default_decoder.decode(s)
  File "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 369, in decode
    raise ValueError(errmsg("Extra data", s, end, len(s)))
ValueError: Extra data: line 2 column 1 - line 7835 column 936 (char 4325 - 16129410)
>>> 



"""