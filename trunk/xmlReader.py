"""
PLN Toolkit Project

Clasa XMLReader citeste un fisier de chat XML si retine replicile
intr-o lista de Utterance, care pot fi accesate usor

"""

from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation

class Utterance:
	def __init__(self):
		self.text = ""
		self.nick = ""
		self.id = ""
		self.refid = ""
		

class XMLReader:
	def __init__(self):
		self.doc = []
		self.xmldoc = 0

	def read(self,filename):
		self.doc = []		
		self.xmldoc = minidom.parse(filename)
		turns_node = self.xmldoc.getElementsByTagName('Turn')
		for turn_node in turns_node:
			ut = Utterance()
			ut.nick = turn_node.attributes['nickname'].value
			utterance_nodes = turn_node.getElementsByTagName('Utterance')
			ut.text = self.getText(utterance_nodes)
			ut.id = utterance_nodes[0].attributes['genid'].value
			ut.refid = utterance_nodes[0].attributes['ref'].value
			self.doc.append(ut)

	def readPOST(self,filename):
		self.doc = []		
		self.xmldoc = minidom.parse(filename)
		aux_node = self.xmldoc.getElementsByTagName('POST')
		turns_node = aux_node[0].getElementsByTagName('TagUt')
		for turn_node in turns_node:
			ut = Utterance()
			ut.id = turn_node.attributes['id'].value
			rc = ""
			if turn_node.hasChildNodes():
				if turn_node.firstChild.nodeType == turn_node.TEXT_NODE:
					rc = rc + turn_node.firstChild.data
			ut.text = rc
			self.doc.append(ut)
		

	def close(self):
		self.xmldoc.unlink()

	def getText(self,nodelist):
		rc = ""
		for node in nodelist:
			if node.hasChildNodes():
				if node.firstChild.nodeType == node.TEXT_NODE:
					rc = rc + node.firstChild.data
		return rc




