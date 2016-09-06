# SIDECAR REST API VERSION 2.0

Sidecar REST API is to handel the nova-evacaute process.

## Commands

### For getting all avilable versions

```html
GET  /
```


#### Request Header

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |

#### Request Body

It does not accept and Request Body

> Success Code: 200

> Error code: 401

#### Response Body

| Pareameters   | Data Type   | Description                                                            |
| ------------- |:-----------:|:----------------------------------------------------------------------:|
| versions      | JSON Object | Object containing array of diffrent versions                           |
| v2            | JSON Object | Object containing version 2 info                                       |
| date          | date time   | Release date of the version                                            |
| status        | string      | What is the status of theversion. `current`, `supported`, `dereciated` |


#### Example

> Request:

```html
curl -H 'Content-Type:application/json'\
     -H 'X-Auth-Token:cb5a9e2cc2a94077b209f29a32347b0c'\
     -L http://controller:9090
```

> RESPONSE:

```json
{
    "versions": [
        {
            "v2": {
                 "date": "2016-08-07T00:00:00", 
                 "status": "current"
            }
        }
    ]
}
```

----

### For getting version info v2.0

```html
GET  /v2/
```


#### Request Header

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |

#### Request Body

It does not accept and Request Body

> Success Code: 200

> Error code: 401

#### Response Body

| Pareameters   | Data Type   | Description                                                            |
| ------------- |-----------:|:------------------------------------------------------------------------|
| v2            | JSON Object | Object containing version 2 info                                       |
| date          | date time   | Release date of the version                                            |
| status        | string      | What is the status of theversion. `current`, `supported`, `dereciated` |


#### Example

> Request:

```html
curl -H 'Content-Type:application/json'\
     -H 'X-Auth-Token:cb5a9e2cc2a94077b209f29a32347b0c'\
     -L http://controller:9090/v2/
```

> RESPONSE:

```json 
{
     "v2": {
          "date": "2016-08-07T00:00:00", 
          "status": "current"
     }
} 
```

----

## Nova Evacuates

### Listing and filtering events

```html
GET  /v2/evacuates/events
```
##### Request Headers

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |

##### Query Parameters

| Pareameters           | Data Type        | Description                                       |
| ----------------------|:---------------- | --------------------------------------------------|
| id                    | String           | Id of the event                                   |
| name                  | String           | name of the event                                 |
| node_uuid             | String           | UUID of the host                                  |
| event_create_time     | Date time        | event_creation_time filter                        |
| min_event_create_time | Date Time        | minimum value event creatuin time                 |
| max_event_create_time | Date time        | maximum value for event creation                  |
| marker                | String           | Last seen event id.                               |
| limit                 | positive integer |Number of results to be displayed. Defgault is 30  | 

> SUCCESS CODE: 200

> Error codes: 401, 403, 500

##### RESPONSE Parameters

| Pareameters           | Data Type        | Description                                           |
| ----------------------|:-----------------| ------------------------------------------------------|
| events                | JSON OBJECT      | A json object containg array of events                |
| id                    | String           | Id of the event                                       |
| name                  | String           | name of the event                                     |
| event_status          | string           | What is the status of the event. The possible values: `created`, `completed`, `running` |
| node_uuid             | String           | UUID of the host                                      |
| event_create_time     | Date time        | When the event was created                            |
| event_complete_time   | Date time        | When the event was completed                          |
| vm_uuid_list          | Aarry            | Array containg the vm ids, participated in the event. |
| extra                 | JSON OBJECT      | Extra data in json                                    |

#### Example

> Request:

```html
curl -H 'Content-Type:application/json'
     -H 'X-Auth-Token:0d7f16c43bcc47b69bcc8dddf262097e' 
     -L http://controller:9090/v2/evacuates/events/?limit=30
```

> RESPONSE:

```json 
{
     "events": [
          {
               "id": "59ca965bef7e4a8f99088ac6f50a2e35", 
               "name": "Hello256", 
               "event_status": "created", 
               "event_create_time": "2016-09-02 14:32:17", 
               "event_complete_time": null, 
               "node_uuid": "test", 
               "vm_uuid_list": ["123", "4565"], 
               "extra": null
          }, 
          {
               "id": "7e1318856d7240728e511013c049876e", 
               "name": "Hello2567", 
               "event_status": "created", 
               "event_create_time": "2016-09-02 13:46:32", 
               "event_complete_time": null, 
               "node_uuid": "test", 
               "vm_uuid_list": ["123", "4565"], 
               "extra": null
          }
     ]
}
```

### Get detail of an event

```html
GET  /v2/evacuates/events/{event_id}
```
##### Request Headers

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |


> SUCCESS CODE: 200

> Error codes: 401, 403, 500

##### RESPONSE Parameters

| Pareameters           | Data Type        | Description                                           |
| ----------------------|:-----------------| ------------------------------------------------------|
| event                 | JSON OBJECT      | A json object containg the event detail               |
| id                    | String           | Id of the event                                       |
| name                  | String           | name of the event                                     |
| event_status          | string           | What is the status of the event. The possible values: `created`, `completed`, `running` |
| node_uuid             | String           | UUID of the host                                      |
| event_create_time     | Date time        | When the event was created                            |
| event_complete_time   | Date time        | When the event was completed                          |
| vm_uuid_list          | Aarry            | Array containg the vm ids, participated in the event. |
| extra                 | JSON OBJECT      | Extra data in json                                    |

#### Example

> Request:

```html
curl -X GET 
     -H 'Contrnt-Type:application/json'
     -H 'X-Auth-Token:2c213cc8f62e4c2086592cf7d52b7c21' 
     -L http://controller:9090/v2/evacuates/events/59ca965bef7e4a8f99088ac6f50a2e35
```

> RESPONSE:

```json 
{
     "event": {
          "event_complete_time": null, 
          "node_uuid": "test", 
          "event_create_time": "2016-09-02 14:32:17", 
          "name": "Hello256", 
          "vm_uuid_list": ["123", "4565"], 
          "extra": null, 
          "event_status": "created", 
          "id": "59ca965bef7e4a8f99088ac6f50a2e35"
     }
}
```


## CREATING NEW EVENT
curl -v -X  POST -L http://198.100.181.66:9090/v2/events/ -H 'Content-Type:application/json' -H 'X-Auth-Token:a5452dd6f64c478aac861428ea919138' -d '{"event":{"name":"Hello", "node_uuid":"12345667", "vm_uuid_list":["124", "456"]}}'

Success code: 201
event Name must be start and end with [a-zA-Z0-9].
Requeires: name, node_uuid, event_uuid_list

< HTTP/1.1 201 Created
< Date: Mon, 05 Sep 2016 11:18:27 GMT
* Server Apache/2.4.7 (Ubuntu) is not blacklisted
< Server: Apache/2.4.7 (Ubuntu)
< x-openstack-request-id: req-4e0141e6-886f-4f23-b2e4-e1575ed44c9a
< Content-Length: 242
< Content-Type: application/json; charset=UTF-8
< 
* Connection #0 to host 198.100.181.66 left intact
{"event": {"event_complete_time": null, "node_uuid": "12345667", "event_create_time": "2016-09-05 04:18:27", "name": "Hello", "vm_uuid_list": ["124", "456"], "extra": null, "event_status": "created", "id": "7bff507ab3d846f3a6643721f4458c39"}}





## LISTING EVENTS

curl -v -X  GET -L http://198.100.181.66:9090/v2/events/ -H 'Content-Type:application/json' -H 'X-Auth-Token:a5452dd6f64c478aac861428ea919138'


