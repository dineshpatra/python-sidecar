server = {
    'port': '9090',
    'host': 'controller'
}

# Pecan Application Configurations
app = {
    'root': 'sidecar.controllers.root.RootController',
    'modules': ['sidecar'],
    'debug': True
}

