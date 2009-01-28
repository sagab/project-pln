# just a simple parser thingie to show off how to
# access XML data by using DOM. There is also a SAX
# version but DOM is simpler, in my opinion.

from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation

doc1 = minidom.parse('xml/1.xml')
people = doc1.getElementsByTagName('Person')

# creating an XML
imp = getDOMImplementation()
doc2 = imp.createDocument(None, 'names', None)
top = doc2.documentElement

for a in people:
	v = a.attributes['nickname'].value
	
	print v
	
	# really need to create document structure Element, Node, Attribute, etc.
	nod = doc2.createElement('name')
	top.appendChild(nod)
	tn = doc2.createTextNode(v)
	nod.appendChild(tn);

# writes content of doc2 DOM from memory to a file
file = open('xml/names.xml','w')
doc2.writexml(file,'  ','  ','\n')
file.close()

#clean up mem
doc1.unlink()
doc2.unlink()
