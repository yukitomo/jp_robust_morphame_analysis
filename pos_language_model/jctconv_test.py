#!/usr/bin/python
#-*-coding:utf-8-*-
#2014-12-27 Yuki Tomo

import jctconv

k = "ご飯"
sent = unicode(k.strip(),"utf-8")
print type(sent)
print jctconv.jctconv.hira2kata(sent)