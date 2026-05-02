import inspect
import httplib
import json
import logging
import os
import sys
from _ssl import SSLError
from json import loads
from urllib2 import Request, urlopen, HTTPError, URLError
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def safeget(dct, *keys):
    ret = None
    if dct:
        for key in keys:
            try:
                ret = dct[key]
            except KeyError:
                pass
    return ret


def safe_get_json(json_string, key, log=logging.getLogger('spotinst-agent')):
    try:
        ret = json.loads(json_string)[key]
    except Exception as e:
        log.error("exception {}".format(e.__str__()))
        return None
    return ret


def safe_read_simple_url(url, log=logging.getLogger('spotinst-agent'), headers={}):
    try:
        log.debug("reading simple {} ...".format(url))
        req = Request(url, headers=headers)
        req.add_header('Content-Type', 'application/json')
        response = urlopen(req, timeout=10)
        return response.read()
    except HTTPError as e:
        log.error("The server can't fulfill the GET {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for GET request. [reason: {}]".format(e.reason))
    except Exception as e:
        log.error("There was an error of GET url {}: {}".format(url, e.__str__()))
    finally:
        try:
            response.close()
        except NameError:
            pass


def safe_put_simple_url(url, log=logging.getLogger('spotinst-agent'), headers={}):
    ret_val = None

    try:
        log.debug("reading simple {} ...".format(url))
        req = Request(url, headers=headers)
        req.get_method = lambda: 'PUT'
        response = urlopen(req, timeout=10)

        if response.code == 200:
            ret_val = response.read()
    except HTTPError as e:
        log.error("The server can't fulfill the PUT {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for PUT {} request. [reason: {}]".format(url, e.reason))
    except Exception as e:
        log.error("There was an error of PUT url {}: {}".format(url, e.__str__()))
    finally:
        try:
            response.close()
        except NameError:
            pass

    return ret_val


def get_gcp_metadata(url, path_params, log=logging.getLogger('spotinst-agent')):
    try:
        url = url + path_params
        log.debug("reading simple {} ...".format(url))
        req = Request(url)
        #req.add_header('Content-Type', 'application/json')
        req.add_header('Metadata-Flavor','Google')
        response = urlopen(req, timeout=10)
        return response.read()
    except HTTPError as e:
        log.error("The server can't fulfill the GET {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for GET request. [reason: {}]".format(e.reason))
    except Exception as e:
        log.error("There was an error of GET url {}: {}".format(url, e.__str__()))
    finally:
        try:
            response.close()
        except NameError:
            pass

# getting vmId - not whole the metadata
def get_azure_metadata(url, log=logging.getLogger('spotinst-agent')):
    try:
        log.debug("reading simple {} ...".format(url))
        req = Request(url)
        req.add_header('Metadata', 'true')
        response = urlopen(req, timeout=10)
        return response.read()
    except HTTPError as e:
        log.error("The server can't fulfill the GET {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for GET request. [reason: {}]".format(e.reason))
    except Exception as e:
        log.error("There was an error of GET url {}: {}".format(url, e.__str__()))
    finally:
        try:
            response.close()
        except NameError:
            pass


def safe_get_simple_url(url, log=logging.getLogger('spotinst-agent')):
    try:
        log.debug("reading simple {} ...".format(url))
        req = Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urlopen(req, timeout=5)
        res = response.read()
        body = loads(res.decode('utf-8'))
        return body
    except HTTPError as e:
        log.error("The server can't fulfill the GET {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for GET request. [reason: {}]".format(e.reason))
    except Exception as e:
        log.error("There was an error of GET url {}: {}".format(url, e.__str__()))
    finally:
        try:
            response.close()
        except NameError:
            pass

def safe_get_url(url, token=None, log=logging.getLogger('spotinst-agent')):
    try:
        log.debug("getting {} ...".format(url))
        req = Request(url)
        req.add_header('Content-Type', 'application/json')
        if token:  # add token
            req.add_header('Authorization', 'Bearer ' + token)

        response = urlopen(req, timeout=10)
        res = response.read()
        body = loads(res.decode('utf-8'))
        return body
    except HTTPError as e:
        log.error("The server can't fulfill the GET {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for GET request. [reason: {}]".format(e.reason))
    except SSLError as e:
        log.error("Connection to API timed out, retry in next iteration : {}".format(str(e)))
    except Exception as e:
        log.error("There was an error of GET url {}: {}".format(url, e.__str__()))
    finally:
        try:
            response.close()
        except NameError:
            pass


def safe_post_url(url, message, token=None, log=logging.getLogger('spotinst-agent')):
    try:
        log.info("posting {} ...".format(url))
        log.info("token is " + token)
        data = message.encode('utf-8')
        req = Request(url)
        req.add_header('Content-Type', 'application/json')
        if token:  # add token
            req.add_header('Authorization', 'Bearer ' + token)

        response = urlopen(req, data, timeout=10)
        res = response.read()
        body = loads(res.decode('utf-8'))
        return body
    except HTTPError as e:
        log.error("The server can't fulfill the POST {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for POST request. [reason: {}]".format(e.reason))
    except SSLError as e:
        log.error("Connection to API timed out, retry in next iteration : {}".format(str(e)))
    except httplib.BadStatusLine as e:
        log.error("Bad status line. The URL is most likely wrong.")
    except Exception as e:
        log.error("There was an error of POST url. Exceptions: " + str(sys.exc_info()[0]))
    finally:
        try:
            response.close()
        except NameError:
            pass


def safe_put_url(url, message, token, log=logging.getLogger('spotinst-agent')):
    try:
        log.debug("putting %s ..." % url)
        data = message.encode('utf-8')
        req = Request(url)
        req.add_header('Content-Type', 'application/json')
        if token:  # add token
            req.add_header('Authorization', 'Bearer ' + token)
        req.get_method = lambda: 'PUT'

        response = urlopen(req, data, timeout=5)
        res = response.read()
        body = loads(res.decode('utf-8'))
        return body
    except HTTPError as e:
        log.error("The server can't fulfill the PUT {} request. [reason: {}]".format(url, e.reason))
    except URLError as e:
        log.error("Unable to reach the server for PUT request. [reason: {}]".format(e.reason))
    except SSLError as e:
        log.error("Connection to API timed out, retry in next iteration : {}".format(str(e)))
    except Exception as e:
        log.error("There was an error of PUT url {}: {}".format(url, e.__str__()))
    finally:
        try:
            response.close()
        except NameError:
            pass


def parse_yml(yml, log=logging.getLogger('spotinst-agent')):
    # Initialize Config
    with open(yml) as f:
        try:
            return yaml.load(f)
        except Exception as e:
            log.error("Can't parse yml file {}. Exception {}".format(yml, e))
            raise e


def load_class_from_name(fqcn):
    # Break apart fqcn to get module and classname
    paths = fqcn.split('.')
    modulename = '.'.join(paths[:-1])
    classname = paths[-1]
    # Import the module
    mod = __import__(modulename, globals(), locals(), ['*'])
    # Get the class
    cls = getattr(sys.modules[modulename], classname)
    # Check cls
    if not inspect.isclass(cls):
        raise TypeError("%s is not a class" % (fqcn))
    # Return class
    return cls


def retrieve_creds():
    # Retrieve auth token
    vars = dict()

    try:
        with open('/root/.spotinst/credentials', "r") as creds:
            for line in creds:
                eq_index = line.find('=')
                var_name = line[:eq_index].strip()
                string_value = line[eq_index + 1:].strip()
                vars[var_name] = string_value

    except IOError:
        print ("Please set a credentials file at /root/.spotinst/credentials")

    return vars
