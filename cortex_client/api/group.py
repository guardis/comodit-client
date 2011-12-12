# coding: utf-8

from resource import Resource
from cortex_client.util.json_wrapper import StringFactory

class Group(Resource):
    def __init__(self, collection, json_data = None):
        super(Group, self).__init__(collection, json_data)

    def get_name(self):
        return self._get_field("name")

    def get_users(self):
        return self._get_list_field("users", StringFactory())

    def add_user(self, user):
        return self._add_to_list_field("users", user)

    def clear_users(self, user):
        return self._set_list_field("users", [])

    def _show(self, indent = 0):
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Users:"
        users = self.get_users()
        for u in users:
            print " "*(indent + 2), u