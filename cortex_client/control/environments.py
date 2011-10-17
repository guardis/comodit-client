# control.environments - Controller for cortex Environments resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.util import globals
from cortex_client.control.resource import ResourceController
from cortex_client.control.exceptions import NotFoundException
from cortex_client.api.environment import Environment
from cortex_client.api.environment_collection import EnvironmentCollection
from cortex_client.api.directory import Directory

class EnvironmentsController(ResourceController):

    _template = "environment.json"

    def __init__(self):
        super(EnvironmentsController, self ).__init__()
        self._collection = EnvironmentCollection()

    def _new_resource(self, json_data):
        return Environment(json_data)

    def _get_resources(self, argv):
        options = globals.options
        parameters = {}

        # Validate input parameters
        org_uuid = None
        if options.org_uuid:
            org_uuid = options.org_uuid
        elif options.env_path:
            path = options.env_path
            org_uuid = Directory.get_organization_uuid(path)
            if not org_uuid: raise NotFoundException(path)
        elif options.env and options.uuid:
            org_uuid = options.env
        elif options.env:
            path = options.env
            org_uuid = Directory.get_organization_uuid(path)
            if not org_uuid: raise NotFoundException(path)

        if(org_uuid):
            parameters["organizationId"] = org_uuid

        return super(EnvironmentsController, self)._get_resources(argv, parameters)

    def _help(self, argv):
        print '''You must provide an action to perfom on this resource.

Actions:
    list --org [id]    List all environments within an organization
    show [id]          Show the details of an environment
    add                Add an environment
    update [id]        Update an environment
    delete [id]        Delete an environment
'''
