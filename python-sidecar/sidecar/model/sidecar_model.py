# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: RootController.py                        |
# |                                                     |
# | Package Name: Python-Sidecar REST API               |
# |                                                     |
# | Version: 2.0                                        |
# |                                                     |
# | Sofatware: Openstack                                |
# |_____________________________________________________|
# | Copyright: 2016@nephoscale.com                      |
# |                                                     |
# | Author:  info@nephoscale.com                        |
# |_____________________________________________________|

#importing the packages
from oslo_config        import cfg
from oslo_log           import log
from oslo_db.sqlalchemy import models
from sqlalchemy.ext     import declarative
from sqlalchemy         import *
from sqlalchemy.sql     import select
from sqlalchemy         import Table, Column, Integer, String, MetaData, ForeignKey, DATETIME, Enum
from sidecar            import exception
from sqlalchemy.orm     import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
try:   import simplejson as json
except ImportError: import json
import sqlalchemy, ConfigParser, enum, uuid, datetime, collections

CONF = cfg.CONF
LOG = log.getLogger(__name__)

# READ THE CONNECTION VARIABLE
try:
    config_file = cfg.CONF.config_file[0]
    config = ConfigParser.ConfigParser()
    config.read(config_file) 
    sql_connection = config.get('database', 'connection', '')   
except Exception as e:
    LOG.error(str(e))
    sql_connection = ''

class Evacuate():
    """
    # | Evacuate model
    """
    metadata = MetaData()
    engine   = create_engine(sql_connection, pool_recycle=3600)
    conn     = engine.connect()
    
    #Creating the tables
    evacuate_events = Table('evacuate_events', metadata,
        Column('id',                  String(100),       primary_key=True,  unique=True, nullable=False),  # Event id column
        Column('name',                String(100),       default='',        unique=True, nullable=False),
        Column('event_status',        Enum('created', 'completed', 'running'), default='created', nullable=True),
        Column('event_create_time',   DATETIME,         default='0000-00-00 00:00:00', nullable=False),
        Column('event_complete_time', DATETIME,         default='0000-00-00 00:00:00', nullable=True),
        Column('node_uuid',           Text),
        Column('vm_uuid_list',        Text),
        Column('extra',               Text)
    )
    metadata.create_all(engine)
    
    def createEvent(self, kw):
        """
        name createUser
        Params: userLists
        Return : Json data
        """
        name_check = select([self.evacuate_events]).where(self.evacuate_events.c.name == kw['name'])
        name_exist = self.conn.execute(name_check).rowcount
        if name_exist:
            raise exception.Conflict("There is already an event named " + kw['name'])

        unique_id = uuid.uuid4().hex
        arg = {
            "id": unique_id,
            "name": kw['name'],
            "event_status": "created",
            "event_create_time": datetime.datetime.now(),
            "node_uuid": kw["node_uuid"],
            "vm_uuid_list": json.dumps(kw["vm_uuid_list"])
        }
        #Inserting the data
        ins = self.evacuate_events.insert().values(arg)
        result = self.conn.execute(ins)
        return unique_id

    def get_detail(self, uuid):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  <uuid>: Id of the event
        # |
        # | Returns: Json
        """
        get_data_select = select([self.evacuate_events]).where(self.evacuate_events.c.id == uuid)
        get_data = self.conn.execute(get_data_select)
        if not get_data.rowcount:
            LOG.error("No event with id " + uuid + " found.")
            raise exception.NotFound("No event with id " + uuid + " found.")
        data = get_data.fetchone()
        result = collections.OrderedDict()
        result["id"]                  = uuid
        result["name"]                = data["name"]
        result["event_status"]        = data["event_status"]
        result["event_create_time"]   = data["event_create_time"]
        result["event_complete_time"] = data["event_create_time"]
        result["node_uuid"]           = data["node_uuid"]
        result["vm_uuid_list"]        = None
        result['extra']               = None
        
        # If the proper data is there 
        # then convert them into json
        if data["vm_uuid_list"]:
            result["vm_uuid_list"] = json.loads(data["vm_uuid_list"])
        if data['extra']:
            result['extra'] = json.loads(data['extra'])
        
        return result

    def list_events(self, args={}):
        """
        # | Method to list the events
        # |
        # | Arguments: Distionary containg the flter values
        # |
        # | Returns Distionary
        """
        allowed_args = [
            'id',
            'name',
            'node_uuid', 
            'event_create_time', 
            'min_event_create_time',
            'max_event_create_time', 
            'marker',
            'limit'
        ]
        valid_args = {}
        for arg in args:
            # | For each given argument
            # | If it matches with allowed argument
            # | Then treat it as valid arg
            if arg in allowed_args:
                valid_args[arg] = args[arg]

        # Okay Bow lets start our query builder
        get_event_list = select([self.evacuate_events])
        for key in valid_args:
            val = valid_args[key].strip()
            if not val:
                continue;
            if key == "id":
                get_event_list = get_event_list.where(self.evacuate_events.c.id == val)
            if key == "name":
                get_event_list = get_event_list.where(self.evacuate_events.c.name == val)
            if key == 'node_uuid':
                get_event_list = get_event_list.where(self.evacuate_events.c.node_uuid == val)
            if key == 'event_create_time':
                get_event_list = get_event_list.where(self.evacuate_events.c.event_create_time == val)
            if key == 'min_event_create_time':
                get_event_list = get_event_list.where(self.evacuate_events.c.event_create_time >= val)
            if key == 'max_event_create_time':
                get_event_list = get_event_list.where(self.evacuate_events.c.event_create_time <= val)
        
        get_event_list = get_event_list.order_by(desc(self.evacuate_events.c.event_create_time))
        # As per the documentaion in
        # https://specs.openstack.org/openstack/api-wg/guidelines/pagination_filter_sort.html
        # we need to add pagination  only after the filtering. So lets just filter out it.
        #
        # Point to be noted, though it is a bad idea to fetch all the data from db (in worst case when
        # there is no filter option), for time being we have done this way. Later we need to use sqlAlchemy
        try:
            result = self.conn.execute(get_event_list)
        except Exception as e:
            LOG.error(str(e))
            return []

        event_list = []
        for row in result:
            event_data = collections.OrderedDict()
            event_data['id']                  = row['id']
            event_data['name']                = row['name']
            event_data['event_status']        = row['event_status']
            event_data['event_create_time']   = row['event_create_time']
            event_data['event_complete_time'] = row['event_complete_time']
            event_data['node_uuid']           = row['node_uuid']
            vm_uuid_list = []
            if row['vm_uuid_list']:
                vm_uuid_list = json.loads(row['vm_uuid_list'])
            event_data['vm_uuid_list']        = vm_uuid_list
            event_data['extra']               = row['extra']
            event_list.append(event_data)
 
        first_index = 0
        if 'marker' in valid_args:
            marker = valid_args['marker']
            if marker is not None:
                for (marker_index, event) in enumerate(event_list):
                    if event['id'] == marker:
                        # we start pagination after the marker
                        first_index = marker_index + 1
                        break
        
        limit = 30

        # Checking for the limit. If the given
        # Limit is not positive then, return emepty result
        if "limit" in valid_args:
            if not valid_args["limit"].isnumeric():
                return []
            if not valid_args["limit"] > 0:
                return []
            limit = valid_args["limit"].strip()
        limit = int(float(limit))

        event_list = event_list[first_index:limit]
        return event_list
 
    def update_event(self, event_id, data):
        """
        # | Method to update an events
        # |
        # | Arguments:
        # |     <uuid>: event id
        # |     <data>: Dictionary containg diffrent update sections
        # |
        # | Returns: None
        """
        event_detail = self.get_detail(event_id)
        if "name" in data:
            # | If name is the parameter check for 
            # | the conflict
            name_check = select([self.evacuate_events]).where(
                and_(
                    self.evacuate_events.c.name == data['name'],
                    self.evacuate_events.c.id != event_id
                ))
            name_exist = self.conn.execute(name_check).rowcount
            if name_exist:
                raise exception.Conflict("There is already an event named " + data['name'])

        if 'event_status' in data:
            if data['event_status'] == 'completed':
                data['event_complete_time'] = datetime.datetime.now()
            else:
                data['event_complete_time'] = '0000-00-00 00:00:00'

        if 'vm_uuid_list' in data:
            data['vm_uuid_list'] = json.dumps(data['vm_uuid_list'])

        #Updating the data
        update = self.evacuate_events.update().where(self.evacuate_events.c.id == event_id).values(data)
        self.conn.execute(update)
 
    def delete_event(self, event_id):
        """
        # | Function to delete an event
        # |
        # | Arguments:
        # |     <event_id>: id of the event
        # |
        # | Returns: None
        """

        # | A vent can be deleted, only if it's status completed
        # | Otherwise by deleting it will make error
        event_detail = self.get_detail(event_id)
        if event_detail['event_status'] != 'completed':
            raise exception.Forbidden("Events with completed status only can be deleted.")
        query = self.evacuate_events.delete().where(self.evacuate_events.c.id == event_id)
        self.conn.execute(query)
