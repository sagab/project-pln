# just a simple parser thingie to show off how to
# access XML data by using DOM. There is also a SAX
# version but DOM is simpler, in my opinion.

from xml.dom import minidom
doc = minidom.parse('xml/1.xml')
people = doc.getElementsByTagName('Person')

for a in people:
	print a.attributes['nickname'].value