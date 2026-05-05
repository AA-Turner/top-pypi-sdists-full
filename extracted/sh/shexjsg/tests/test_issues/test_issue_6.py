from pyjsg.jsglib.loader import loads as jsg_loads

from ShExJSG import ShExJ


shex = """{
  "@context": [
      "http://www.w3.org/ns/shex.jsonld",
      {
         "@base": "http://bioentity.io/vocab/"
      }
   ],
  "type": "Schema",
  "shapes": [
    {
      "id": "http://a.example/S1",
      "type": "Shape"
    }
  ]
}"""


def test_context():
    jsg_loads(shex, ShExJ)