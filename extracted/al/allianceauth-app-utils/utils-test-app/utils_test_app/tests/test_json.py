import datetime as dt
import json
from unittest import TestCase

from app_utils.json import JSONDateTimeDecoder, JSONDateTimeEncoder


class TestJsonSerializers(TestCase):
    def test_should_encode_and_decode_with_naive_datetime(self):
        # given
        my_dt = dt.datetime.now()
        obj = {"alpha": 1, "my_data": my_dt}
        # when
        data_json = json.dumps(obj, cls=JSONDateTimeEncoder)
        obj_2 = json.loads(data_json, cls=JSONDateTimeDecoder)
        # then
        self.assertDictEqual(obj, obj_2)

    def test_should_encode_and_decode_with_aware_datetime_utc(self):
        # given
        my_dt = dt.datetime.now(tz=dt.timezone.utc)
        obj = {"alpha": 1, "my_data": my_dt}
        # when
        data_json = json.dumps(obj, cls=JSONDateTimeEncoder)
        obj_2 = json.loads(data_json, cls=JSONDateTimeDecoder)
        # then
        self.assertDictEqual(obj, obj_2)

    # def test_should_encode_and_decode_with_aware_datetime_other(self):
    #     # given
    #     dt_unware = dt.datetime.now()
    #     localtz = pytz.timezone("Europe/Lisbon")
    #     dt_aware = localtz.localize(dt_unware)
    #     obj = {"alpha": 1, "my_data": dt_aware}
    #     # when
    #     data_json = json.dumps(obj, cls=JSONDateTimeEncoder)
    #     obj_2 = json.loads(data_json, cls=JSONDateTimeDecoder)
    #     # then
    #     self.assertDictEqual(obj, obj_2)

    def test_should_encode_and_decode_without_datetime(self):
        # given
        obj = {"alpha": 1}
        # when
        data_json = json.dumps(obj, cls=JSONDateTimeEncoder)
        obj_2 = json.loads(data_json, cls=JSONDateTimeDecoder)
        # then
        self.assertDictEqual(obj, obj_2)
