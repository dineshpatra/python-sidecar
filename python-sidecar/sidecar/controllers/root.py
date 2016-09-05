# coding=utf-8
from pecan import expose, redirect
from oslo_config import cfg
import pecan, json
from sidecar import rbac
from sidecar.model import user as user_model
import event

class V2Controller(object):
    """
    # | Version 2 controller.
    """
    events = event.EventController()

    def __init__(self):
        """
        # | Initialization function
        # | 
        # | Arguments: None
        # |
        # | Returns None
        """

    @expose(generic=True, template='json')
    def index(self):
        """
        # | Index function for the version 2
        # |
        # | @Arguments: Void
        # |
        # | @Returns: Dictionary containg the version info
        """
        return  {"v2": {"date":"2016-08-07T00:00:00", "status":"current"}}

class RootController(object):
    """
    | # Root Controller Class
    """
    v2 = V2Controller()

    def __init__(self):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """
    
    @expose(generic=True, template='json')
    def index(self):
        """
        # | Index function of the rest api
        # |
        # | Arguments: None
        # |
        # | Returns JSON
        """
        return {"versions": [self.v2.index()]}

