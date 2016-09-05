schema = {
    "type" : "object",
    "required": ["event"],
    "properties" : {
        "event": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "pattern": r"^[a-zA-Z0-9]([\w\s-]+[a-zA-Z0-9])$"
                },
                "vm_uuid_list": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "uniqueItems": True
                }
            }
        }
    }    
}
