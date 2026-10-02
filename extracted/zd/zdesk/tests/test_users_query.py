import time

from zdesk import get_id_from_url

from zdesk_common import islocation, isstatuscode

def test_users_query(zd):
    result = zd.users_search(query=f'email:{zd._zdesk_email} -role:end-user')
    assert isstatuscode(result), \
        'placeholder'

    #response_raw = zd.users_search(ticket_id,
    #                              raw_query='?include=comment_count',
    #                              retval ='content')

    #assert 'comment_count' in response_query['ticket'], \
    #    'query failed to include comment_count'
    
    #assert 'comment_count' in response_raw['ticket'], \
    #    'raw_query failed to include comment_count'
    
    # Delete
    #result = zd.ticket_delete(ticket_id, retval='code')

    #assert isstatuscode(result), \
    #    'Delete ticket raw_query_test response is not a status code string'

