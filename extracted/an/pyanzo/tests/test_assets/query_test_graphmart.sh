DATASET="http://cambridgesemantics.com/Graphmart/9da211618a15476daa10cead2292d8e7"
DATASOURCE="http://cambridgesemantics.com/GqeDatasource/guid_3af6a337ad444400a1f01dbe2e16b82b"
QUERY="select * where { ?s ?p ?o } limit 2"

anzo query -dataset ${DATASET} -ds ${DATASOURCE} "${QUERY}" -o json

