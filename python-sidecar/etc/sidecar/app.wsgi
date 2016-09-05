# File Name: app.wsgi
# This file is used during our server start
# Copy Right: nephoscale@2016
# Start Date: 26th July 2016

import os
import socket
import sys
from oslo_config import cfg
import oslo_i18n
from oslo_log import log
from oslo_reports import guru_meditation_report as gmr
sys.path.append("/opt/stack/sidecar/sidecar/sidecar")
import app
sys.path.remove("/opt/stack/sidecar/sidecar/sidecar")


OPTS = [
    cfg.StrOpt('host',
               default=socket.gethostname(),
               help='Name of this node, which must be valid in an AMQP '
               'key. Can be an opaque identifier. For ZeroMQ only, must '
               'be a valid host name, FQDN, or IP address.'),
    cfg.IntOpt('http_timeout',
               default=600,
               help='Timeout seconds for HTTP requests. Set it to None to '
                    'disable timeout.'),
]
cfg.CONF.register_opts(OPTS)

CLI_OPTS = [
    cfg.StrOpt('os-username',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_USERNAME', 'sidecar'),
               help='User name to use for OpenStack service access.'),
    cfg.StrOpt('os-password',
               deprecated_group="DEFAULT",
               secret=True,
               default=os.environ.get('OS_PASSWORD', 'default'),
               help='Password to use for OpenStack service access.'),
    cfg.StrOpt('os-tenant-id',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_TENANT_ID', ''),
               help='Tenant ID to use for OpenStack service access.'),
    cfg.StrOpt('os-tenant-name',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_TENANT_NAME', 'sidecar'),
               help='Tenant name to use for OpenStack service access.'),
    cfg.StrOpt('os-cacert',
               default=os.environ.get('OS_CACERT'),
               help='Certificate chain for SSL validation.'),
    cfg.StrOpt('os-auth-url',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_AUTH_URL',
                                      'http://198.100.181.66:5000/v2.0'),
               help='Auth URL to use for OpenStack service access.')
]

cfg.CONF.register_cli_opts(CLI_OPTS, group="service_credentials")

API_OPT = cfg.IntOpt('workers',
                     default=1,
                     min=1,
                     deprecated_group='DEFAULT',
                     deprecated_name='api_workers',
                     help='Number of workers for api, default value is 1.')
cfg.CONF.register_opt(API_OPT, 'api')

NOTI_OPT = cfg.IntOpt('workers',
                      default=1,
                      min=1,
                      deprecated_group='DEFAULT',
                      deprecated_name='notification_workers',
                      help='Number of workers for notification service, '
                           'default value is 1.')
cfg.CONF.register_opt(NOTI_OPT, 'notification')

COLL_OPT = cfg.IntOpt('workers',
                      default=1,
                      min=1,
                      deprecated_group='DEFAULT',
                      deprecated_name='collector_workers',
                      help='Number of workers for collector service. '
                           'default value is 1.')
cfg.CONF.register_opt(COLL_OPT, 'collector')


LOG = log.getLogger(__name__)
oslo_i18n.enable_lazy()
log.register_options(cfg.CONF)
log_levels = (cfg.CONF.default_log_levels +
                  ['stevedore=INFO', 'keystoneclient=INFO'])
log.set_defaults(default_log_levels=log_levels)
argv = []
cfg.CONF(argv[1:], project='sidecar', validate_default_values=True, version="1.0", default_config_files=None)
application = app.load_app()
