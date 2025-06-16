import pydicom
from dicomweb_client.api import DICOMfileClient


client = DICOMfileClient("file:///tmp/dcmtest")


dcm = client.retrieve_study("1.3.46.670589.14.1000.210.4.199999.20110525182825.1.0")[0]

frames = client.retrieve_instance(
    study_instance_uid="1.3.46.670589.14.1000.210.4.199999.20110525182825.1.0",
    series_instance_uid=dcm.SeriesInstanceUID,
    sop_instance_uid=dcm.SOPInstanceUID,
    media_types=(('image/jp2', '1.2.840.10008.1.2.4.90', ), )
    # frame_numbers=[1],
)

breakpoint()
