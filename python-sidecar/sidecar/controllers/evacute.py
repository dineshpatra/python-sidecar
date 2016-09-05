#-*- coding: utf-8 -*-
# ______________________________________________________________________
# | evacute controller file                                            |
# |                                                                    |
# | This file is responsible for handling the evacute related stuff    |
# |____________________________________________________________________|
# | Copyright: 2016@nephoscale.com<info@nephoscale.com>                |
# |                                                                    |
# | Start date: 22nd Aug 2016                                          |
# |____________________________________________________________________|

from pecan import expose, redirect
from pecan.secure import secure
from oslo_config import cfg
import pecan, json
from sidecar import rbac
from sidecar.model import user as user_model
from sidecar.keystoneauth import authenticate

class Evacute(object):
    """
    # | Evacute class
    """
    
    def __init__(self):
        """
        # | Evacute initialization
        # |
        # | Arguments: None
        # |
        # | Returns None
        """

    @secure(authenticate)
    @expose(generic=True, template='json')
    def index(self):
        """
        # | Evacute index function
        # |
        # | Arguments: None
        # |
        # | Returns: None
        """
        return {
            "test": "test"
        }
