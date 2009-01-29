# just a simple parser thingie to show off how to
# access XML data by using DOM. There is also a SAX
# version but DOM is simpler, in my opinion.

from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation

def getText(nodelist):
    rc = ""
    for node in nodelist:
       if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

doc1 = minidom.parse('xml/4.xml')
turns_node = doc1.getElementsByTagName('Turn')

# creating an XML
imp = getDOMImplementation()
doc2 = imp.createDocument(None, 'names', None)
top = doc2.documentElement

for turn_node in turns_node:
	nick = turn_node.attributes['nickname'].value
	
	utterance_node = turn_node.getElementsByTagName('Utterance')

	utterance = getText(utterance_node)
	
	# de ce nu merge asta de mai jos? nu ca ar merge functia de mai sus oricum :)
	#utterance =  turn_node.getElementsByTagName('Utterance')[0].data
	print nick,":",utterance,"!"



	# really need to create document structure Element, Node, Attribute, etc.
#	nod = doc2.createElement('name')
#	top.appendChild(nod)
#	tn = doc2.createTextNode(v)
#	nod.appendChild(tn);

# writes content of doc2 DOM from memory to a file
#file = open('xml/names.xml','w')
#doc2.writexml(file,'  ','  ','\n')
#file.close()

#clean up mem
#doc1.unlink()
#doc2.unlink()
