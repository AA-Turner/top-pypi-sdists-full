#############################################
#	Dual License: BSD-3-Clause AND MPL-2.0	#
#	Copyright (c) 2024, Adam Nogowski		#
#############################################

if __name__ == "__main__":
	from typing import Any
	from data_to_xml.xml_converter import XMLConverter
	from pathlib import Path

	my_dict: dict[str, Any] = {
	    'name': 'The Andersson\'s',
	    'size': 4,
	    'members': {
	        'total-age': 62,
	        'child': [
	            {
	                '@name': 'Tom',
	                '@sex': 'male',
	            },
	            {
	                '@name': 'Betty',
	                '@sex': 'female',
	                'grandchild': [
	                    {
	                        '@name': 'herbert',
	                        '@sex': 'male',
	                    },
	                    {
	                        '@name': 'lisa',
	                        '@sex': 'female',
	                    },
	                ]
	            },
	        ]
	    },
	}

	def write_to_file(xml: str, file_name: str) -> None:
		output_file: str = Path(f"{__file__}/../{file_name}.xml").as_posix()
		with open(file=output_file, mode="w+") as f:
			f.writelines(xml)

	xml_converter: XMLConverter = XMLConverter(my_dict=my_dict, root_node='family')
	print(xml_converter.formatted_xml)
	write_to_file(xml=xml_converter.minified_xml, file_name="minified")
	write_to_file(xml=xml_converter.formatted_xml, file_name="formatted")
