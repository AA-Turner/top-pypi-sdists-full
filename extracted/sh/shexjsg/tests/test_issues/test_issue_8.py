from pyjsg.jsglib import loads as jsg_loads

from ShExJSG import ShExC, ShExJ

shexj = """{
   "type": "Schema",
   "@context": [
      "http://www.w3.org/ns/shex.jsonld",
      {
         "@base": "http://bioentity.io/vocab/"
      }
   ],
   "shapes": [
       {
         "type": "ShapeAnd",
         "id": "http://bioentity.io/vocab/BiologicalEntity",
         "shapeExprs": [
            "http://bioentity.io/vocab/NamedThing",
            {
               "type": "Shape",
               "expression": {
                  "type": "TripleConstraint",
                  "predicate": "http://purl.obolibrary.org/obo/RO_0002200",
                  "valueExpr": {
                     "type": "NodeConstraint"
                  },
                  "min": 0,
                  "max": 1
               }
            }
         ]
       }
    ]
}
"""


def test_empty_node_constraint():
    # Note: This test may no longer be valid, as we had invoked the ShExC compiler below to re-load the
    # resulting string.  For dependency reasons, we do not want to have ShExJSG dependent on the ShExC compiler so
    # we've shortened this test. FWIW, it passed before we did
    # shexc_str = str(ShExC(shex_json))
    # shex_c = ShExC(shexc_str)
    shex_json: ShExJ.Schema = jsg_loads(shexj, ShExJ)
    shex_c = ShExC(shex_json)
    assert shex_c.schema is not None