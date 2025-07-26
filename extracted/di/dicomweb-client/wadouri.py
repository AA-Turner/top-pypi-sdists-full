from dicomweb_client.uri import URI, ProtocolDialect


uri = URI(base_url='http://localhost', study_instance_uid='1.2.3', series_instance_uid='4.5.6', dialect=ProtocolDialect.URI)

print(uri)
