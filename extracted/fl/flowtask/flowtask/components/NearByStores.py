import asyncio
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from concurrent.futures import ProcessPoolExecutor
from .flow import FlowComponent
from ..exceptions import ComponentError, DataNotFound


class NearByStores(FlowComponent):
    """
    NearByStores.

    Overview:
        Calculates the nearest stores to an employee location.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          NearByStores:
          depends:
          - QueryToPandas_1
          - QueryToPandas_2
          radius: 50
        ```
    """
    _version = "1.0.0"
    async def start(self, **kwargs):
        if self.previous:
            try:
                self.df1: pd.DataFrame = self.previous[0].output()
                self.df2: pd.DataFrame = self.previous[1].output()
            except IndexError:
                raise ComponentError(
                    "NearByStores Requires 2 Dataframes", status=404
                )
        else:
            raise DataNotFound(
                "Data Not Found", status=404
            )
        await super().start(**kwargs)
        return True

    async def close(self):
        pass

    def _print_data_(self, df: pd.DataFrame, title: str = None):
        if not title:
            title = self.__class__.__name__
        print(f"::: Printing {title} === ")
        print("Data: ", df)
        if df.empty:
            print("The DataFrame is empty.")
        else:
            for column, t in df.dtypes.items():
                print(f"{column} -> {t} -> {df[column].iloc[0]}")

    def _find_nearby_stores(self, employee_row, stores_gdf, employees_gdf):
        # Employee's buffer geometry
        employee_buffer = employee_row['buffer']
        employee_buffer_gdf = gpd.GeoDataFrame(
            {'geometry': [employee_buffer]}, crs=employees_gdf.crs
        )

        # Spatial join to find stores within the buffer
        nearby_stores = gpd.sjoin(
            stores_gdf, employee_buffer_gdf, how='inner', predicate='intersects'
        )

        # If no stores are found, return an empty list
        if nearby_stores.empty:
            return []

        # Build a list of dictionaries combining employee and store information
        rows = []
        employee_info = {
            'associate_oid': employee_row['associate_oid'],
            'corporate_email': employee_row['corporate_email'],
            'employee_coordinates': (employee_row.geometry.y, employee_row.geometry.x),
            'employee_position': (employee_row.latitude, employee_row.longitude)
        }

        for idx, store_row in nearby_stores.iterrows():
            store_info = {
                'store_id': store_row['store_id'],
                'store_name': store_row['store_name'],
                'store_coordinates': (store_row.geometry.y, store_row.geometry.x),
                'store_position': (store_row.latitude, store_row.longitude),
                'visit_rule': store_row.get('visit_rule', None),
                'visit_category': store_row.get('visit_category', None)
            }
            # Combine employee and store info
            combined_row = {**employee_info, **store_info}
            rows.append(combined_row)

        return rows

    async def _async_find_nearby_stores(self, employee_row, stores_gdf, employees_gdf):
        try:
            result = await asyncio.to_thread(
                self._find_nearby_stores,
                employee_row,
                stores_gdf,
                employees_gdf
            )
            return result
        except Exception as e:
            # Log the exception and return None
            print(f"An error occurred: {e}")
            return None

    async def run(self):
        # Create geometry columns for employees
        self.df2['geometry'] = self.df2.apply(
            lambda row: Point(row['longitude'], row['latitude']), axis=1
        )
        employees_gdf = gpd.GeoDataFrame(self.df2, geometry='geometry', crs='EPSG:4326')

        # Create geometry columns for stores
        self.df1['geometry'] = self.df1.apply(
            lambda row: Point(row['longitude'], row['latitude']), axis=1
        )
        stores_gdf = gpd.GeoDataFrame(self.df1, geometry='geometry', crs='EPSG:4326')

        # Reproject to EPSG:3857 that allows accurate distance measurements in meters.
        employees_gdf = employees_gdf.to_crs(epsg=3857)
        stores_gdf = stores_gdf.to_crs(epsg=3857)

        # Build spatial index for stores_gdf
        stores_gdf.sindex

        # radius:
        radius = getattr(self, 'radius', 100)

        # Convert miles to meters (1 mile = 1609.34 meters)
        buffer_radius = radius * 1609.34  # 482,802 meters

        # Create buffers
        employees_gdf['buffer'] = employees_gdf.geometry.buffer(buffer_radius)

        batch_size = 50

        # Create a list of tasks
        tasks = [
            self._async_find_nearby_stores(employee_row, stores_gdf, employees_gdf)
            for _, employee_row in employees_gdf.iterrows()
        ]

        tasks_chunks = [tasks[i:i + batch_size] for i in range(0, len(tasks), batch_size)]

        results = []
        for chunk in tasks_chunks:
            # Run tasks in the chunk concurrently
            chunk_results = await asyncio.gather(*chunk)
            # Collect the rows from each result
            for result in chunk_results:
                if result:  # Check if the list is not empty
                    results.extend(result)  # Extend the results list with the returned rows

        # Concatenate all results
        if results:
            final_df = pd.DataFrame(results)
        else:
            # If no results, create an empty DataFrame with the expected columns
            final_df = pd.DataFrame(columns=[
                'associate_oid', 'corporate_email', 'employee_position',
                'store_id', 'store_position', 'visit_rule', 'visit_category'
            ])

        # Set the final output
        self._print_data_(final_df)
        self._result = final_df

        return self._result
