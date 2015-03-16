# XML in Python #

There are a few tutorials over here: http://diveintopython.org/xml_processing/

Looks simple enough:

```
from xml.dom import minidom
doc = minidom.parse('1.xml')
```

And a few methods to help with parsing:

  * .toxml()  - gets string representation
  * .firstChild
  * .childNodes[i](i.md)

And the rest can be found in the DOM documentation on http://www.w3schools.com/