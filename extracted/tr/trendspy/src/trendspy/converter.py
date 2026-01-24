import numpy as np
import pandas as pd
from .utils import *

_RELATED_QUERIES_DESIRED_COLUMNS  = ['query','topic','title','type','mid','value']

class TrendsDataConverter:
	"""
	Converts raw Google Trends API responses to pandas DataFrames.

	This class provides static methods for converting various types of
	Google Trends data into more usable formats.

	Methods:
		interest_over_time: Converts timeline data
		related_queries: Converts related queries data
		geo_data: Converts geographic data
		suggestions: Converts search suggestions
		rss_items: Parses RSS feed items
	"""
	@staticmethod
	def token_to_bullets(token_data):
		items = token_data.get('request', {}).get('comparisonItem', [])
		bullets = [item.get('complexKeywordsRestriction', {}).get('keyword', [''])[0].get('value','') for item in items]
		metadata = [next(iter(item.get('geo', {'':'unk'}).values()), 'unk') for item in items]
		if len(set(metadata))>1:
			bullets = [b+' | '+m for b,m in zip(bullets, metadata)]
		metadata = [item.get('time', '').replace('\\', '') for item in items]
		if len(set(metadata))>1:
			bullets = [b+' | '+m for b,m in zip(bullets, metadata)]

		return bullets

	@staticmethod
	def interest_over_time(widget_data, keywords, time_as_index=True):
		"""
		Converts interest over time data to a pandas DataFrame.

		Parameters:
			widget_data (dict): Raw API response data
			keywords (list): List of keywords for column names
			time_as_index (bool): Use time as DataFrame index

		Returns:
			pandas.DataFrame: Processed interest over time data
		"""
		timeline_data = widget_data
		timeline_data = timeline_data.get('default', timeline_data)
		timeline_data = timeline_data.get('timelineData', timeline_data)
		if not timeline_data:
			return pd.DataFrame(columns=keywords)


		df_data = np.array(extract_column(timeline_data, 'value')).reshape(len(timeline_data), -1)
		df_data = dict(zip(keywords, df_data.T))
		if ('isPartial' in timeline_data[-1]) or any('isPartial' in row for row in timeline_data):
			df_data['isPartial'] = extract_column(timeline_data, 'isPartial', False)


		timestamps = extract_column(timeline_data, 'time', f=lambda x:int(x) if x else None)
		timestamps = np.array(timestamps, dtype='datetime64[s]').astype('datetime64[ns]')
		# timestamps += np.timedelta64(get_utc_offset_minutes(), 'm')
		if time_as_index:
			return pd.DataFrame(df_data, index=pd.DatetimeIndex(timestamps, name='time [UTC]'))
		return pd.DataFrame({'time':timestamps, **df_data})

	@staticmethod
	def multirange_interest_over_time(data, bullets=None):
		data = data.get('default', {}).get('timelineData', [{}])
		if not 'columnData' in data[0]:
			return pd.DataFrame()

		num_parts = len(data[0]['columnData'])
		if bullets is None:
			bullets = ['keyword_'+str(i) for i in range(num_parts)]

		df_data = {}
		for i in range(num_parts):
			timeline_data = [item['columnData'][i] for item in data]
			df_data[bullets[i]] = extract_column(timeline_data, 'value', f=lambda x:x if x!=-1 else None)

			if ('isPartial' in timeline_data[-1]) or any('isPartial' in row for row in timeline_data):
				df_data['isPartial_'+str(i)] = extract_column(timeline_data, 'isPartial', False)

			timestamps = extract_column(timeline_data, 'time', f=lambda ts:int(ts) if ts else None)
			timestamps = np.array(timestamps, dtype='datetime64[s]').astype('datetime64[ns]')
			df_data['index_'+str(i)] = timestamps
		return pd.DataFrame(df_data)

	@staticmethod
	def related_queries(widget_data):
		ranked_data 	 = widget_data.get('default',{}).get('rankedList')
		if not ranked_data:
			return {'top':pd.DataFrame(), 'rising':pd.DataFrame()}	
		
		result           = {}
		result['top']    = pd.DataFrame(flatten_data(filter_data(ranked_data[0]['rankedKeyword'], _RELATED_QUERIES_DESIRED_COLUMNS), ['topic']))
		result['rising'] = pd.DataFrame(flatten_data(filter_data(ranked_data[1]['rankedKeyword'], _RELATED_QUERIES_DESIRED_COLUMNS), ['topic']))
		return result

	@staticmethod
	def geo_data(widget_data, bullets=None):
		data = widget_data.get('default', {}).get('geoMapData', [])
		filtered_data = list(filter(lambda item:item['hasData'][0], data))
		if not filtered_data:
			return pd.DataFrame()
		
		num_keywords = len(filtered_data[0]['value'])
		if not bullets:
			bullets = ['keyword_'+str(i) for i in range(num_keywords)]

		found_cols = set(filtered_data[0].keys()) & {'coordinates', 'geoCode', 'geoName', 'value'}
		df_data = {}
		df_data['geoName'] = extract_column(filtered_data, 'geoName')
		if 'geoCode' in found_cols:
			df_data['geoCode'] = extract_column(filtered_data, 'geoCode')
		if 'coordinates' in found_cols:
			df_data['lat'] = extract_column(filtered_data, 'coordinates', f=lambda x:x['lat'])
			df_data['lng'] = extract_column(filtered_data, 'coordinates', f=lambda x:x['lng'])

		values = np.array(extract_column(filtered_data, 'value')).reshape(len(filtered_data), -1)
		for keyword,values_row in zip(bullets, values.T):
			df_data[keyword] = values_row
		return pd.DataFrame(df_data)
	
	@staticmethod
	def suggestions(data):
		return pd.DataFrame(data['default']['topics'])
	
	@staticmethod
	def rss_items(data):
		item_pattern = re.compile(r'<item>(.*?)</item>', re.DOTALL)
		items = list(map(lambda item:parse_xml_to_dict(item, 'ht:'), item_pattern.findall(data)))
		return items
	
	@staticmethod
	def trending_now_showcase_timeline(data, request_timestamp=None):
		lens = [len(item[1]) for item in data]
		min_len, max_len = min(lens), max(lens)
		if min_len in {30,90,180,42}:
			max_len = min_len + 1

		time_offset = 480 if max_len < 32 else 14400 if max_len < 45 else 960

		timestamp = int(request_timestamp or datetime.now(timezone.utc).timestamp())
		timestamps = [timestamp // time_offset * time_offset - time_offset * i for i in range(max_len+2)][::-1]
		timestamps = np.array(timestamps, dtype='datetime64[s]').astype('datetime64[ns]')
		if (timestamp%time_offset) <= 60: # Time delay determined empirically
			df_data = {item[0]:item[1][-min_len:] for item in data}
			df = pd.DataFrame(df_data, index=timestamps[:-1][-min_len:])
			return df
		
		res = {}
		for item in data:
			res[item[0]] = np.pad(item[1], (0, max_len - len(item[1])), mode='constant', constant_values=0)
		df = pd.DataFrame(res, index=timestamps[-max_len:])
		return df