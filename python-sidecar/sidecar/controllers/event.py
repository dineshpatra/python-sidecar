from pecan import expose
from pecan.secure import secure
from oslo_config import cfg
import pecan
from sidecar import rbac
from sidecar.model import sidecar_model as sql_model
import sidecar.validation as validation
import json
import requests
import ConfigParser
import logging
from sidecar import exception

class EventController(object):
    """
    Desc: Controller for the evacuate
    Name: EvacuateController
    
    
    """
    def __init__(self, data=None):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """
        self.evacuates = sql_model.Evacuate()


    @expose(generic=True, template='json')
    def details(self, *kw):
        """
        # | Method to get the details of an event.
        # |
        # | Arguments: 
        # |     <kw>: List containg url params
        # |     
        # | @Returns: Null
        """
        if (len(kw) == 0 or len(kw) > 1)\
           or (pecan.request.method != 'GET'):
            # | If there is no key, then return
            # | 404 error
            pecan.response.status = 404
            return send_error(404, 'Not Found', 'Resource not found.')
        event_id = kw[0]
        try:
            result = self.evacuates.get_detail(event_id)
        except exception.NotFound as e:
            return send_error(e.code, e.title, e.message)
        return { "event": result }
     
    @expose(generic=True, template='json')
    def index(self, **kw):
        """
        # | Function to list the events
        # |
        # | @Arguments:
        # |     <kw>: Url query parameters
        # |
        # | @Returns: Json response
        """
        try:
            eventList = self.evacuates.listEvent(kw)
            return {"events": eventList}
        except Exception as err:
            pecan.response.status = 500
            print str(err)
            return {
                "error": {
                    "code": 500,
                    "title": "Internal Server Error",
                    "message": "Unknown error occured."
                }
            }
    
    @expose(generic=True, template='json')
    @index.when(method='POST', template='json')
    def index_POST(self, *data, **json):
        valid = validation.Validation()
        try:
            valid.json_header()
        except exception.NotJSONHeader as e:
            return send_error(e.code, e.title, e.message)
        try:
            json_data = valid.json_data('create_event', pecan.request.body_file.read())
        except exception.BadData as e:
            return send_error(e.code, e.title, e.message)
        try:
            data = json_data['event']
            new_event_id = self.evacuates.createEvent(data)
        except exception.Conflict as e:
            return send_error(e.code, e.title, e.message)
            pecan.abort(e.code, e.message)
        pecan.response.status = 201
        return { "event": self.evacuates.get_detail(new_event_id)}
     
    @expose(generic=True, template='json')
    #@index.when(method='PUT', template='json')
    def edit(self, *kw):
        if (len(kw) == 0 or len(kw) > 1)\
           or (pecan.request.method != 'PUT'):
            # | If there is no key, then return
            # | 404 error
            pecan.response.status = 404
            return send_error(404, 'Not Found', 'Resource not found.')
        event_id = kw[0]
        valid = validation.Validation()
        try:
            valid.json_header()
        except exceptio.NotJSONHeader as e:
            return send_error(e.code, e.title, e.message)
        try:
            json_data = valid.json_data('edit_event', pecan.request.body_file.read())
        except exception.BadData as e:
            return send_error(e.code, e.title, e.message)
        try:
            self.evacuates.update_event(event_id, json_data['event'])
        except exception.Conflict as e:
            return send_error(e.code, e.title, e.message)
        except exception.NotFound as e:
            return send_error(e.code, e.title, e.message)
        pecan.response.status = 204    
        #return {"user": "in the put"}

    @expose(generic=True, template='json')
    @index.when(method='DELETE', template='json')
    def index_DELETE(self, **kwargs):
        self.evacuates.deleteEvent(kwargs['uuid'])
        return {"user": "in the delete list"}


def send_error(code, title, message):
    pecan.response.status = code
    return {
        "error": {
            "code": code,
            "title": title,
            "message": message
        }
    }
