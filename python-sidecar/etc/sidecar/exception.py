class InvalidJSON(Exception):
    code = 400
    pass

class NotJSONHeader(Exception):
    code = "400"
    title = "Bad Request"
    message = "Invalid Content Type in Header"
    pass

class BadData(Exception):
    code = 400
    title = "Bad Data"
    pass

class NotFound(Exception):
    code = 404
    title = "Not Found"
    pass

class Conflict(Exception):
    code = 409
    title = "Conflict"
    pass
