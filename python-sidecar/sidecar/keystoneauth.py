#-*- coding: utf-8 -*-
# ______________________________________________________________________
# | keystone authentication file                                       |
# |                                                                    |
# | This file is responsible for handling the keystone authenticateion |
# |____________________________________________________________________|
# | Copyright: 2016@nephoscale.com<info@nephoscale.com>                |
# |                                                                    |
# | Start date: 22nd Aug 2016                                          |
# |____________________________________________________________________|

from pecan import expose, redirect
import pecan
from sidecar import exception
from oslo_config import cfg
import ConfigParser, urllib2, urllib, json
Config = ConfigParser.ConfigParser()
Config.read(cfg.CONF.config_file[0])

def _KesytoneAdminAuthenticatev2():
    """
    # | Function to get the auth token for admin
    # |
    # | Arguments: None
    # |
    # | Returns admin auth token
    """ 
    auth_url = Config.get('keystone_auth', 'auth_url')
    username = Config.get('keystone_auth', 'username')
    password = Config.get('keystone_auth', 'password')
    data = {
        "auth": {
            "passwordCredentials": {
                "username": username,
                "password": password
            }    
        }
    }
    data = json.dumps(data)
    url = auth_url + 'tokens'
    req = urllib2.Request(url, data)
    req.add_header("Content-Type", "application/json")
    r = urllib2.urlopen(req)
    result = r.read()
    body = json.loads(result)
    return body['access']['token']['id']
    
def authenticate():
    auth_token = pecan.request.headers.get('X-Auth-Token')
    if not auth_token:
        # | If auth token is not defined, then
        # | return false.
        return False
    
    auth_version = Config.get('keystone_auth', 'auth_version')
    
    if auth_version == '2':
        # | If keystone version is 2.0
        # | Then need to authenticate for 
        # | endpoints
        try:
            url = 'http://controller:35357/v2.0/tokens/' + auth_token + '/endpoints'
            admin_authtoken = _KesytoneAdminAuthenticatev2()
            request = urllib2.Request(url)
            request.add_header("Content-Type", "application/json")
            request.add_header("X-Auth-Token", admin_authtoken)
            response = urllib2.urlopen(request)
            response = response.read()
            print response
        except Exception as e:
            print str(e)
            return False

        print response.info()

    #pecan.response.status = 403
    #pecan.response.text = 'Hellooo'
    
    return False;
