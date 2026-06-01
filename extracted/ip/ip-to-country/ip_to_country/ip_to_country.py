import ipaddress
import os
import pickle
import bisect
import csv
import importlib.resources as pkg_resources


class IpToCountry:
    def __init__(self, ipv4_pickle='ipv4_ranges.pkl', ipv6_pickle='ipv6_ranges.pkl', country_info='country_info.pkl'):
        with pkg_resources.open_binary('ip_to_country.data', ipv4_pickle) as f:
            self.ipv4_ranges = pickle.load(f)

        with pkg_resources.open_binary('ip_to_country.data', ipv6_pickle) as f:
            self.ipv6_ranges = pickle.load(f)

        with pkg_resources.open_binary('ip_to_country.data', country_info) as f:
            self.country_info = pickle.load(f)

        self.ipv4_starts = [int(start) for start, _, _ in self.ipv4_ranges]

    @staticmethod
    def build_from_directory(directory="build_files", ipv4_pickle='ipv4_ranges.pkl', ipv6_pickle='ipv6_ranges.pkl'):
        ipv4_ranges = []
        ipv6_ranges = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    for line in file:
                        if line.startswith('#') or not line.strip():
                            continue
                        parts = line.strip().split('|')
                        if len(parts) < 7:
                            continue
                        registry, cc, record_type, start, value, date, status = parts[:7]
                        if status not in ('allocated', 'assigned'):
                            continue
                        try:
                            if record_type == 'ipv4':
                                start_ip = ipaddress.IPv4Address(start)
                                num_ips = int(value)
                                end_ip = ipaddress.IPv4Address(int(start_ip) + num_ips - 1)
                                ipv4_ranges.append((start_ip, end_ip, cc))
                            elif record_type == 'ipv6':
                                network = ipaddress.IPv6Network(f"{start}/{value}", strict=False)
                                ipv6_ranges.append((network, cc))
                        except ValueError as e:
                            print(f"Skipping invalid record: {e}")
                            continue

        with open("ip_to_country/data/" + ipv4_pickle, 'wb') as f:
            ipv4_ranges.sort(key=lambda x: int(x[0]))
            pickle.dump(ipv4_ranges, f)
        with open("ip_to_country/data/" + ipv6_pickle, 'wb') as f:
            pickle.dump(ipv6_ranges, f)

        IpToCountry._build_country_codes()

    @staticmethod
    def _build_country_codes():
        country_dict = {}

        with open("build_files/country-codes.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                alpha2 = row['ISO3166-1-Alpha-2'].strip()
                if not alpha2:  # Skip rows with missing alpha-2 codes
                    continue
                # Build the data for each country
                country_info = {
                    'ISO3166-1-Alpha-2': alpha2,
                    'ISO3166-1-Alpha-3': row['ISO3166-1-Alpha-3'].strip(),
                    'region': row['Region Name'].strip(),
                    'continent': row['Continent'].strip(),
                    'languages': row['Languages'].strip().split(','),
                    'country_name': row['official_name_en'].strip(),
                    'currency': row['ISO4217-currency_name'].strip(),
                    'currency_code': row['ISO4217-currency_alphabetic_code'].strip(),
                }
                country_dict[alpha2] = country_info

        # Save to pickle
        with open("ip_to_country/data/country_info.pkl", 'wb') as f:
            pickle.dump(country_dict, f)

    def ip_to_country(self, ip):
        ip_obj = ipaddress.ip_address(ip)
        if isinstance(ip_obj, ipaddress.IPv4Address):
            cc = self._lookup_ipv4(ip_obj)
        elif isinstance(ip_obj, ipaddress.IPv6Address):
            cc = self._lookup_ipv6(ip_obj)
        else:
            raise ValueError("Unsupported IP address type")
        if cc is None:
            return None
        country_info = self.country_info.get(cc, None)
        result = {'country_code': cc}
        if country_info:
            result.update(country_info)
        return result

    def _lookup_ipv4(self, ip_obj):
        ip_int = int(ip_obj)
        idx = bisect.bisect_right(self.ipv4_starts, ip_int) - 1
        if 0 <= idx < len(self.ipv4_ranges):
            start_ip, end_ip, cc = self.ipv4_ranges[idx]
            if start_ip <= ip_obj <= end_ip:
                return cc
        return None

    def _lookup_ipv6(self, ip_obj):
        for network, cc in self.ipv6_ranges:
            if ip_obj in network:
                return cc
        return None
