import asyncio
from typing import Union
import pandas as pd
from collections.abc import Callable
from rapidfuzz import process, fuzz
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas
from ..interfaces.databases import DBSupport

def preprocess_address(address):
    """Preprocess Address for Fuzzy String Matching.
    

        Example:

        ```yaml
        PlacerStores:
          location_field: find_address
        ```

    """
    if pd.isnull(address):
        return ""
    # Convert to lowercase, remove punctuation, and strip whitespace
    address = address.replace('.', '').strip()
    return address


class PlacerStores(DBSupport, tPandas):
    """
    PlacerStores.

    Overview

    The `PlacerStores` is used to match PlacerAI stores with Stores tables at different schemas.

    Properties

    :widths: auto

    | location_field   | Yes      | str       | The name of the column to be used for matching.                                   |

    Return
       A New Dataframe with all stores matching using a Fuzzy Search Match.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PlacerStores:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._column: Union[str, list] = kwargs.pop("location_field", None)
        self._account: str = kwargs.pop("account_field", 'program_slug')
        if not self._column:
            raise ConfigError(
                "PlacerStores requires a column for matching => **location_field**"
            )
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def find_best_match(self, address, choices, threshold: int = 80, token_threshold: int = 80):
        """
        Find the best fuzzy match for a given address.

        Parameters:
        - address (str): The address to match.
        - choices (list): List of addresses to match against.
        - threshold (int): Minimum similarity score to consider a match.

        Returns:
        - best_match (str) or None: The best matching address or None if no match meets the threshold.
        - score (int): The similarity score of the best match.
        """
        match = process.extractOne(address, choices, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            return match[0], match[1]

        # evaluate if all tokens (words) are matching on different order:
        match = process.extractOne(address, choices, scorer=fuzz.token_set_ratio)
        if match and match[1] >= token_threshold:
            return match[0], match[1]

        # still not match, return None
        return None, None

    def match_addresses(self, data_row, store_addresses, df_stores):
        best_match, score = self.find_best_match(
            data_row[self._column], store_addresses, threshold=80)
        if best_match:
            matched_store = df_stores[df_stores[self._column] == best_match].iloc[0]
            return pd.Series({
                'store_id': matched_store['store_id'],
                'place_id': matched_store['place_id'],
                'plus_code': matched_store['plus_code'],
                'location_code': matched_store['location_code'],
                'formatted_address': matched_store['formatted_address'],
                'matched_formatted_address': matched_store[self._column],
                'similarity_score': score
            })
        else:
            return pd.Series({
                'store_id': None,
                'place_id': None,
                'plus_code': None,
                'location_code': None,
                'formatted_address': None,
                'matched_formatted_address': None,
                'similarity_score': score
            })

    async def _run(self):
        try:
            # Create a Group By program_slug to extract the retailers:
            retailers = self.data[self._account].drop_duplicates().reset_index(drop=True)
            # Preprocess addresses for primary stores:
            self.data[self._column] = self.data[self._column].apply(preprocess_address)
            
            # Create a copy of the original DataFrame to preserve original data
            result_df = self.data.copy()
            matches_found = False

            # Iterate over every retailer and query the list of stores for that particular program:
            db = self.default_connection('pg')
            for retailer in retailers.values:
                # Skip invalid retailer names (like <NA>)
                if pd.isna(retailer) or not isinstance(retailer, str):
                    self._logger.warning(f'Skipping invalid retailer name: {retailer}')
                    continue

                self._logger.notice(f' Evaluating Program {retailer} ...')
                
                # Check if schema exists before querying
                schema_query = """
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.schemata 
                        WHERE schema_name = $1
                    );
                """
                async with await db.connection() as conn:
                    try:
                        exists = await conn.fetchval(schema_query, retailer)
                        if not exists:
                            self._logger.warning(f'Schema {retailer} does not exist in database')
                            continue

                        # If schema exists, proceed with original query
                        query = f"""
                            SELECT 
                                store_id, 
                                place_id, 
                                plus_code, 
                                formatted_address,
                                formatted_address as {self._column}, 
                                location_code 
                            FROM {retailer}.stores
                        """
                        result = await conn.fetchall(query)
                        if not result:
                            self._logger.warning(f'No stores found for retailer {retailer}')
                            continue
                            
                        df_stores = pd.DataFrame([dict(store) for store in result])
                        
                    except Exception as e:
                        self._logger.error(f'Error querying database for {retailer}: {str(e)}')
                        continue

                    if df_stores.empty:
                        self._logger.warning(f'No Stores Found for Program {retailer}')
                        continue

                    # Preprocess addresses for secondary stores:
                    df_stores[self._column] = df_stores[self._column].apply(preprocess_address)
                    store_addresses = df_stores[self._column].tolist()
                    df_data = result_df[result_df[self._account] == retailer].copy()
                    
                    if df_data.empty:
                        self._logger.warning(f'No data to match for retailer {retailer}')
                        continue

                    matched_df = df_data.apply(
                        self.match_addresses,
                        axis=1,
                        store_addresses=store_addresses,
                        df_stores=df_stores
                    )

                    if not matched_df.empty:
                        matches_found = True
                        # First update all columns except formatted_address
                        for col in ['store_id', 'place_id', 'plus_code', 'location_code']:
                            if col not in result_df.columns:
                                result_df[col] = None 
                            result_df[col] = result_df[col].astype(object)  
                            result_df.loc[df_data.index, col] = matched_df[col]
                        
                        # Ensure formatted_address column exists
                        if 'formatted_address' not in result_df.columns:
                            result_df['formatted_address'] = None
                        
                        # Create mask for rows where formatted_address is empty
                        empty_mask = (
                            result_df['formatted_address'].isna() | 
                            (result_df['formatted_address'] == '') |
                            (result_df['formatted_address'].str.strip() == '')
                        )
                        # Combine with current retailer mask
                        update_mask = empty_mask & (result_df[self._account] == retailer)
                        
                        # Update formatted_address only where it's empty
                        result_df.loc[update_mask, 'formatted_address'] = matched_df.loc[update_mask[update_mask].index, 'formatted_address']
                        
                        # Add temporary columns for join
                        result_df.loc[df_data.index, f'matched_{self._column}'] = matched_df['matched_formatted_address']
                        result_df.loc[df_data.index, 'similarity_score'] = matched_df['similarity_score']

            # If no matches were found, return original DataFrame
            if not matches_found:
                self._logger.warning('No matches found for any retailer')
                return self.data

            # Remove temporary columns if they exist
            try:
                result_df = result_df.drop(
                    columns=[f'matched_{self._column}', 'similarity_score']
                )
            except KeyError:
                pass

            # Log results
            matched_stores = result_df[result_df['store_id'].notna()]
            self._logger.info(f"Total matches found: {len(matched_stores)}/{len(result_df)}")

            return result_df

        except Exception as err:
            self._logger.error(f"Error processing data: {str(err)}")
            raise ComponentError(
                f"Generic Error on Data: error: {str(err)}"
            ) from err
