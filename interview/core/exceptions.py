class TMTBadRequestParamError(Exception):
    """
    Error indicating a bad request from the client.

    Indicates the client sent a request parameter that is invalid and which the
    server is unable to process. For example, if the client sends an unrecognized
    query_param value this error could be raised.

    This should not be used for validation of user-provided input - use ValidationError
    for that.

    The server should handle this error by sending a "something went wrong" type
    of message to the client and log necessary debug info.
    """
