# coding: utf-8

from cortex_client.api.resource import Resource
from cortex_client.api.collection import Collection

class Setting(Resource):
    """
    A host's setting. A setting has a key, a value and a version number. Note
    that in order to add a setting to a host, a change request must be used. Same
    applies to setting's deletion and update. Therefore, a setting does not
    feature setters.
    """
    def __init__(self, collection, json_data = None):
        super(Setting, self).__init__(collection, json_data)

    def get_identifier(self):
        return self.get_key()

    def get_name(self):
        return self.get_key()

    def get_value(self):
        """
        Provides setting's value.
        @return: The value
        @rtype: String
        """
        return self._get_field("value")

    def get_key(self):
        """
        Provides setting's key.
        @return: The key
        @rtype: String
        """
        return self._get_field("key")

    def get_status(self):
        return self._get_field("status")

    def get_version(self):
        """
        Provides setting's version number.
        @return: The version number
        @rtype: Integer
        """
        return int(self._get_field("version"))

    def _show(self, indent = 0):
        """
        Prints this property's state to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        print " "*indent, "Key:", self.get_key()
        print " "*indent, "Value:", self.get_value()
        print " "*indent, "Status:", self.get_status()


class SettingFactory(object):

    def __init__(self, collection):
        self._collection = collection

    """
    Host's setting factory.
    
    @see: L{Setting}
    @see: L{cortex_client.util.json_wrapper.JsonWrapper._get_list_field}
    """
    def new_object(self, json_data):
        """
        Instantiates a L{Setting} object using given state.
        
        @param json_data: A quasi-JSON representation of a Property instance's state.
        @type json_data: String, dict or list
        
        @return: A setting
        @rtype: L{Setting}
        """
        return Setting(self._collection, json_data)


class SettingCollection(Collection):
    def __init__(self, api, collection_path):
        super(SettingCollection, self).__init__(collection_path, api)

    def _new_resource(self, json_data):
        return Setting(self, json_data)
