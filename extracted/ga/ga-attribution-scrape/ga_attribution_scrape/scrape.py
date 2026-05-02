##import packages

import google.auth

from google.auth.transport import requests as google_requests
from apiclient.discovery import build  # pip install --upgrade google-api-python-client
from oauth2client.service_account import ServiceAccountCredentials  # pip3 install --upgrade oauth2client
from google.oauth2 import service_account

import requests
import pandas as pd
import io
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime, date as d, timedelta
import time
import os
import sys
from tqdm import tqdm

# Make all the prints red
#sys.stdout.write("\033[1;31m")


class Scrape:
    class Goals:

        def __init__(self, configuration, limit_rows=None):
            self.configuration = configuration
            self.limit_rows = limit_rows

        @property
        def _constructor(self):

            def get_ga_goals(account_id, property_id, view_id, credentials=None):

                # Build analytic authentication
                SCOPES = ['https://www.googleapis.com/auth/analytics', "https://www.googleapis.com/auth/analytics.edit",
                          "https://www.googleapis.com/auth/analytics.readonly"]

                if credentials is not None:
                    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scopes=SCOPES)
                else:
                    credentials, project_id = google.auth.default(scopes=SCOPES)
                    credentials.refresh(google_requests.Request())

                analytics = build('analytics', 'v3', credentials=credentials)

                # Get  GA Goals
                goal_response = analytics.management().goals().list(
                    accountId=account_id, webPropertyId=property_id, profileId=view_id) \
                    .execute()
                goal_response = goal_response["items"]
                goals = pd.DataFrame(goal_response)
                goals = goals[goals.active == True]
                goals = goals.reset_index()

                return goals

            def scrape_ga_attribution_data(
                    request_url,
                    request_headers,
                    form_data,
                    backdate,
                    account_id,
                    property_id,
                    view_id,
                    credentials):


                # From configuration backdate or not. If not then get yesterday.
                if backdate:

                    ga_management_data = get_ga_goals(
                        account_id=account_id,
                        property_id=property_id,
                        view_id=view_id,
                        credentials=credentials
                    )

                    start_date = self.configuration['ga_attribution_scrape']['backdate']['start_date']
                    end_date = self.configuration['ga_attribution_scrape']['backdate']['end_date']
                    date_range = []
                    for date in pd.date_range(start=start_date, end=end_date):
                        date_range.append(date.strftime('%Y%m%d'))
                else:

                    ga_management_data = get_ga_goals(
                        account_id=account_id,
                        property_id=property_id,
                        view_id=view_id
                    )

                    yesterday = d.today() - timedelta(days=1)
                    date_range = [str(yesterday.strftime('%Y%m%d'))]

                    # Loop through each day for each goal for DDA
                ga_attribution_data = pd.DataFrame()

                for date in tqdm(date_range, desc="Date", total=len(date_range)):
                    for row in tqdm(ga_management_data.id, desc="Goal ID", total=len(ga_management_data.id)):

                        # Filter goals to row goal - we'll use this to manipulate response and final data output
                        conversion = ga_management_data[ga_management_data.id == row]

                        # Add dates into form data for response
                        form_data['_u.date00'] = date
                        form_data['_u.date01'] = date

                        # Add conversion ID into response
                        conversion_id = conversion.id.to_list()[0]
                        form_data['_.bfType'] = conversion_id

                        # Get raw response data for GA
                        raw_response = requests.post(request_url, data=form_data, headers=request_headers).text
                        # print(raw_response)
                        # Check for http error in response
                        while 'The service is temporarily unavailable. Please try again in a few minutes.' in raw_response:
                            print(
                                "http error: The service is temporarily unavailable. Please try again in a few minutes.")
                            print("Sleeping for a couple of mins then retry")
                            time.sleep(120)
                            raw_response = requests.post(request_url, data=form_data, headers=request_headers).text

                        # print(raw_response)
                        time.sleep(1.5)

                        # Clean response
                        # Cleaning the actual response by removing the unnecessary lines and adding in other variables
                        response = pd.read_csv(io.StringIO(raw_response), quotechar='"', skipinitialspace=True,
                                               error_bad_lines=False,
                                               skiprows=5)[:-3]

                        # Renaming the columns
                        new_column_names = []
                        for item in response.columns:
                            x = item.replace(" ", "_")
                            x = x.replace("-", "_")
                            if x[0].isdigit():
                                x = "_" + x
                            new_column_names.append(x.lower())
                        response.columns = new_column_names
                        response = response[response.columns.drop(list(response.filter(regex='%_change_')))]

                        # Change the types to float and removing all special characters
                        for item in response.columns:
                            if 'spend' in item or 'data_driven' in item:
                                response[item] = response[item].replace({'£|€|$|>|<|,|\\%': ''}, regex=True)
                                response[item] = response[item].astype(float)

                        # Make data into pandas dataframe
                        clean_data = pd.DataFrame(response, columns=response.columns)

                        # Add in the conversion name and id of goals
                        clean_data['conversion_name'] = conversion.name.to_list() * len(clean_data.index)
                        clean_data['conversion_id'] = conversion.id.to_list() * len(clean_data.index)

                        # Add date into data
                        clean_data["date"] = datetime.strptime(date, '%Y%m%d')

                        ga_attribution_data = pd.concat([ga_attribution_data, clean_data])
                        # print(ga_attribution_data)

                        if self.limit_rows is not None:
                            break

                return ga_attribution_data

            return scrape_ga_attribution_data(
                request_url=self.configuration['ga_attribution_scrape']['request']['url'],
                request_headers=self.configuration['ga_attribution_scrape']['request']['headers'],
                form_data=self.configuration['ga_attribution_scrape']['request']['form_data'],
                backdate=self.configuration['ga_attribution_scrape']['backdate']['backdate'],
                account_id=self.configuration['ga_attribution_scrape']['ga']['account_id'],
                property_id=self.configuration['ga_attribution_scrape']['ga']['property_id'],
                view_id=self.configuration['ga_attribution_scrape']['ga']['view_id'],
                credentials=self.configuration['ga_attribution_scrape']['ga']['service_account_path']
            )

        def show_config(self):
            return self.configuration

        def to_bq(self, cloud_function=False, location=None):

            def bq_auth(credentials):
                return service_account.Credentials.from_service_account_file(credentials)

            def days_between(d1, d2):
                d1 = datetime.strptime(d1, "%Y-%m-%d")
                d2 = datetime.strptime(d2, "%Y-%m-%d")
                return abs((d2 - d1).days)

            # define vars from self
            df = self._constructor
            creds = self.configuration['ga_attribution_scrape']['bigquery']['service_account_path']
            backdate = self.configuration['ga_attribution_scrape']['backdate']['backdate']
            project_id = self.configuration['ga_attribution_scrape']['bigquery']['project_id']
            dataset_id = self.configuration['ga_attribution_scrape']['bigquery']['dataset_id']
            table_id = self.configuration['ga_attribution_scrape']['bigquery']['table_id']

            if not cloud_function or backdate:
                # Create bq authentication
                bq_authing = bq_auth(credentials=creds)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds

            # Additional bq related vars
            table_location = dataset_id + '.' + table_id

            # Check if table already exists
            bq_client = bigquery.Client()  # Create BQ Client

            try:
                # Check to see if a table exists
                bq_client.get_table(table_location)

                # If it does then run a query to check that dates are not overlapping in backdate
                start_date = self.configuration['ga_attribution_scrape']['backdate']['start_date']
                end_date = self.configuration['ga_attribution_scrape']['backdate']['end_date']

                config_date_range = []
                for date in pd.date_range(start=start_date, end=end_date):
                    config_date_range.append(date.strftime('%Y-%m-%d'))
                config_start_date = config_date_range[0]
                config_end_date = config_date_range[-1]
                #print(config_date_range)

                sql = "SELECT FORMAT_DATETIME('%Y-%m-%d', CAST(date AS DATETIME)) as date FROM `" \
                      + project_id + '.' + table_location + "` GROUP BY date ORDER BY date"
                query_job = bq_client.query(sql)
                dates_df = query_job.result().to_dataframe()
                bq_date_range = dates_df['date'].to_list()
                bq_start_date = bq_date_range[0]
                bq_end_date = bq_date_range[-1]
                #print(bq_date_range)

                if (days_between(bq_start_date, config_end_date) != 1 or
                        days_between(bq_end_date, config_start_date) != 1):
                    dates = []
                    for date in bq_date_range + config_date_range:
                        dates.append(datetime.strptime(date, '%Y-%m-%d'))
                    config_date_range = pd.date_range(min(dates), max(dates))
                    config_date_range = config_date_range.strftime('%Y-%m-%d').to_list()

                intersection_of_dates = [date for date in config_date_range if date in bq_date_range]
                if intersection_of_dates:  # Check if intersection is empty
                    print("Config dates overlap with dates in bigquery. Fixing...")
                    for overlappingDates in intersection_of_dates:
                        if overlappingDates in config_date_range:
                            config_date_range.remove(overlappingDates)
                    if config_date_range:
                        print(
                            "New dates configuration. Start date: " + config_start_date +
                            " and end date: " + config_end_date
                        )
                    else:
                        print("Config dates are already present in bigquery dataset.")
                        sys.exit()
            except:  # If table doesnt exist don't do anything
                pass

            # Set relevant to_gbq vars
            if_exists = 'append'
            if location is None:
                location = 'US'

            if not cloud_function or backdate:
                df.to_gbq(
                    dataset_id + '.' + table_id,
                    project_id,
                    chunksize=None,
                    if_exists=if_exists,
                    location=location,
                    credentials=bq_authing
                )
            else:
                df.to_gbq(
                    dataset_id + '.' + table_id,
                    project_id,
                    chunksize=None,
                    if_exists=if_exists,
                    location=location
                )

    # def ecommerce(self):
    #    request_url = self.configuration['ga_attribution_scrape']['request']['url']
    #    request_headers = self.configuration['ga_attribution_scrape']['request']['headers']
    #    form_data = self.configuration['ga_attribution_scrape']['request']['form_data']
