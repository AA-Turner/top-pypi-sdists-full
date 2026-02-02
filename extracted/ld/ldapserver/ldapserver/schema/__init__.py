from .types import *
from .definitions import *
from . import syntaxes, matching_rules

RFC4512_ATTRIBUTE_TYPES = [
	"( 2.5.4.1 NAME 'aliasedObjectName' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 SINGLE-VALUE )",
	"( 2.5.4.0 NAME 'objectClass' EQUALITY objectIdentifierMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.38 )",
	"( 2.5.18.3 NAME 'creatorsName' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 SINGLE-VALUE NO-USER-MODIFICATION USAGE directoryOperation )",
	"( 2.5.18.1 NAME 'createTimestamp' EQUALITY generalizedTimeMatch ORDERING generalizedTimeOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 SINGLE-VALUE NO-USER-MODIFICATION USAGE directoryOperation )",
	"( 2.5.18.4 NAME 'modifiersName' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 SINGLE-VALUE NO-USER-MODIFICATION USAGE directoryOperation )",
	"( 2.5.18.2 NAME 'modifyTimestamp' EQUALITY generalizedTimeMatch ORDERING generalizedTimeOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.24 SINGLE-VALUE NO-USER-MODIFICATION USAGE directoryOperation )",
	"( 2.5.21.9 NAME 'structuralObjectClass' EQUALITY objectIdentifierMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.38 SINGLE-VALUE NO-USER-MODIFICATION USAGE directoryOperation ) ",
	"( 2.5.21.10 NAME 'governingStructureRule' EQUALITY integerMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE NO-USER-MODIFICATION USAGE directoryOperation )",
	"( 2.5.18.10 NAME 'subschemaSubentry' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 SINGLE-VALUE NO-USER-MODIFICATION USAGE directoryOperation )",
	"( 2.5.21.6 NAME 'objectClasses' EQUALITY objectIdentifierFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.37 USAGE directoryOperation )",
	"( 2.5.21.5 NAME 'attributeTypes' EQUALITY objectIdentifierFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.3 USAGE directoryOperation )",
	"( 2.5.21.4 NAME 'matchingRules' EQUALITY objectIdentifierFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.30 USAGE directoryOperation )",
	"( 2.5.21.8 NAME 'matchingRuleUse' EQUALITY objectIdentifierFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.31 USAGE directoryOperation )",
	"( 1.3.6.1.4.1.1466.101.120.16 NAME 'ldapSyntaxes' EQUALITY objectIdentifierFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.54 USAGE directoryOperation )",
	"( 2.5.21.2 NAME 'dITContentRules' EQUALITY objectIdentifierFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.16 USAGE directoryOperation )",
	"( 2.5.21.1 NAME 'dITStructureRules' EQUALITY integerFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.17 USAGE directoryOperation )",
	"( 2.5.21.7 NAME 'nameForms' EQUALITY objectIdentifierFirstComponentMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.35 USAGE directoryOperation )",
	"( 1.3.6.1.4.1.1466.101.120.6 NAME 'altServer' SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 USAGE dSAOperation )",
	"( 1.3.6.1.4.1.1466.101.120.5 NAME 'namingContexts' SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 USAGE dSAOperation )",
	"( 1.3.6.1.4.1.1466.101.120.13 NAME 'supportedControl' SYNTAX 1.3.6.1.4.1.1466.115.121.1.38 USAGE dSAOperation )",
	"( 1.3.6.1.4.1.1466.101.120.7 NAME 'supportedExtension' SYNTAX 1.3.6.1.4.1.1466.115.121.1.38 USAGE dSAOperation )",
	"( 1.3.6.1.4.1.4203.1.3.5 NAME 'supportedFeatures' EQUALITY objectIdentifierMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.38 USAGE dSAOperation )",
	"( 1.3.6.1.4.1.1466.101.120.15 NAME 'supportedLDAPVersion' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 USAGE dSAOperation )",
	"( 1.3.6.1.4.1.1466.101.120.14 NAME 'supportedSASLMechanisms' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 USAGE dSAOperation )",
]
RFC4512_OBJECT_CLASSES = [
	"( 2.5.6.0 NAME 'top' ABSTRACT MUST objectClass )",
	"( 2.5.6.1 NAME 'alias' SUP top STRUCTURAL MUST aliasedObjectName )",
	"( 1.3.6.1.4.1.1466.101.120.111 NAME 'extensibleObject' SUP top AUXILIARY )",
	"( 2.5.20.1 NAME 'subschema' AUXILIARY MAY ( dITStructureRules $ nameForms $ ditContentRules $ objectClasses $ attributeTypes $ matchingRules $ matchingRuleUse ) )",
]
#:
RFC4512_SCHEMA = Schema(syntax_definitions=syntaxes.ALL, matching_rule_definitions=matching_rules.ALL, attribute_type_definitions=RFC4512_ATTRIBUTE_TYPES, object_class_definitions=RFC4512_OBJECT_CLASSES)
#:
CORE_SCHEMA = RFC4512_SCHEMA

RFC4519_ATTRIBUTE_TYPES = [
	"( 2.5.4.15 NAME 'businessCategory' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.6 NAME ( 'c' 'countryName' ) SUP name SYNTAX 1.3.6.1.4.1.1466.115.121.1.11 SINGLE-VALUE )",
	"( 2.5.4.3 NAME ( 'cn' 'commonName' ) SUP name )",
	"( 0.9.2342.19200300.100.1.25 NAME ( 'dc' 'domainComponent' ) EQUALITY caseIgnoreIA5Match SUBSTR caseIgnoreIA5SubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )",
	"( 2.5.4.13 NAME 'description' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.27 NAME 'destinationIndicator' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.44 )",
	"( 2.5.4.49 NAME 'distinguishedName' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )",
	"( 2.5.4.46 NAME 'dnQualifier' EQUALITY caseIgnoreMatch ORDERING caseIgnoreOrderingMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.44 )",
	"( 2.5.4.47 NAME 'enhancedSearchGuide' SYNTAX 1.3.6.1.4.1.1466.115.121.1.21 )",
	"( 2.5.4.23 NAME 'facsimileTelephoneNumber' SYNTAX 1.3.6.1.4.1.1466.115.121.1.22 )",
	"( 2.5.4.44 NAME 'generationQualifier' SUP name )",
	"( 2.5.4.42 NAME ( 'givenName' 'gn' ) SUP name )",
	"( 2.5.4.51 NAME 'houseIdentifier' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.43 NAME 'initials' SUP name )",
	"( 2.5.4.25 NAME 'internationalISDNNumber' EQUALITY numericStringMatch SUBSTR numericStringSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.36 )",
	"( 2.5.4.7 NAME ( 'l' 'localityName' ) SUP name )",
	"( 2.5.4.31 NAME 'member' SUP distinguishedName )",
	"( 2.5.4.41 NAME 'name' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.10 NAME ( 'o' 'organizationName' ) SUP name )",
	"( 2.5.4.11 NAME ( 'ou' 'organizationalUnitName' ) SUP name )",
	"( 2.5.4.32 NAME 'owner' SUP distinguishedName )",
	"( 2.5.4.19 NAME 'physicalDeliveryOfficeName' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.16 NAME 'postalAddress' EQUALITY caseIgnoreListMatch SUBSTR caseIgnoreListSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.41 )",
	"( 2.5.4.17 NAME 'postalCode' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.18 NAME 'postOfficeBox' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.28 NAME 'preferredDeliveryMethod' SYNTAX 1.3.6.1.4.1.1466.115.121.1.14 SINGLE-VALUE )",
	"( 2.5.4.26 NAME 'registeredAddress' SUP postalAddress SYNTAX 1.3.6.1.4.1.1466.115.121.1.41 )",
	"( 2.5.4.33 NAME 'roleOccupant' SUP distinguishedName )",
	"( 2.5.4.14 NAME 'searchGuide' SYNTAX 1.3.6.1.4.1.1466.115.121.1.25 )",
	"( 2.5.4.34 NAME 'seeAlso' SUP distinguishedName )",
	"( 2.5.4.5 NAME 'serialNumber' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.44 )",
	"( 2.5.4.4 NAME ( 'sn' 'surname' ) SUP name )",
	"( 2.5.4.8 NAME 'st' SUP name )",
	"( 2.5.4.9 NAME 'street' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.20 NAME 'telephoneNumber' EQUALITY telephoneNumberMatch SUBSTR telephoneNumberSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.50 )",
	"( 2.5.4.22 NAME 'teletexTerminalIdentifier' SYNTAX 1.3.6.1.4.1.1466.115.121.1.51 )",
	"( 2.5.4.21 NAME 'telexNumber' SYNTAX 1.3.6.1.4.1.1466.115.121.1.52 )",
	"( 2.5.4.12 NAME 'title' SUP name )",
	"( 0.9.2342.19200300.100.1.1 NAME ( 'uid' 'userid' ) EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.5.4.50 NAME 'uniqueMember' EQUALITY uniqueMemberMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.34 )",
	"( 2.5.4.35 NAME 'userPassword' EQUALITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )",
	"( 2.5.4.24 NAME 'x121Address' EQUALITY numericStringMatch SUBSTR numericStringSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.36 )",
	"( 2.5.4.45 NAME 'x500UniqueIdentifier' EQUALITY bitStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.6 )",
]
RFC4519_OBJECT_CLASSES = [
	"( 2.5.6.11 NAME 'applicationProcess' SUP top STRUCTURAL MUST cn MAY ( seeAlso $ ou $ l $ description ) )",
	"( 2.5.6.2 NAME 'country' SUP top STRUCTURAL MUST c MAY ( searchGuide $ description ) )",
	"( 1.3.6.1.4.1.1466.344 NAME 'dcObject' SUP top AUXILIARY MUST dc )",
	"( 2.5.6.14 NAME 'device' SUP top STRUCTURAL MUST cn MAY ( serialNumber $ seeAlso $ owner $ ou $ o $ l $ description ) )",
	"( 2.5.6.9 NAME 'groupOfNames' SUP top STRUCTURAL MUST ( member $ cn ) MAY ( businessCategory $ seeAlso $ owner $ ou $ o $ description ) )",
	"( 2.5.6.17 NAME 'groupOfUniqueNames' SUP top STRUCTURAL MUST ( uniqueMember $ cn ) MAY ( businessCategory $ seeAlso $ owner $ ou $ o $ description ) )",
	"( 2.5.6.3 NAME 'locality' SUP top STRUCTURAL MAY ( street $ seeAlso $ searchGuide $ st $ l $ description ) )",
	"( 2.5.6.4 NAME 'organization' SUP top STRUCTURAL MUST o MAY ( userPassword $ searchGuide $ seeAlso $ businessCategory $ x121Address $ registeredAddress $ destinationIndicator $ preferredDeliveryMethod $ telexNumber $ teletexTerminalIdentifier $ telephoneNumber $ internationalISDNNumber $ facsimileTelephoneNumber $ street $ postOfficeBox $ postalCode $ postalAddress $ physicalDeliveryOfficeName $ st $ l $ description ) )",
	"( 2.5.6.7 NAME 'organizationalPerson' SUP person STRUCTURAL MAY ( title $ x121Address $ registeredAddress $ destinationIndicator $ preferredDeliveryMethod $ telexNumber $ teletexTerminalIdentifier $ telephoneNumber $ internationalISDNNumber $ facsimileTelephoneNumber $ street $ postOfficeBox $ postalCode $ postalAddress $ physicalDeliveryOfficeName $ ou $ st $ l ) )",
	"( 2.5.6.8 NAME 'organizationalRole' SUP top STRUCTURAL MUST cn MAY ( x121Address $ registeredAddress $ destinationIndicator $ preferredDeliveryMethod $ telexNumber $ teletexTerminalIdentifier $ telephoneNumber $ internationalISDNNumber $ facsimileTelephoneNumber $ seeAlso $ roleOccupant $ preferredDeliveryMethod $ street $ postOfficeBox $ postalCode $ postalAddress $ physicalDeliveryOfficeName $ ou $ st $ l $ description ) )",
	"( 2.5.6.5 NAME 'organizationalUnit' SUP top STRUCTURAL MUST ou MAY ( businessCategory $ description $ destinationIndicator $ facsimileTelephoneNumber $ internationalISDNNumber $ l $ physicalDeliveryOfficeName $ postalAddress $ postalCode $ postOfficeBox $ preferredDeliveryMethod $ registeredAddress $ searchGuide $ seeAlso $ st $ street $ telephoneNumber $ teletexTerminalIdentifier $ telexNumber $ userPassword $ x121Address ) )",
	"( 2.5.6.6 NAME 'person' SUP top STRUCTURAL MUST ( sn $ cn ) MAY ( userPassword $ telephoneNumber $ seeAlso $ description ) )",
	"( 2.5.6.10 NAME 'residentialPerson' SUP person STRUCTURAL MUST l MAY ( businessCategory $ x121Address $ registeredAddress $ destinationIndicator $ preferredDeliveryMethod $ telexNumber $ teletexTerminalIdentifier $ telephoneNumber $ internationalISDNNumber $ facsimileTelephoneNumber $ preferredDeliveryMethod $ street $ postOfficeBox $ postalCode $ postalAddress $ physicalDeliveryOfficeName $ st $ l ) )",
	"( 1.3.6.1.1.3.1 NAME 'uidObject' SUP top AUXILIARY MUST uid )",
]
#:
RFC4519_SCHEMA = CORE_SCHEMA.extend(attribute_type_definitions=RFC4519_ATTRIBUTE_TYPES, object_class_definitions=RFC4519_OBJECT_CLASSES)

RFC4523_ATTRIBUTE_TYPES = [
	"( 2.5.4.36 NAME 'userCertificate' DESC 'X.509 user certificate' EQUALITY certificateExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.8 )",
	"( 2.5.4.37 NAME 'cACertificate' DESC 'X.509 CA certificate' EQUALITY certificateExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.8 )",
	"( 2.5.4.40 NAME 'crossCertificatePair' DESC 'X.509 cross certificate pair' EQUALITY certificatePairExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.10 )",
	"( 2.5.4.39 NAME 'certificateRevocationList' DESC 'X.509 certificate revocation list' EQUALITY certificateListExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.9 )",
	"( 2.5.4.38 NAME 'authorityRevocationList' DESC 'X.509 authority revocation list' EQUALITY certificateListExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.9 )",
	"( 2.5.4.53 NAME 'deltaRevocationList' DESC 'X.509 delta revocation list' EQUALITY certificateListExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.9 )",
	"( 2.5.4.52 NAME 'supportedAlgorithms' DESC 'X.509 supported algorithms' EQUALITY algorithmIdentifierMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.49 )",
]
RFC4523_OBJECT_CLASSES = [
	"( 2.5.6.21 NAME 'pkiUser' DESC 'X.509 PKI User' SUP top AUXILIARY MAY userCertificate )",
	"( 2.5.6.22 NAME 'pkiCA' DESC 'X.509 PKI Certificate Authority' SUP top AUXILIARY MAY ( cACertificate $ certificateRevocationList $ authorityRevocationList $ crossCertificatePair ) )",
	"( 2.5.6.19 NAME 'cRLDistributionPoint' DESC 'X.509 CRL distribution point' SUP top STRUCTURAL MUST cn MAY ( certificateRevocationList $ authorityRevocationList $ deltaRevocationList ) )",
	"( 2.5.6.23 NAME 'deltaCRL' DESC 'X.509 delta CRL' SUP top AUXILIARY MAY deltaRevocationList )",
	"( 2.5.6.15 NAME 'strongAuthenticationUser' DESC 'X.521 strong authentication user' SUP top AUXILIARY MUST userCertificate )",
	"( 2.5.6.18 NAME 'userSecurityInformation' DESC 'X.521 user security information' SUP top AUXILIARY MAY ( supportedAlgorithms ) )",
	"( 2.5.6.16 NAME 'certificationAuthority' DESC 'X.509 certificate authority' SUP top AUXILIARY MUST ( authorityRevocationList $ certificateRevocationList $ cACertificate ) MAY crossCertificatePair )",
	"( 2.5.6.16.2 NAME 'certificationAuthority-V2' DESC 'X.509 certificate authority, version 2' SUP certificationAuthority AUXILIARY MAY deltaRevocationList )",
]
#:
RFC4523_SCHEMA = RFC4519_SCHEMA.extend(attribute_type_definitions=RFC4523_ATTRIBUTE_TYPES, object_class_definitions=RFC4523_OBJECT_CLASSES)

RFC4524_ATTRIBUTE_TYPES = [
	"( 0.9.2342.19200300.100.1.37 NAME 'associatedDomain' EQUALITY caseIgnoreIA5Match SUBSTR caseIgnoreIA5SubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )",
	"( 0.9.2342.19200300.100.1.38 NAME 'associatedName' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )",
	"( 0.9.2342.19200300.100.1.48 NAME 'buildingName' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.43 NAME 'co' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 0.9.2342.19200300.100.1.14 NAME 'documentAuthor' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )",
	"( 0.9.2342.19200300.100.1.11 NAME 'documentIdentifier' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.15 NAME 'documentLocation' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.56 NAME 'documentPublisher' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 0.9.2342.19200300.100.1.12 NAME 'documentTitle' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.13 NAME 'documentVersion' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.5 NAME 'drink' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.20 NAME 'homePhone' EQUALITY telephoneNumberMatch SUBSTR telephoneNumberSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.50 )",
	"( 0.9.2342.19200300.100.1.39 NAME 'homePostalAddress' EQUALITY caseIgnoreListMatch SUBSTR caseIgnoreListSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.41 )",
	"( 0.9.2342.19200300.100.1.9 NAME 'host' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.4 NAME 'info' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{2048} )",
	"( 0.9.2342.19200300.100.1.3 NAME 'mail' EQUALITY caseIgnoreIA5Match SUBSTR caseIgnoreIA5SubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.26{256} )",
	"( 0.9.2342.19200300.100.1.10 NAME 'manager' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )",
	"( 0.9.2342.19200300.100.1.41 NAME 'mobile' EQUALITY telephoneNumberMatch SUBSTR telephoneNumberSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.50 )",
	"( 0.9.2342.19200300.100.1.45 NAME 'organizationalStatus' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.42 NAME 'pager' EQUALITY telephoneNumberMatch SUBSTR telephoneNumberSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.50 )",
	"( 0.9.2342.19200300.100.1.40 NAME 'personalTitle' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.6 NAME 'roomNumber' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.21 NAME 'secretary' EQUALITY distinguishedNameMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 )",
	"( 0.9.2342.19200300.100.1.44 NAME 'uniqueIdentifier' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
	"( 0.9.2342.19200300.100.1.8 NAME 'userClass' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{256} )",
]
RFC4524_OBJECT_CLASSES = [
	"( 0.9.2342.19200300.100.4.5 NAME 'account' SUP top STRUCTURAL MUST uid MAY ( description $ seeAlso $ l $ o $ ou $ host ) )",
	"( 0.9.2342.19200300.100.4.6 NAME 'document' SUP top STRUCTURAL MUST documentIdentifier MAY ( cn $ description $ seeAlso $ l $ o $ ou $ documentTitle $ documentVersion $ documentAuthor $ documentLocation $ documentPublisher ) )",
	"( 0.9.2342.19200300.100.4.9 NAME 'documentSeries' SUP top STRUCTURAL MUST cn MAY ( description $ l $ o $ ou $ seeAlso $ telephonenumber ) )",
	"( 0.9.2342.19200300.100.4.13 NAME 'domain' SUP top STRUCTURAL MUST dc MAY ( userPassword $ searchGuide $ seeAlso $ businessCategory $ x121Address $ registeredAddress $ destinationIndicator $ preferredDeliveryMethod $ telexNumber $ teletexTerminalIdentifier $ telephoneNumber $ internationaliSDNNumber $ facsimileTelephoneNumber $ street $ postOfficeBox $ postalCode $ postalAddress $ physicalDeliveryOfficeName $ st $ l $ description $ o $ associatedName ) )",
	"( 0.9.2342.19200300.100.4.17 NAME 'domainRelatedObject' SUP top AUXILIARY MUST associatedDomain )",
	"( 0.9.2342.19200300.100.4.18 NAME 'friendlyCountry' SUP country STRUCTURAL MUST co )",
	"( 0.9.2342.19200300.100.4.14 NAME 'rFC822localPart' SUP domain STRUCTURAL MAY ( cn $ description $ destinationIndicator $ facsimileTelephoneNumber $ internationaliSDNNumber $ physicalDeliveryOfficeName $ postalAddress $ postalCode $ postOfficeBox $ preferredDeliveryMethod $ registeredAddress $ seeAlso $ sn $ street $ telephoneNumber $ teletexTerminalIdentifier $ telexNumber $ x121Address ) )",
	"( 0.9.2342.19200300.100.4.7 NAME 'room' SUP top STRUCTURAL MUST cn MAY ( roomNumber $ description $ seeAlso $ telephoneNumber ) )",
	"( 0.9.2342.19200300.100.4.19 NAME 'simpleSecurityObject' SUP top AUXILIARY MUST userPassword )",
]
#:
RFC4524_SCHEMA = RFC4519_SCHEMA.extend(attribute_type_definitions=RFC4524_ATTRIBUTE_TYPES, object_class_definitions=RFC4524_OBJECT_CLASSES)
#:
COSINE_SCHEMA = RFC4524_SCHEMA

RFC3112_ATTRIBUTE_TYPES = [
	"( 1.3.6.1.4.1.4203.1.3.3 NAME 'supportedAuthPasswordSchemes' DESC 'supported password storage schemes' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26{32} USAGE dSAOperation )",
	"( 1.3.6.1.4.1.4203.1.3.4 NAME 'authPassword' DESC 'password authentication information' EQUALITY 1.3.6.1.4.1.4203.1.2.2 SYNTAX 1.3.6.1.4.1.4203.1.1.2 )",
]
RFC3112_OBJECT_CLASSES = [
	"( 1.3.6.1.4.1.4203.1.4.7 NAME 'authPasswordObject' DESC 'authentication password mix in class' AUXILIARY MAY authPassword )",
]
#:
RFC3112_SCHEMA = CORE_SCHEMA.extend(attribute_type_definitions=RFC3112_ATTRIBUTE_TYPES, object_class_definitions=RFC3112_OBJECT_CLASSES)

RFC2079_ATTRIBUTE_TYPES = [
	"( 1.3.6.1.4.1.250.1.57 NAME 'labeledURI' DESC 'Uniform Resource Identifier with optional label' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
]
RFC2079_OBJECT_CLASSES = [
	"( 1.3.6.1.4.1.250.3.15 NAME 'labeledURIObject' DESC 'object that contains the URI attribute type' SUP top AUXILIARY MAY labeledURI )",
]
#: :any:`Schema` implementing the labeledURIObject object class and the
#: labeledURI attribute type.
RFC2079_SCHEMA = CORE_SCHEMA.extend(attribute_type_definitions=RFC2079_ATTRIBUTE_TYPES, object_class_definitions=RFC2079_OBJECT_CLASSES)

RFC2798_ATTRIBUTE_TYPES = [
	# Originally from RFC1274, but updated and used by RFC2798
	"( 0.9.2342.19200300.100.1.55 NAME 'audio' EQUALITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40{250000} )",
	# Also from RFC1274 and updated by RFC2798, but lacks SYNTAX, so "Fax" is added here
	"( 0.9.2342.19200300.100.1.7 NAME 'photo' SYNTAX 1.3.6.1.4.1.1466.115.121.1.23 )",

	"( 2.16.840.1.113730.3.1.1 NAME 'carLicense' DESC 'vehicle license or registration plate' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.16.840.1.113730.3.1.2 NAME 'departmentNumber' DESC 'identifies a department within an organization' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 2.16.840.1.113730.3.1.241 NAME 'displayName' DESC 'preferred name of a person to be used when displaying entries' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE )",
	"( 2.16.840.1.113730.3.1.3 NAME 'employeeNumber' DESC 'numerically identifies an employee within an organization' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE )",
	"( 2.16.840.1.113730.3.1.4 NAME 'employeeType' DESC 'type of employment for a person' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 0.9.2342.19200300.100.1.60 NAME 'jpegPhoto' DESC 'a JPEG image' SYNTAX 1.3.6.1.4.1.1466.115.121.1.28 )",
	"( 2.16.840.1.113730.3.1.39 NAME 'preferredLanguage' DESC 'preferred written or spoken language for a person' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE )",
	"( 2.16.840.1.113730.3.1.40 NAME 'userSMIMECertificate' DESC 'signed message used to support S/MIME' SYNTAX 1.3.6.1.4.1.1466.115.121.1.5 )",
	"( 2.16.840.1.113730.3.1.216 NAME 'userPKCS12' DESC 'PKCS #12 PFX PDU for exchange of personal identity information' SYNTAX 1.3.6.1.4.1.1466.115.121.1.5 )",
]
RFC2798_OBJECT_CLASSES = [
	"( 2.16.840.1.113730.3.2.2 NAME 'inetOrgPerson' SUP organizationalPerson STRUCTURAL MAY ( audio $ businessCategory $ carLicense $ departmentNumber $ displayName $ employeeNumber $ employeeType $ givenName $ homePhone $ homePostalAddress $ initials $ jpegPhoto $ labeledURI $ mail $ manager $ mobile $ o $ pager $ photo $ roomNumber $ secretary $ uid $ userCertificate $ x500uniqueIdentifier $ preferredLanguage $ userSMIMECertificate $ userPKCS12 ) )",
]
#: :any:`Schema` implementing the inetOrgPerson object class and its
#: attribute types.
RFC2798_SCHEMA = (RFC4524_SCHEMA|RFC2079_SCHEMA|RFC4523_SCHEMA).extend(attribute_type_definitions=RFC2798_ATTRIBUTE_TYPES, object_class_definitions=RFC2798_OBJECT_CLASSES)
#:
INETORG_SCHMEA = RFC2798_SCHEMA

RFC2307BIS_ATTRIBUTE_TYPES = [
	"( 1.3.6.1.1.1.1.0 NAME 'uidNumber' DESC 'An integer uniquely identifying a user in an administrative domain' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.1 NAME 'gidNumber' DESC 'An integer uniquely identifying a group in an administrative domain' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.2 NAME 'gecos' DESC 'The GECOS field; the common name' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.3 NAME 'homeDirectory' DESC 'The absolute path to the home directory' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.4 NAME 'loginShell' DESC 'The path to the login shell' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.5 NAME 'shadowLastChange' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.6 NAME 'shadowMin' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.7 NAME 'shadowMax' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.8 NAME 'shadowWarning' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.9 NAME 'shadowInactive' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.10 NAME 'shadowExpire' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.11 NAME 'shadowFlag' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.12 NAME 'memberUid' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 1.3.6.1.1.1.1.13 NAME 'memberNisNetgroup' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 1.3.6.1.1.1.1.14 NAME 'nisNetgroupTriple' DESC 'Netgroup triple' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 1.3.6.1.1.1.1.15 NAME 'ipServicePort' DESC 'Service port number' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.16 NAME 'ipServiceProtocol' DESC 'Service protocol name' EQUALITY caseIgnoreMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )",
	"( 1.3.6.1.1.1.1.17 NAME 'ipProtocolNumber' DESC 'IP protocol number' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.18 NAME 'oncRpcNumber' DESC 'ONC RPC number' EQUALITY integerMatch ORDERING integerOrderingMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.27 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.19 NAME 'ipHostNumber' DESC 'IPv4 addresses as a dotted decimal omitting leading zeros or IPv6 addresses as defined in RFC2373' EQUALITY caseIgnoreIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )",
	"( 1.3.6.1.1.1.1.20 NAME 'ipNetworkNumber' DESC 'IP network omitting leading zeros, eg. 192.168' EQUALITY caseIgnoreIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.21 NAME 'ipNetmaskNumber' DESC 'IP netmask omitting leading zeros, eg. 255.255.255.0' EQUALITY caseIgnoreIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.22 NAME 'macAddress' DESC 'MAC address in maximal, colon separated hex notation, eg. 00:00:92:90:ee:e2' EQUALITY caseIgnoreIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )",
	"( 1.3.6.1.1.1.1.23 NAME 'bootParameter' DESC 'rpc.bootparamd parameter' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )",
	"( 1.3.6.1.1.1.1.24 NAME 'bootFile' DESC 'Boot image name' EQUALITY caseExactIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 )",
	"( 1.3.6.1.1.1.1.26 NAME 'nisMapName' DESC 'Name of a generic NIS map' EQUALITY caseIgnoreMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{64} )",
	"( 1.3.6.1.1.1.1.27 NAME 'nisMapEntry' DESC 'A generic NIS entry' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{1024} SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.28 NAME 'nisPublicKey' DESC 'NIS public key' EQUALITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.29 NAME 'nisSecretKey' DESC 'NIS secret key' EQUALITY octetStringMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.30 NAME 'nisDomain' DESC 'NIS domain' EQUALITY caseIgnoreIA5Match SYNTAX 1.3.6.1.4.1.1466.115.121.1.26{256} )",
	"( 1.3.6.1.1.1.1.31 NAME 'automountMapName' DESC 'automount Map Name' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.32 NAME 'automountKey' DESC 'Automount Key value' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE )",
	"( 1.3.6.1.1.1.1.33 NAME 'automountInformation' DESC 'Automount information' EQUALITY caseExactMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE )",
]
RFC2307BIS_OBJECT_CLASSES = [
	"( 1.3.6.1.1.1.2.0 NAME 'posixAccount' DESC 'Abstraction of an account with POSIX attributes' SUP top AUXILIARY MUST ( cn $ uid $ uidNumber $ gidNumber $ homeDirectory ) MAY ( authPassword $ userPassword $ loginShell $ gecos $ description ) )",
	"( 1.3.6.1.1.1.2.1 NAME 'shadowAccount' DESC 'Additional attributes for shadow passwords' SUP top AUXILIARY MUST uid MAY ( authPassword $ userPassword $ description $ shadowLastChange $ shadowMin $ shadowMax $ shadowWarning $ shadowInactive $ shadowExpire $ shadowFlag ) )",
	"( 1.3.6.1.1.1.2.2 NAME 'posixGroup' DESC 'Abstraction of a group of accounts' SUP top AUXILIARY MUST gidNumber MAY ( authPassword $ userPassword $ memberUid $ description ) )",
	"( 1.3.6.1.1.1.2.3 NAME 'ipService' DESC 'Abstraction an Internet Protocol service.  Maps an IP port and protocol (such as tcp or udp) to one or more names; the distinguished value of the cn attribute denotes the service\\27s canonical name' SUP top STRUCTURAL MUST ( cn $ ipServicePort $ ipServiceProtocol ) MAY description )",
	"( 1.3.6.1.1.1.2.4 NAME 'ipProtocol' DESC 'Abstraction of an IP protocol. Maps a protocol number to one or more names. The distinguished value of the cn attribute denotes the protocol canonical name' SUP top STRUCTURAL MUST ( cn $ ipProtocolNumber ) MAY description )",
	"( 1.3.6.1.1.1.2.5 NAME 'oncRpc' DESC 'Abstraction of an Open Network Computing (ONC) [RFC1057] Remote Procedure Call (RPC) binding.  This class maps an ONC RPC number to a name.  The distinguished value of the cn attribute denotes the RPC service canonical name' SUP top STRUCTURAL MUST ( cn $ oncRpcNumber ) MAY description )",
	"( 1.3.6.1.1.1.2.6 NAME 'ipHost' DESC 'Abstraction of a host, an IP device. The distinguished value of the cn attribute denotes the host\\27s canonical name. Device SHOULD be used as a structural class' SUP top AUXILIARY MUST ( cn $ ipHostNumber ) MAY ( authPassword $ userPassword $ l $ description $ manager ) )",
	"( 1.3.6.1.1.1.2.7 NAME 'ipNetwork' DESC 'Abstraction of a network. The distinguished value of the cn attribute denotes the network canonical name' SUP top STRUCTURAL MUST ipNetworkNumber MAY ( cn $ ipNetmaskNumber $ l $ description $ manager ) )",
	"( 1.3.6.1.1.1.2.8 NAME 'nisNetgroup' DESC 'Abstraction of a netgroup. May refer to other netgroups' SUP top STRUCTURAL MUST cn MAY ( nisNetgroupTriple $ memberNisNetgroup $ description ) )",
	"( 1.3.6.1.1.1.2.9 NAME 'nisMap' DESC 'A generic abstraction of a NIS map' SUP top STRUCTURAL MUST nisMapName MAY description )",
	"( 1.3.6.1.1.1.2.10 NAME 'nisObject' DESC 'An entry in a NIS map' SUP top STRUCTURAL MUST ( cn $ nisMapEntry $ nisMapName ) )",
	"( 1.3.6.1.1.1.2.11 NAME 'ieee802Device' DESC 'A device with a MAC address; device SHOULD be used as a structural class' SUP top AUXILIARY MAY macAddress )",
	"( 1.3.6.1.1.1.2.12 NAME 'bootableDevice' DESC 'A device with boot parameters; device SHOULD be used as a structural class' SUP top AUXILIARY MAY ( bootFile $ bootParameter ) )",
	"( 1.3.6.1.1.1.2.14 NAME 'nisKeyObject' DESC 'An object with a public and secret key' SUP top AUXILIARY MUST ( cn $ nisPublicKey $ nisSecretKey ) MAY ( uidNumber $ description ) )",
	"( 1.3.6.1.1.1.2.15 NAME 'nisDomainObject' DESC 'Associates a NIS domain with a naming context' SUP top AUXILIARY MUST nisDomain )",
	"( 1.3.6.1.1.1.2.16 NAME 'automountMap' SUP top STRUCTURAL MUST ( automountMapName ) MAY description )",
	"( 1.3.6.1.1.1.2.17 NAME 'automount' DESC 'Automount information' SUP top STRUCTURAL MUST ( automountKey $ automountInformation ) MAY description )",
	"( 1.3.6.1.1.1.2.18 NAME 'groupOfMembers' DESC 'A group with members (DNs)' SUP top STRUCTURAL MUST cn MAY ( businessCategory $ seeAlso $ owner $ ou $ o $ description $ member ) )",
]
#: :any:`Schema` implementing draft-howard-rfc2307bis-02 (updated/extended NIS schema)
RFC2307BIS_SCHEMA = (RFC4524_SCHEMA|RFC3112_SCHEMA).extend(attribute_type_definitions=RFC2307BIS_ATTRIBUTE_TYPES, object_class_definitions=RFC2307BIS_OBJECT_CLASSES)
