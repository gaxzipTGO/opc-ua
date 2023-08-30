import time
from opcua import ua, uamethod, Server
from opcua.server.history_sql import HistorySQLite

@uamethod
def mutiply(parent, x, y):
    return x * y
# end mutiply()

if __name__ == '__main__':
    # server initialization
    server = Server()
    server.set_endpoint('opc.tcp://0.0.0.0:4840')
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_Sign])
    server.set_server_name('OPCUA Server')
    # server.allow_remote_admin(False)    
    # server.iserver.history_manager.set_storage(HistorySQLite('db/opcua-history.db'))  
    # server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
    server.load_certificate('security/server_cert.pem')
    server.load_private_key('security/server_prikey.pem')

    # register a namespace
    uri = 'OPCUA_SERVER'
    ns_index = server.register_namespace(uri)
    
    # setup nodes
    objects = server.get_objects_node()
    # add object(nodeid, browse_name)
    obj = objects.add_object(f'ns={ns_index};i=1', f'{ns_index}:object')
    # add variable(nodeid, browse_name, value)
    var = obj.add_variable(f'ns={ns_index};i=2', f'{ns_index}:var', 5.7)
    # array = obj.add_variable(f'ns={ns_index};i=4', f'{ns_index}:array', [1, 2, 3])
    # var.set_writable()
    # # add property(nodeid, browse_name, value)
    # prop = obj.add_property(f'ns={ns_index};i=8', f'{ns_index}:property', 'I am a property')
    # # add method(nodeid, browse_name, function_name, [input_args_types], [output_args_types])
    # method = obj.add_method(f'ns={ns_index};i=16', f'{ns_index}:method', mutiply, [ua.VariantType.Int64, ua.VariantType.Int64], [ua.VariantType.Int64])
    # #

    # # setup event and event generator(event_type=None, emitting_node=ua.ObjectIds.Server)
    # # default event
    # default_event_generator = server.get_event_generator()
    # # custom event
    # custom_event_type = server.nodes.base_event_type.add_object_type(ns_index, 'event')
    # custom_event_type.add_property(2, 'NumericProperty', ua.Variant(0, ua.VariantType.Float))
    # custom_event_type.add_property(2, 'StringProperty', ua.Variant(True, ua.VariantType.String))
    # custom_event_generator = server.get_event_generator(custom_event_type, obj)
    # #

    # start the server
    server.start()
    # server.historize_node_data_change(var, period=None, count=100)
    # # error => server.historize_node_event(obj, period=None, count=100)
    # server.historize_node_event(server.get_server_node(), period=None, count=100)

    try:
        # count = 0
        while True:
            time.sleep(1)
            # count += 1
            # # set var's value
            # var.set_value(count)
            # # trigger custom event
            # custom_event_generator.event.Message = ua.LocalizedText(f'Event: {count}')
            # custom_event_generator.event.NumericProperty = count
            # custom_event_generator.event.StringProperty = 'Property ' + str(count)
            # custom_event_generator.trigger()
            # # trigger default event
            # default_event_generator.trigger(message='This is default event')
    finally:
        # server.iserver.history_manager.stop()
        server.stop()
    # end try-finally
# end if