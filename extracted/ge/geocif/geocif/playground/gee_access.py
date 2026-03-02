import os
import ee
import geemap
import pandas as pd
import geopandas as gpd
from datetime import datetime
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Earth Engine
try:
    ee.Initialize()
    logging.info("Successfully initialized Earth Engine.")
except Exception as e:
    logging.info("Initializing Earth Engine Authentication.")
    ee.Authenticate()
    ee.Initialize()
    logging.info("Successfully authenticated and initialized Earth Engine.")


class SatelliteDataProcessor:
    def __init__(self, shapefile_path, start_date_col, end_date_col, data_source='HLS',
                 output_folder='downloads', stats=['mean'], percentiles=[25, 50, 75],
                 field_id_col=None, buffer_size=30):
        """
        Initialize the SatelliteDataProcessor with user-supplied parameters.
        """
        self.shapefile_path = shapefile_path
        self.start_date_col = start_date_col
        self.end_date_col = end_date_col
        self.data_source = data_source
        self.output_folder = output_folder
        self.stats = stats
        self.percentiles = percentiles
        self.field_id_col = field_id_col
        self.buffer_size = buffer_size
        self.gdf = None
        self.ee_feature_collection = None

        # Ensure output directory exists
        os.makedirs(self.output_folder, exist_ok=True)
        logging.info(f"Output directory '{self.output_folder}' is ready.")

        # Load and prepare shapefile
        self.load_shapefile()

    def load_shapefile(self):
        """
        Load the shapefile into a GeoDataFrame, ensure valid geometries,
        handle CRS for accurate buffering, and convert to GEE FeatureCollection.
        """
        try:
            self.gdf = gpd.read_file(self.shapefile_path)
            logging.info(f"Shapefile '{self.shapefile_path}' loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load shapefile '{self.shapefile_path}': {e}")
            raise

        # Ensure geometries are valid
        self.gdf['geometry'] = self.gdf['geometry'].apply(
            lambda geom: geom if geom.is_valid else geom.buffer(0)
        )
        logging.info("Validated and corrected geometries.")

        # Handle CRS: Buffering requires a projected CRS. Reproject if necessary.
        if self.gdf.crs is None:
            logging.error("Shapefile has no CRS defined. Please define a CRS.")
            raise ValueError("Shapefile has no CRS defined.")
        else:
            logging.info(f"Shapefile CRS is projected: {self.gdf.crs}")

        # Convert date columns to proper format
        self.gdf[self.start_date_col] = self.gdf[self.start_date_col].apply(self.format_date)
        self.gdf[self.end_date_col] = self.gdf[self.end_date_col].apply(self.format_date)
        logging.info("Formatted date columns.")

        # Convert GeoDataFrame to GEE FeatureCollection
        self.ee_feature_collection = self.gdf_to_gee(self.gdf)
        logging.info("Converted GeoDataFrame to Earth Engine FeatureCollection.")

    @staticmethod
    def get_utm_crs(lon, lat):
        """
        Determine the UTM CRS based on longitude and latitude.
        """
        utm_band = int((lon + 180) / 6) + 1
        if lat >= 0:
            epsg_code = 32600 + utm_band
        else:
            epsg_code = 32700 + utm_band
        return f"EPSG:{epsg_code}"

    @staticmethod
    def format_date(date_input):
        """
        Convert date input to 'YYYY-MM-DD' format or 'YYYY' if only year is provided.
        Supports 'DD-MM-YYYY', 'YYYY-MM-DD', 'YYYY', and float formats.
        """
        if pd.isnull(date_input):
            return None
        # Handle float inputs
        if isinstance(date_input, float):
            if date_input.is_integer():
                date_input = int(date_input)
                logging.debug(f"Converted float {date_input} to integer for date processing.")
            else:
                logging.warning(f"Float date '{date_input}' has a fractional part. Treating as invalid date.")
                return None
        # Convert to string if not already
        if not isinstance(date_input, str):
            date_input = str(date_input).strip()
        else:
            date_input = date_input.strip()

        # Attempt to parse full dates
        for fmt in ('%d-%m-%Y', '%Y-%m-%d'):
            try:
                return datetime.strptime(date_input, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        # Attempt to parse year-only format
        try:
            return datetime.strptime(date_input, '%Y').strftime('%Y')
        except ValueError:
            pass
        logging.warning(
            f"Invalid date format: '{date_input}'. Expected 'DD-MM-YYYY', 'YYYY-MM-DD', 'YYYY', or integer year.")
        return None

    @staticmethod
    def gdf_to_gee(gdf):
        """
        Converts a GeoDataFrame to an Earth Engine FeatureCollection.
        """
        features = []
        for idx, row in gdf.iterrows():
            geom = row['geometry'].__geo_interface__
            # Use specified field identifier or 'id'
            properties = row.drop('geometry').to_dict()
            feature = ee.Feature(ee.Geometry(geom), properties)
            features.append(feature)
        return ee.FeatureCollection(features)

    def mask_edge(self, image):
        """
        Apply edge masking to Sentinel-1 VV band images.
        Masks pixels with values less than -30.0 dB.

        Parameters:
        - image: ee.Image to be masked.

        Returns:
        - Masked ee.Image.
        """
        edge = image.lt(-30.0)
        masked_image = image.mask().And(edge.Not())
        return image.updateMask(masked_image)

    def apply_cloud_mask_hls(self, image):
        """
        Apply cloud mask for HLS using the Fmask band.
        """
        fmask = image.select('Fmask')
        return image.updateMask(fmask.eq(0))

    def apply_cloud_mask_s2(self, image):
        """
        Apply cloud mask for Sentinel-2 using the SCL band.
        """
        scl = image.select('SCL')
        # Remap classes: 4=Vegetation, 5=Bare Soil, 6=Water, 7=Unclassified, 11=Snow
        mask = scl.remap([4, 5, 6, 7, 11], [1, 1, 1, 1, 1], 0)
        return image.updateMask(mask.eq(1))

    def apply_cloud_mask_sentinel1(self, image):
        """
        Sentinel-1 is radar data and not affected by clouds.
        Apply edge masking using the provided mask_edge function.
        """
        # Apply edge masking
        image = self.mask_edge(image)
        return image

    def apply_cloud_mask(self, image):
        """
        Apply cloud masking depending on the data source.
        """
        if self.data_source == 'Sentinel-1':
            return self.apply_cloud_mask_sentinel1(image)
        elif self.data_source == 'HLS':
            return self.apply_cloud_mask_hls(image)
        elif self.data_source == 'Sentinel-2':
            return self.apply_cloud_mask_s2(image)
        else:
            logging.warning(f"Unknown data source '{self.data_source}'. No cloud masking applied.")
            return image

    def apply_qa_mask(self, image):
        """
        Placeholder for additional QA masking if needed.
        """
        return image

    def download_and_compute_indices(self):
        """
        Download satellite data and compute vegetation indices for each geometry for each available date.
        """
        # Get features as a list
        try:
            features = self.ee_feature_collection.getInfo()['features']
            logging.info(f"Processing {len(features)} features.")
        except Exception as e:
            logging.error(f"Failed to retrieve features from FeatureCollection: {e}")
            return

        total_features = len(features)
        for idx, feat in enumerate(features, start=1):
            feature_id = feat['properties'].get(self.field_id_col, 'unknown') if self.field_id_col else feat[
                'properties'].get('id', 'unknown')
            logging.info(f"Processing feature {idx}/{total_features}: '{feature_id}'")
            self.process_feature(feat)

    def process_feature(self, feature_info):
        """
        Process a single feature: For each available date in the given date range,
        compute vegetation indices and save them into a CSV.
        """
        feature = ee.Feature(feature_info)
        geom = feature.geometry()
        properties = feature_info['properties']

        # Retrieve start and end dates
        start_date = properties.get(self.start_date_col)
        end_date = properties.get(self.end_date_col)

        # Retrieve field identifier
        if self.field_id_col:
            field_identifier = properties.get(self.field_id_col, 'unknown')
        else:
            field_identifier = properties.get('id', 'unknown')

        feature_id = field_identifier if self.field_id_col else properties.get('id', 'unknown')

        if not start_date or not end_date:
            logging.warning(f"Skipping feature '{feature_id}': Missing start or end date.")
            return

        # Handle year-based data retrieval
        if start_date == end_date and len(start_date) == 4:
            try:
                year = int(start_date)
                if self.data_source == 'HLS' and year < 2018:
                    logging.warning(
                        f"Feature '{feature_id}': HLS data not available for year '{year}'. Skipping feature.")
                    return
                if self.data_source == 'Sentinel-1' and year < 2014:
                    logging.warning(
                        f"Feature '{feature_id}': Sentinel-1 data not available for year '{year}'. Skipping feature.")
                    return
                start_date = f"{year}-01-01"
                end_date = f"{year}-12-31"
                logging.info(
                    f"Feature '{feature_id}': Detected same start and end date as year '{year}'. Setting date range to entire year.")
            except ValueError:
                logging.warning(f"Feature '{feature_id}': Invalid year format '{start_date}'. Skipping feature.")
                return
        if year < 2019:
            logging.warning(f"Feature '{feature_id}': Data not available before 2019. Skipping feature.")
            return

        # Define image collection and bands based on data source
        if self.data_source == 'HLS':
            collection = ee.ImageCollection('NASA/HLS/HLSL30/v002').filterDate(start_date, end_date).filterBounds(geom)
            bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'Fmask']
            scale = 30
        elif self.data_source == 'Sentinel-1':
            collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
                .filterDate(start_date, end_date) \
                .filterBounds(geom) \
                .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV').Or(
                ee.Filter.listContains('transmitterReceiverPolarisation', 'HH')))
            bands = ['VV', 'VH']  # Initial assumption; will adjust based on available bands
            scale = 10
        elif self.data_source == 'Sentinel-2':
            collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate(start_date,
                                                                                      end_date).filterBounds(geom)
            bands = ['B2', 'B3', 'B4', 'B8', 'SCL']
            scale = 10
        else:
            logging.error(f"Unsupported data source '{self.data_source}'. Skipping feature '{feature_id}'.")
            return

        try:
            # Get collection size
            collection_size = collection.size().getInfo()
            logging.info(f"Feature '{feature_id}': Found {collection_size} images in the collection.")
            if collection_size == 0:
                logging.warning(f"No images found for feature '{feature_id}' within the specified date range.")
                return

            # Convert collection to a list for iteration
            image_list = collection.toList(collection_size)
            all_records = []

            for i in range(collection_size):
                img = ee.Image(image_list.get(i))

                # Detect if original geometry is a point and buffer if necessary
                geom_type = feature.geometry().type().getInfo()

                if geom_type == 'Point':
                    # Buffer by buffer_size meters
                    buffered_geom = geom.buffer(self.buffer_size)
                    logging.debug(
                        f"Feature '{feature_id}': Geometry is a Point. Buffered by {self.buffer_size} meters.")
                else:
                    buffered_geom = geom

                # Log buffered geometry bounds
                bounds = buffered_geom.bounds().getInfo()
                logging.debug(f"Feature '{feature_id}': Buffered Geometry Bounds: {bounds}")

                # Apply cloud and QA masks
                img = self.apply_cloud_mask(img)
                img = self.apply_qa_mask(img)

                # Adjust bands for Sentinel-1 based on available bands
                if self.data_source == 'Sentinel-1':
                    available_bands = img.bandNames().getInfo()
                    if 'VV' in available_bands and 'VH' in available_bands:
                        selected_bands = ['VV', 'VH']
                    elif 'HH' in available_bands and 'HV' in available_bands:
                        selected_bands = ['HH', 'HV']
                    else:
                        logging.error(
                            f"Feature '{feature_id}': Image does not contain required bands. Available bands: {available_bands}")
                        continue  # Skip this image

                    # Select relevant bands and clip to geometry
                    img = img.select(selected_bands).clip(buffered_geom)

                    # Compute indices based on available bands
                    indices_df = self.compute_vegetation_indices(img, buffered_geom, scale)
                    if indices_df.empty:
                        logging.warning(f"Feature '{feature_id}': No indices computed for image {i + 1}.")
                        continue
                else:
                    # Select relevant bands and clip to geometry
                    img = img.select(bands).clip(buffered_geom)

                    # Verify if selected bands exist in the image
                    available_bands = img.bandNames().getInfo()
                    missing_bands = [band for band in bands if band not in available_bands]
                    if missing_bands:
                        logging.error(
                            f"Feature '{feature_id}': Image does not contain bands {missing_bands}. Available bands: {available_bands}")
                        continue  # Skip this image

                    # Get image date
                    img_date = ee.Date(img.get('system:time_start')).format('YYYY-MM-DD').getInfo()
                    logging.debug(f"Feature '{feature_id}': Processing image dated {img_date}.")

                    # Compute indices for this single-date image
                    indices_df = self.compute_vegetation_indices(img, buffered_geom, scale)
                    if indices_df.empty:
                        logging.warning(f"Feature '{feature_id}': No indices computed for image {i + 1}.")
                        continue

                if not indices_df.empty:
                    # Add identification and date columns
                    indices_df['feature_id'] = feature_id
                    indices_df['field_id'] = properties.get(self.field_id_col,
                                                            'unknown') if self.field_id_col else properties.get('id',
                                                                                                                'unknown')
                    if self.data_source == 'Sentinel-1':
                        # Sentinel-1 images have dates; extract from metadata
                        img_date = ee.Date(img.get('system:time_start')).format('YYYY-MM-DD').getInfo()
                        indices_df['date'] = img_date
                    else:
                        indices_df['date'] = img_date
                    all_records.append(indices_df)

            if all_records:
                final_df = pd.concat(all_records, ignore_index=True)
                csv_name = f"{self.output_folder}/{feature_id}_{self.data_source}_{start_date}_{end_date}_indices.csv"
                final_df.to_csv(csv_name, index=False)
                logging.info(f"Processed and saved data for feature '{feature_id}'.")
            else:
                logging.warning(f"No valid data found for feature '{feature_id}' after processing.")
        except:
            logging.error(f"Failed to process feature '{feature_id}': {e}")

    def compute_vegetation_indices(self, image, geometry, scale):
        """
        Compute vegetation or radar indices for the provided image.
        """
        reducers = self.get_reducers()
        indices_list = []

        if self.data_source == 'HLS':
            # HLS band mapping: NIR=B5, RED=B4, GREEN=B3, BLUE=B2
            indices = {}
            indices['NDVI'] = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
            indices['EVI'] = image.expression(
                '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
                    'NIR': image.select('B5'),
                    'RED': image.select('B4'),
                    'BLUE': image.select('B2')
                }).rename('EVI')
            indices['NDWI'] = image.normalizedDifference(['B3', 'B5']).rename('NDWI')
            indices['GNDVI'] = image.normalizedDifference(['B5', 'B3']).rename('GNDVI')
            indices['SAVI'] = image.expression(
                '((NIR - RED) / (NIR + RED + L)) * (1 + L)', {
                    'NIR': image.select('B5'),
                    'RED': image.select('B4'),
                    'L': 0.5
                }).rename('SAVI')
            indices['MSAVI'] = image.expression(
                '(2 * NIR + 1 - sqrt((2 * NIR + 1)**2 - 8 * (NIR - RED))) / 2', {
                    'NIR': image.select('B5'),
                    'RED': image.select('B4')
                }).rename('MSAVI')

        elif self.data_source == 'Sentinel-2':
            # Sentinel-2: NIR=B8, RED=B4, GREEN=B3, BLUE=B2
            indices = {}
            indices['NDVI'] = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            indices['EVI'] = image.expression(
                '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4'),
                    'BLUE': image.select('B2')
                }).rename('EVI')
            indices['NDWI'] = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
            indices['GNDVI'] = image.normalizedDifference(['B8', 'B3']).rename('GNDVI')
            indices['SAVI'] = image.expression(
                '((NIR - RED) / (NIR + RED + L)) * (1 + L)', {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4'),
                    'L': 0.5
                }).rename('SAVI')
            indices['MSAVI'] = image.expression(
                '(2 * NIR + 1 - sqrt((2 * NIR + 1)**2 - 8 * (NIR - RED))) / 2', {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4')
                }).rename('MSAVI')

        elif self.data_source == 'Sentinel-1':
            # Sentinel-1: RVI computation handled based on available bands
            indices = {}
            available_bands = image.bandNames().getInfo()
            if 'VV' in available_bands and 'VH' in available_bands:
                indices['RVI'] = image.expression(
                    '4 * VH / (VV + VH)', {
                        'VV': image.select('VV'),
                        'VH': image.select('VH')
                    }).rename('RVI')
            elif 'HH' in available_bands and 'HV' in available_bands:
                indices['RVI'] = image.expression(
                    '4 * HV / (HH + HV)', {
                        'HH': image.select('HH'),
                        'HV': image.select('HV')
                    }).rename('RVI')
            else:
                # No valid bands for RVI
                logging.warning("Sentinel-1 image does not have the required bands for RVI computation.")
                return pd.DataFrame()

            # Optionally include individual bands
            if 'VV' in available_bands:
                indices['VV'] = image.select('VV')
            if 'VH' in available_bands:
                indices['VH'] = image.select('VH')
            if 'HH' in available_bands:
                indices['HH'] = image.select('HH')
            if 'HV' in available_bands:
                indices['HV'] = image.select('HV')

        else:
            # Unknown source, no indices
            logging.warning(f"Unknown data source '{self.data_source}'. No indices computed.")
            indices = {}

        # Compute statistics for each index
        for index_name, index_image in indices.items():
            stats_dict = index_image.reduceRegion(
                reducer=self.get_reducers(),
                geometry=geometry,
                scale=scale,
                bestEffort=True
            ).getInfo()
            if stats_dict:
                for stat_key, value in stats_dict.items():
                    indices_list.append({
                        'index': index_name,
                        'statistic': stat_key,
                        'value': value
                    })

        if indices_list:
            indices_df = pd.DataFrame(indices_list)
            return indices_df
        else:
            return pd.DataFrame()

    def get_reducers(self):
        """
        Create an ee.Reducer based on specified statistics.
        """
        reducers = []
        if 'mean' in self.stats:
            reducers.append(ee.Reducer.mean().setOutputs(['mean']))
        if 'median' in self.stats:
            reducers.append(ee.Reducer.median().setOutputs(['median']))
        if 'stdDev' in self.stats:
            reducers.append(ee.Reducer.stdDev().setOutputs(['stdDev']))
        if 'min' in self.stats:
            reducers.append(ee.Reducer.min().setOutputs(['min']))
        if 'max' in self.stats:
            reducers.append(ee.Reducer.max().setOutputs(['max']))
        if 'percentile' in self.stats:
            reducers.append(ee.Reducer.percentile(self.percentiles).setOutputs([f'p{p}' for p in self.percentiles]))

        if reducers:
            # Combine reducers into a single reducer
            combined_reducer = reducers[0]
            for r in reducers[1:]:
                combined_reducer = combined_reducer.combine(r, sharedInputs=True)
            return combined_reducer
        else:
            # Default to mean if no reducers are specified
            return ee.Reducer.mean().setOutputs(['mean'])

    def format_indices(self, index_name, stats_dict):
        """
        Format the indices into a list of dictionaries with 'index', 'statistic', 'value'.
        """
        formatted_list = []
        for stat_key, value in stats_dict.items():
            formatted_list.append({
                'index': index_name,
                'statistic': stat_key,
                'value': value
            })
        return formatted_list


# Example usage
if __name__ == "__main__":
    processor = SatelliteDataProcessor(
        shapefile_path=r'C:\Users\ritvik\Downloads\Yield_Afg_2015_2021 (2)\Yield_data_2015to2021_field_level.shp',  # Replace with your shapefile path
        start_date_col='Year',  # Replace with your start date column name
        end_date_col='Year',  # Replace with your end date column name
        data_source='Sentinel-2',  # Options: 'HLS', 'Sentinel-1', 'Sentinel-2'
        output_folder='downloads',
        stats=['mean', 'median'],
        percentiles=[25],
        field_id_col='Pnt_Id'  # Replace with your field identifier column name, if any
    )

    processor.download_and_compute_indices()
