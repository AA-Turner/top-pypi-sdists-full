from pydantic import BaseModel

class NetworkTraffic(BaseModel):
    """
    The Network Traffic object describes characteristics of network traffic. Network
    traffic refers to data moving across a network at a given point of time. Defined
    by D3FEND <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Net
    workTraffic/'>d3f:NetworkTraffic</a>.
    """

    # Recommended:
    bytes: int | None = None
    packets: int | None = None

    # Optional:
    bytes_in: int | None = None
    bytes_out: int | None = None
    packets_in: int | None = None
    packets_out: int | None = None
    chunks: int | None = None # The total number of chunks (in and out).
    chunks_in: int | None = None # The number of chunks sent from the destination to the source.
    chunks_out: int | None = None # The number of chunks sent from the source to the destination.
