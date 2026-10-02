import csv

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

DOMAINS = set()


def _load_from_csv():
    """
    Load free email domains from a CSV file into the FREE_EMAIL_DOMAINS set.
    This function is intended for internal use only.

    Parameters:
    path_to_csv (str): The path to the CSV file containing the domains.
    """

    global DOMAINS
    resource = files("freemailchecker.data").joinpath("freemaildomains.csv")
    with resource.open("r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            domain = row[0].strip().lower()
            if domain:
                DOMAINS.add(domain)


def is_free_email(email):
    """
    Check if the domain

    Parameters:
    email (str): The email address to check.

    Returns:
    bool: True if the email's domain is a free email domain, False otherwise.
    """
    domain = email.split("@")[-1].lower()  # Extract the domain part of the email
    return is_free_domain(domain)


def is_free_domain(domain):
    """
    Check if the domain is in our free email domain list

    Parameters:
    domain (str): The domain to check

    Returns:
    bool: True if the domain is in our free email domain list, False
    otherwise.
    """

    return domain.strip() in DOMAINS


_load_from_csv()
