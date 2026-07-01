import json
import time
from datetime import datetime

import pandas as pd
import requests

from lexisnexisapi import credentials as cred

__version__ = "3.0.3.3"
__author__ = (
    "Robert Cuffney & Ozgur Aycan, "
    "CS Integration Consultants @ LexisNexis"
)


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred in function: '{func.__name__}'")
            print(
                f"error: {e}",
            )
            print(f"args:{args}")
            print(f"kwargs:{kwargs}")
            raise  # Re-raise the exception to propagate it further

    return wrapper


# Constants are usually defined on a module level
# and written in all capital letters
# with underscores separating words.
# Examples include MAX_OVERFLOW and TOTAL.

METABASE_SEARCH_URL = "http://metabase.moreover.com/api/v10/searchArticles?"
METABASE_RATE_CHECK_URL = "https://metabase.moreover.com/api/v10/rateLimits?key="

# Function names should be lowercase,
# with words separated by underscores
# as necessary to improve readability.

# Class names should normally
# use the CapWords convention.
# CapitalizedWords


class Search:
    """
    mbSearch class
    returns API response as a python class
    accepts either a string query,
    or a dictionary of all metabase parameters

    full_dataset = True --
    activates the option to create a full dataset of total results
    """

    @error_handler
    def __init__(self, full_dataset=False, **kwargs):
        self.parameters = self.set_parameters(kwargs)
        if full_dataset:
            data = self.get_fulldataset()
            print(data["totalResults"])
        else:
            data = http_request(self.parameters)
        if isinstance(data, dict):
            self.__dict__.update(data)
        else:
            print("Something went wrong, No data was returned")

    def set_parameters(self, p):
        p.setdefault("key", cred.get_Key("Metabase_Search_Key"))
        p.setdefault("limit", "10000")
        p["format"] = "json"
        return p

    @error_handler
    def articles_dataframe(self, *args):
        """
        returns a data frame of the articles
        optional parameter fields, is a list of desired fields to return
        """
        df = pd.DataFrame.from_records(self.articles)
        # Filter dataframe, if *args are provided
        if args:
            series = list(args)
            df = df[series]
        return df

    @error_handler
    def create_file(self, file="articles.json"):
        """
        creates a json file
        """
        if self.totalResults != 0:
            with open(file, "w") as my_file:
                my_file.write(json.dumps(self.articles, indent=4))
                print(
                    f"{len(self.articles)} article(s) successfully written to a file:{file}"
                )
        else:
            print("no articles to write to file!")

    '''
    Below Functions, within this class, used only for FullDataSet
    '''
    @error_handler
    def get_fulldataset(self):
        self.parameters.pop("sequence_id", "")  # get rid of 'sequence_id' if it's there
        # self.parameters['limit']='1000'                       #This will set the limit to the maximum allowed per their key
        t_lst = []  # this will be the list of all articles
        x = 1  # this will represent the number of articles left

        i = 1  # i counts the number of loops occurring
        mc = Streamline(self.parameters["key"])
        while x > 0:  # run while x (number of articles remaining)
            # self.set_calls()                               #use set_calls object to determine calls left in minute
            mc.track_calls()
            myData = http_request(self.parameters)  # call API
            t_lst = t_lst + myData["articles"]  # add articles to t_lst
            s_id = myData["articles"][-1][
                "sequenceId"
            ]  # find the last sequence id available
            self.parameters[
                "sequence_id"
            ] = s_id  # set sequence within parameters for next API call
            t = myData["totalResults"]
            print(
                f"\rRemaining Results: {t} / sequence_id: {s_id} / number: {i}",
                end="              ",
            )  # print progress
            x = int(myData["totalResults"]) - len(
                myData["articles"]
            )  # update number of articles left to pull
            i += 1
        # End of 'while' loop
        print("all done")  # print to notify user of completion
        # total = len(t_lst)                               #total of all articles pulled, should equal original 'totalResults'
        myData[
            "articles"
        ] = t_lst  # set the total list of articles as the value in the key 'articles'
        myData["totalResults"] = len(
            t_lst
        )  # make sure the 'totalResults' key is set to the original 'totalResults'
        return myData


class Streamline:
    """
    This is a class object to maximize metabase search calls without going over the
    calls per minute limit.  Class is used as a counter
    Upon instantiation the rate limit API is called.
    The Streamline object will reset it's calls_remaining to the minute_limit at the beginning of every new minute.
    """

    def __init__(self, key):
        self.key = key
        self.start_minute = self.get_current_minute()
        lst = rate_check(self.key)
        for rate in lst:
            if rate.get("unit") == "MINUTE":
                self.minute_limit = int(rate.get("limit", 0))
        self.calls_remaining = self.minute_limit

    @error_handler
    def track_calls(self):
        current_minute = self.get_current_minute()
        same_minute = self.start_minute == current_minute
        if same_minute:
            self.calls_remaining -= 1
        else:
            self.calls_remaining = self.minute_limit - 1
            self.startMin = self.get_current_minute()
        if self.calls_remaining < 1:
            self.wait_for_new_min()
        return self.calls_remaining

    def restart(self):
        print()

    def wait_for_new_min(self):
        current_minute = self.get_current_minute()
        print(f"Waiting for a new Minute . . . current minute:{current_minute}")
        while self.start_minute == current_minute:
            time.sleep(1)
            current_minute = self.get_current_minute()
        self.start_minute = current_minute
        self.calls_remaining = self.minute_limit - 1

    def get_current_minute(self):
        return datetime.now().minute


def http_request(p):
    url = METABASE_SEARCH_URL
    r = requests.get(url, params=p)
    data = r.__dict__.copy()
    data.pop("_content", None)
    data.update(r.json())
    if r.status_code != 200:
        print(r.text)
        print("An error occurred while attempting to retrieve data from the API.")
    return data


@error_handler
def rate_check(key):
    """
    Calls the Metabase rate limit API and 
    returns the results as a list of dictionaries
    """
    if not key:
        key = cred.get_Key("Metabase_Search_Key")
    rateCheckUrl = METABASE_RATE_CHECK_URL + key
    r = requests.get(rateCheckUrl)
    if r.status_code == 200:
        data = r.json()
    return data["rateLimits"]


def set_metabase_search_key(v):
    cred.set_Key(Metabase_Search_Key=v)


def get_time():
    """
    returns the current minute
    """
    return datetime.now().minute


class Article:
    """
    An instance of this class is created using 1 article
    this class is not for the aggregate http response.
    A sample call:
    myArticleInstance =article = article(myArticle)
    """
    def __init__(self, myArticle):
        """
        Takes each key from the article dictionary and
        sets it as an attribute of the class
        """
        self.__dict__.update(myArticle)


@error_handler
def indexTerms(obj, *args):
    """
    returns a dataframe of index terms
    accepts either an instance of Search, or an instance of Article.
    if Search is sent, df return is an aggregate count of the terms
    if Article is sent, df return is a dataframe of all index terms
    """
    if isinstance(obj, Search):
        if obj.articles:
            df = pd.concat(
                [
                    pd.DataFrame.from_dict(article["indexTerms"], orient="columns")
                    for article in obj.articles
                ]
            )
            df["count"] = df.groupby(["name"])["domains"].transform("count")
            df = df.drop(columns=["score", "code"])
            df = df.dropna()
            df = df.drop_duplicates(["name"])
            df = df.sort_values("count", ascending=False)
        else:
            print("no indexTerms to show!")
    if isinstance(obj, Article):
        indexterms_lst = obj.indexTerms
        for x in indexterms_lst:
            if x.get("domains") is None:
                x.remove(x)
        df = pd.DataFrame.from_records(indexterms_lst)

    # Filter dataframe, if *args are provided
    if args:
        lst = [x.upper() for x in args]
        df["INCLUDE"] = df["domains"].apply(
            lambda v: len(list(set(v).intersection(lst))) != 0
        )
        df = df[df["INCLUDE"]].reset_index(drop=True)
        del df["INCLUDE"]
        df
    return df
