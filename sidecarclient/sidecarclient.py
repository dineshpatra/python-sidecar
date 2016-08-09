#!/usr/bin/env python
"""
Name: Sidecarclient.py
Desc:  Sidecar CLI Utility
Created By: Binoy M V
Created On:  7-July-2016
"""

#importing the packages
import argparse
import os
import sys
from prettytable import PrettyTable
import requests
import json
import logging
import re
import ConfigParser

#Services
service_args = [
    'create-data',
    'update-data',
    'delete-data',
    'list-data',
]

#Getting the configuration details
# To determine Keystone API version
Config = ConfigParser.ConfigParser()
Config.read("./configure.cfg")
auth_url = Config.get("CREDENTIALS", "auth_url")
pecan_url = Config.get("CREDENTIALS", "pecan_url")

class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required,
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

class SidecarDataError(Exception):
    """Default exception raised for policy enforcement failure."""

    def __init__(self, data):
        msg = (('%(data)s in command is not valid') %
               {'data': data})
        super(SidecarDataError, self).__init__(msg)

class Env():

    def __init__(self):
        headers = {'Content-Type': 'application/json'}
        data = Config.get("CREDENTIALS", "cred")
        response = requests.post(auth_url, data = data, headers = headers)

        #checking the version and loading the api accordingly
        if "v3" in auth_url:
            self.token = response.headers['X-Subject-Token']
        else:
            token_data  = json.loads(response.text)
            self.token = token_data['access']['token']['id']
            self.url = pecan_url

    def list_data(self, args):
        """
        To retrieve details as list.
        Args: args. NA
        Returns:
            Returns response to the CLI
        Raises: Exception
        """
        #Defining the table header values
        logging.info('Defining the table header values')
        x = PrettyTable(['Name', 'Full Name', 'Id'])
        x.align = 'l'
        
        #Setting the url and calling the API
        logging.info('Setting the url and calling the API')
        header = {'X-Auth-Token': self.token, 'Content-Type': 'application/json'}
        response = requests.get(self.url, headers = header)
        user_data = json.loads(response.text)
         
        #Getting the response and passing to pretty table
        logging.info('Getting the response and passing to pretty table')
        for response_text in user_data['user']:
            x.add_row([response_text['name'], response_text['fullname'], response_text['id']])
        print x
    
    def create_data(self, args):
        """
        To create role.
        Args: args 
        Returns:
            Returns response to the CLI
        Raises: Exception
        """
        
        logging.info('Checking the parameters to create data')
        if 'name' not in args.keys():
            raise SidecarDataError(args)

        #Defining the table header values
        del args['subparser_name']
        header = {'X-Auth-Token': self.token, 'Content-Type': 'application/json'}
        response = requests.post(self.url, params=args, headers=header)

    def update_data(self, **args):
        """
        To create role.
        Args: args 
        Returns:
            Returns response to the CLI
        Raises: Exception
        """
        
        logging.info('Checking the parameters to update data')
        if 'id' not in args.keys():
            raise SidecarDataError(args)

        del args['subparser_name']
 
        #Defining the table header values
        header = {'X-Auth-Token': self.token, 'Content-Type': 'application/json'}
        response = requests.put(self.url, params=args, headers=header)
   
    def delete_data(self, args):
        """
        To create role.
        Args: args 
        Returns:
            Returns response to the CLI
        Raises: Exception
        """

        logging.info('Checking the parameters to delete data')
        if 'id' not in args.keys():
            raise SidecarDataError(args)

        #Defining the table header values
        data = {"id": args['id']}
        header = {'X-Auth-Token': self.token, 'Content-Type': 'application/json'}
        response = requests.delete(self.url, params=data, headers=header)
        
    def list_role(args):
        """
        To list role.
        Args: args 
        Returns:
            Returns response to the CLI
        Raises: Exception
        """
        
        #Defining the table header values
        logging.info('Defining the table header values')
        x = PrettyTable(['Name', 'Id'])
        x.align = 'l'
        response = requests.get(self.url, auth=('user', 'pass'), headers = header_value)
        
        #Getting the response and passing to pretty table
        logging.info('Getting the response and passing to pretty table')
        for response_text in json.loads(response.text):
            x.add_row([response_text['name'],response_text['id']])
        print x

def normalize(args):
    datum = {}
    for arg, val in args.__dict__.iteritems():
        # skip service arguments
        if arg.startswith('os_') or arg in service_args:
            continue
        # set parameter and normalize its value
        datum[arg] = re.sub(r'\s+', ' ', val.strip()) if hasattr(val, 'strip') else val
    return datum


#Checking the name and adding the arg parse    
if __name__ == '__main__':

    #Making the argument parse
    ap = argparse.ArgumentParser(description='Pecan client tool')
    subparsers = ap.add_subparsers(help='sub-command help', dest='subparser_name')
    
    #Listing data command
    sp = subparsers.add_parser('list-data', help='List Data')

    #Create role command
    sp = subparsers.add_parser('create-data',  help = "Create user data")
    sp.add_argument('--name', help='Name to update')
    sp.add_argument('--fullname', help='Fullname to update')

    #update data
    sp = subparsers.add_parser('update-data',  help = "Update data")
    sp.add_argument("id", help="Id for update")
    sp.add_argument('--name', help='Name to update')
    sp.add_argument('--fullname', help='Fullname to update')
 
    #delete data
    sp = subparsers.add_parser('delete-data',  help = "Delete data")
    sp.add_argument("--id", action=EnvDefault,  dest="id", default=None, help="Id", envvar="ID")

    #Argument parser
    args = ap.parse_args()
    
    cmd = Env()
    #Calling the function for listing data
    if args.subparser_name == 'list-data':
        cmd.list_data(args)
    
    #Calling the function for creating role
    if args.subparser_name == 'create-data':
        datum = normalize(args)
        cmd.create_data(datum)
        
    #Calling the function for update data
    if args.subparser_name == 'update-data':
        print 'args', args
        datum = normalize(args)
        cmd.update_data(**datum)

    #Calling the function for delete data
    if args.subparser_name == 'delete-data':
        datum = normalize(args)
        cmd.delete_data(datum)