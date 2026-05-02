"""
Summary.

    EC2 SpotPrice Lib, GPL v3 License

    Copyright (c) 2018-2020 Blake Huber

    Python 3 Class.  Datatime object conversion --> utc formatted
    string when when embedded in a dictionary returned by Amazon
    Web Services' EC2 Spot Price

    Python 3 Module Function.  Datatime object conversion --> utc
    formatted string

"""

import datetime


def utc_conversion(data):
    """
        Converts datetime object embedded in a dictionary schema
        to utc datetime string format

    Args:
        :data (list | dict):  list of spot price data.  Alternatively,
            can be same list wrapped in dictionary (below)

    .. code: json

        {
            'AvailabilityZone': 'eu-west-1a',
            'InstanceType': 'm5d.4xlarge',
            'ProductDescription': 'Red Hat Enterprise Linux',
            'SpotPrice': '0.420000',
            'Timestamp': datetime.datetime(2019, 8, 11, 23, 56, 50, tzinfo=tzutc())
        }

    Returns:
        datetime, TYPE: str

    .. code: json

        {
            'AvailabilityZone': 'eu-west-1a',
            'InstanceType': 'm5d.4xlarge',
            'ProductDescription': 'Red Hat Enterprise Linux',
            'SpotPrice': '0.420000',
            'Timestamp': '2019-08-11T23:56:50Z'
        }

    """
    dt = data['Timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')
    data['Timestamp'] = dt
    return data


class UtcConversion():
    """
    Class that converts datetime object embedded in a
    dictionary schema to utc datetime string format
    """
    def __init__(self, data):
        """
        Args:
            :data (list | dict):  list of spot price data.  Alternatively,
                can be same list wrapped in dictionary (below)

        .. code: json

            {
                'SpotPriceHistory': [
                    {
                        'AvailabilityZone': 'eu-west-1a',
                        'InstanceType': 'm5d.4xlarge',
                        'ProductDescription': 'Red Hat Enterprise Linux',
                        'SpotPrice': '0.420000',
                        'Timestamp': datetime.datetime(2019, 8, 11, 23, 56, 50, tzinfo=tzutc())
                    },
                    {
                        'AvailabilityZone': 'eu-west-1a',
                        'InstanceType': 'm5d.4xlarge',
                        ...
                    }
                ]
            }
        """
        self.d = data['SpotPriceHistory'] if isinstance(data, dict) else data
        self.formatted = [x['Timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ') for x in self.d]
        self.prices = self.convert(self.d)

    def convert(self, pricelist):
        """
        Converts datetime object embedded in a dictionary
        schema to utc datetime string format

        Args:
            :pricelist (list): list of spot price dictionaries
                with time represented as a datetime object

        Returns:
            list of dictionaries, TYPE: list

        .. code: json

            {
                'AvailabilityZone': 'eu-west-1a',
                'InstanceType': 'm5d.4xlarge',
                'ProductDescription': 'Red Hat Enterprise Linux',
                'SpotPrice': '0.420000',
                'Timestamp': '2019-08-11T23:56:50Z'
            }

        """
        for index, pdict in enumerate(pricelist):
            pricelist[index]['Timestamp'] = self.formatted[index]
        return pricelist
