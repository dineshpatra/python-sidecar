#-*- coding: utf-8 -*-
# ______________________________________________________________________
# | User model file                                                    |
# |                                                                    |
# | This file is responsible for handling the user related stuff in db |
# |____________________________________________________________________|
# | Copyright: 2016@nephoscale.com<info@nephoscale.com>                |
# |                                                                    |
# | Start date: 22nd Aug 2016                                          |
# |____________________________________________________________________|

#importing the packages
from oslo_config import cfg
from sqlalchemy import *
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import logging

class User():
    """User class for managing the user operation."""
    
    #Definidng the meta data
    metadata = MetaData()
    parser = cfg.ConfigParser(cfg.CONF.config_file[0],{})
    parser.parse() 
    for section , entries in parser.sections.iteritems():
        if section ==  'database': 
            engine = create_engine(entries['connection'][0], pool_recycle=3600)
            conn = engine.connect()    
 
    #Creating the tables
    users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100)),
        Column('fullname', String(100)),)

    def createUser(self, kw):
        """
        name createUser
        Params: userLists
        Return : Json data
        """

        #Inserting the data
        logging.info('Inserting details into the user table')
        ins = self.users.insert().values(kw)
        result = self.conn.execute(ins)
        
     
    def listUser(self, name=None):
        """
        name listUser
        Params: NA
        Return : Json data
        """
        
        #Selecing the data
        logging.info('Selecting details from the user table')
        selecting = select([self.users])
        result = self.conn.execute(selecting)
        userList = []
        for row in result:
            userData = {}
            userData['id'] = row['id']
            userData['name'] = row['name']
            userData['fullname'] = row['fullname']
            userList.append(userData)   
        return userList
 
    def updateUser(self, id, kw):
        """
        name updateUser
        Params: id
        Return : Json data
        """
        #Updating the data
        logging.info('Updating the details of user table')
        update = self.users.update().where(self.users.c.id == id).values(kw)
        self.conn.execute(update)
 
    def deleteUser(self, id):
        """
        name  deleteUser
        Params: id
        Return : NA
        """
        
        #Deleting the data
        logging.info('Deleteting details from the user table')
        self.conn.execute(self.users.delete().where(self.users.c.id == id))
