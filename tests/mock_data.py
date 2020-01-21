missing_header_message = 'invalid_header: Authorization header missing'

bearer_missing_message = '''\
invalid_header: "Bearer" missing from Authorization header'''

token_missing_message = '''\
invalid_header: Token missing from Authorization header'''

invalid_auth_header_message = '''\
invalid_header: Authorization header must be "bearer token"'''

token_expired_message = 'token_expired: Token expired'

invalid_signature_token_message = '''\
invalid_token: Unable to verify token header'''

forbidden_error_message = 'forbidden: Permission not found'

unprocessable_error_message = 'unable to process request'

not_found_error_message = 'resource not found'

bad_request_error_message = 'bad request'

not_allowed_error_message = 'method not allowed'

undecodable_token_message = 'invalid_token: Unable to decode token'

casting_asst_token = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9UTTRSR\
    FpCT1VReVEwVTJSRU5GTmpGR056QkJOalF3TmtGQ1FqUkdNVGd6TTBZNU1FUXpSZyJ9.eyJpc3\
    MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LmF1dGgwLmNvbS8iLCJzdWIiOiJRU25WN2RkNmlKTW\
    g1aGg0dHQ1UjI1QmdrTFg0S1NMOUBjbGllbnRzIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTc5NT\
    kxMjE3LCJleHAiOjE1Nzk2Nzc2MTcsImF6cCI6IlFTblY3ZGQ2aUpNaDVoaDR0dDVSMjVCZ2tMWDRLU0\
    w5Iiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhb\
    HMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.f0T8KpFGUQZyqs1jcgk\
    V_y3lqRSY9m4KHoUhy737CY2896ORnSNL8LP_dtKX9610wH_bw47gV899vB4aLkJbVqF2kCS3ivYzfJ6\
    _ferXjYYl7wYRIwE-__2xX8jGqlqLdLV4V5YZDeYtTojGXs73WWlJSlGXAk5VOl807TtC_1QUBC2nig\
    DWzSvB7-paK0eb-ltQ8AqVKNwkjIrhYtlioRM-rKywRW3A3FDN7wfJepqVYIipn7NnZ0qTezDEJMaY0y\
    DxwDlOsjlSY0Q66MLQWu1WOVwJYYHW9ejGfSrKOVqRTfPz2zGtNpslTeeToxAd9mU-0BUbqaETSzY9z7NvzA'''

bad_request_error_response = {
                                'success': False,
                                'error': 400,
                                'message': bad_request_error_message
                            }

header_missing_response = {
                                'success': False,
                                'error': 401,
                                'message': missing_header_message
                            }

bearer_missing_response = {
                                'success': False,
                                'error': 401,
                                'message': bearer_missing_message
                            }

token_missing_response = {
                                'success': False,
                                'error': 401,
                                'message': token_missing_message
                            }

token_expired_response = {
                                'success': False,
                                'error': 401,
                                'message': token_expired_message
                            }

invalid_auth_header_response = {
                                'success': False,
                                'error': 401,
                                'message': invalid_auth_header_message
                            }

invalid_signature_response = {
                                'success': False,
                                'error': 401,
                                'message': invalid_signature_token_message
                            }

undecodable_token_response = {
                                'success': False,
                                'error': 401,
                                'message': undecodable_token_message
                            }

forbidden_error_response = {
                                'success': False,
                                'error': 403,
                                'message': forbidden_error_message
                            }

not_found_error_response = {
                                'success': False,
                                'error': 404,
                                'message': not_found_error_message
                            }

not_allowed_error_response = {
                                'success': False,
                                'error': 405,
                                'message': not_allowed_error_message
                            }

unprocessable_error_response = {
                                'success': False,
                                'error': 422,
                                'message': unprocessable_error_message
                            }

actor = {
            'id': '',
            'name': '',
            'age': '',
            'gender': '',
        }

movie = {
            'id': '',
            'title': '',
            'release_date': '',
        }
