import xmlReader

r = xmlReader.XMLReader()
r.read('xml/4.xml')

for msg in r.doc:
	print msg.id,":",msg.refid,":",msg.nick," : ",msg.text
