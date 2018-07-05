
# coding: utf-8

# In[42]:

#from xml.etree.ElementTree import parse

#tree = parse("kowiki-20180401-pages-articles-multistream.xml")
#note = tree.getroot()

import xml.parsers.expat

#parser = xml.parsers.expat.ParserCreate()
#parser.ParseFile(open("kowiki-20180401-pages-articles-multistream.xml", "r", encoding="UTF8").read())

parser = xml.parsers.expat.ParserCreate()
with open("kowiki-20180401-pages-articles-multistream.xml", "r").read() as fh:
    for line in fh:
        if line.find("<<축구 선수 정보") !=  -1 : 
            print(line)
            break
        


# In[ ]:



