from dicomweb_client.api import DICOMwebClient


client = DICOMwebClient("http://172.27.190.125/ea/MGH_VNA_NDHM")

dcm = client.retrieve_instance(
    study_instance_uid="1.2.840.114350.2.362.2.798268.2.824235692.1",
    series_instance_uid="1.2.840.113619.2.452.3.279717852.329.1619778479.438",
    sop_instance_uid="1.2.840.113619.2.452.3.279717852.329.1619778479.440.1",
    media_types=["application/dicom"]
)

print(dcm.SeriesDescription)

client = DICOMwebClient("http://172.27.190.125/ea/MGH_VNA_NDHM", wado_url_prefix='wado')

dcm = client.retrieve_instance_legacy(
    study_instance_uid="1.2.840.114350.2.362.2.798268.2.824235692.1",
    series_instance_uid="1.2.840.113619.2.452.3.279717852.329.1619778479.438",
    sop_instance_uid="1.2.840.113619.2.452.3.279717852.329.1619778479.440.1",
)

print(dcm.SeriesDescription)
# http://172.27.190.125/ea/MGH_VNA_NDHM/studies/1.2.840.114350.2.362.2.798268.2.824235692.1/series/1.2.840.113619.2.452.3.279717852.329.1619778479.438/instances/1.2.840.113619.2.452.3.279717852.329.1619778479.440.1/rendered

im = client.retrieve_instance_rendered_legacy(
    study_instance_uid="1.2.840.114350.2.362.2.798268.2.824235692.1",
    series_instance_uid="1.2.840.113619.2.452.3.279717852.329.1619778479.438",
    sop_instance_uid="1.2.840.113619.2.452.3.279717852.329.1619778479.440.1",
    params={"rows": 90, "columns": 90}
)

open("test.jpg", "wb").write(im)

print(len(im))
