# SIDECAR REST API VERSION 2.0

## GETTING AVILABLE VERSIONS

curl -X GET -L http://controller:9090 -H 'Content-Type:application/json' -H 'X-Auth-Token:&lt;keystone token&gt;'

### Example

curl -v -X GET -L http://198.100.181.66:9090 -H 'Content-Type:application/json' -H 'X-Auth-Token:a5452dd6f64c478aac861428ea919138'

> GET / HTTP/1.1
> User-Agent: curl/7.35.0
> Host: 198.100.181.66:9090
> Accept: */*
> Content-Type:application/json
> X-Auth-Token:a5452dd6f64c478aac861428ea919138
> 
< HTTP/1.1 200 OK
< Date: Mon, 05 Sep 2016 10:55:29 GMT
* Server Apache/2.4.7 (Ubuntu) is not blacklisted
< Server: Apache/2.4.7 (Ubuntu)
< x-openstack-request-id: req-17c151d4-8958-45fa-b977-d64bfc6d42e7
< Content-Length: 76
< Content-Type: application/json; charset=UTF-8
< 
* Connection #0 to host 198.100.181.66 left intact
{"versions": [{"v2": {"date": "2016-08-07T00:00:00", "status": "current"}}]}

## GETTING V2 INFO

curl -v -X GET -L http://198.100.181.66:9090/v2 -H 'Content-Type:application/json' -H 'X-Auth-Token:a5452dd6f64c478aac861428ea919138'

### RESPONSE

< HTTP/1.1 200 OK
< Date: Mon, 05 Sep 2016 10:59:43 GMT
* Server Apache/2.4.7 (Ubuntu) is not blacklisted
< Server: Apache/2.4.7 (Ubuntu)
< x-openstack-request-id: req-a484b147-53db-48b4-8f09-3b2cd5861134
< Content-Length: 60
< Content-Type: application/json; charset=UTF-8
< 
* Connection #0 to host 198.100.181.66 left intact
{"v2": {"date": "2016-08-07T00:00:00", "status": "current"}} 
