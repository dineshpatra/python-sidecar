#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Name : SQL Alchemy test file
Desc;  SQL Alchemy script
Created By: Binoy M V
Created On:  26-July-2016
"""

#importing the packages
from oslo_config import cfg
from sqlalchemy import *
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DATETIME, Enum
import enum, uuid, datetime
from sqlalchemy.dialects.postgresql import UUID
from sidecar import exception
import simplejson as json

class StatusEnum(enum.Enum):
    completed = 'completed'
    created   = 'created'
    running   = 'running'
    #nothing   = ''


class Evacuate():
    """User class for managing the user operation."""
    
    #Definidng the meta data
    metadata = MetaData()
    
    #Creating the db connection
    parser = cfg.ConfigParser(cfg.CONF.config_file[0],{})
    parser.parse() 
    for section , entries in parser.sections.iteritems():
        if section ==  'database': 
            engine = create_engine(entries['connection'][0], pool_recycle=3600)
            conn = engine.connect()
    
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
        name createUser
        Params: userLists
        Return : Json data
        """
        get_data_select = select([self.evacuate_events]).where(self.evacuate_events.c.id == uuid)
        get_data = self.conn.execute(get_data_select)
        if not get_data.rowcount:
            raise exception.NotFound("No event with id " + uuid + " found.")
        data = get_data.fetchone()
        result = {
            "id": uuid,
            "name": data['name'],
            "event_status": data["event_status"],
            "event_create_time": data["event_create_time"],
            "event_complete_time": data["event_complete_time"],
            "node_uuid": data["node_uuid"],
            "vm_uuid_list": json.loads(data["vm_uuid_list"]),
            "extra": None
        }

        if data['extra']:
            result['extra'] = json.loads(data['extra'])
        
        return result

    def listEvent(self, args={}):
        """
        name listUser
        Params: NA
        Return : Json data
        """
        allowed_args = [
            'id',
            'node_uuid', 
            'event_create_time>', 
            'event_create_time>=', 
            #'vm_uuid', 
            'event_create_time<', 
            'event_create_time<=',
            'marker',
            'limit'
        ]
        valid_args = {}
        for arg in args:
            if arg in allowed_args:
                valid_args.append(arg)
        

        get_event_list = select([self.evacuate_events])
        offset = 0
        limit  = 30
      
        get_event_list = get_event_list.limit(limit).offset(offset)
        #Selecing the data
        #selecting = select([self.evacuate_events]).where(self.evacuate_events.c.uuid == uuid)
        result = self.conn.execute(get_event_list)
        eventList = []
    
        for row in result:
            eventData = {}
            eventData['id'] = row['id']
            eventData['name'] = row['name']
            eventData['event_status'] = row['event_status']
            eventData['event_create_time'] = row['event_create_time']
            eventData['event_complete_time'] = row['event_complete_time']
            eventData['node_uuid'] = row['node_uuid']
            eventData['vm_uuid_list'] = row['vm_uuid_list']
            eventData['extra'] = row['extra']
            eventList.append(eventData)  
        return eventList
 
    def update_event(self, uuid, data):
        """
        name updateUser
        Params: id
        Return : Json data
        """
        if "name" in data:
            name_check = select([self.evacuate_events]).where(self.evacuate_events.c.name == data['name'])
            name_exist = self.conn.execute(name_check).rowcount
            if name_exist:
                raise exception.Conflict("There is already an event named " + data['name'])

        get_data_select = select([self.evacuate_events]).where(self.evacuate_events.c.id == uuid)
        get_data = self.conn.execute(get_data_select)
        if not get_data.rowcount:
            raise exception.NotFound("No event with id " + uuid + " found.")
        
        if 'vm_uuid_list' in data:
            data['vm_uuid_list'] = json.dumps(data['vm_uuid_list'])

        #Updating the data
        update = self.evacuate_events.update().where(self.evacuate_events.c.id == uuid).values(data)
        self.conn.execute(update)
 
    def deleteEvent(self, uuid):
        """
        name  deleteUser
        Params: id
        Return : NA
        """
        #Deleting the data
        query = self.evacuate_events.delete().where(self.evacuate_events.c.uuid == uuid)

