from lgt_jobs.lgt_data.mongo_repository import SubscriptionsRepository


def get_linkedin_search_contact(name: str):
    return f"https://www.linkedin.com/search/results/all/?keywords={name}&origin=GLOBAL_SEARCH_HEADER&sid=u%40F"


def get_help_text(user):
    subscription = SubscriptionsRepository().find_one(id=user.subscription_id)
    return 'the onboarding call with us!' if subscription.trial else 'a call with us.'
