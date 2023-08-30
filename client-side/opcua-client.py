import time
import hashlib
from opcua import ua, Client
from datetime import datetime

class SubHandler(object):
    def datachange_notification(self, node, value, data):
        print(f'{node} is updated to {value}')
        print()
    # end datachange_notification()

    def event_notification(self, event):
        print(f'received an event from {event.SourceName}:')
        if event.SourceName == 'object':
            print(f'NumericProperty: {event.NumericProperty}')
            print(f'StringProperty: {event.StringProperty}')
        # end if

        print(f'Message: {event.Message.Text}')
        print()
    # end event_notification()
# end class SubHandler

def getVariableInfo(node):
    if node.get_node_class().name == 'Variable':
        print(f'NodeId: {node.get_path()[-1]}')
        print(f'NodeClass: {node.get_node_class().name}')
        print(f'BrowseName: {node.get_browse_name().to_string()}')
        print(f'DisplayName: {node.get_display_name().Text}')
        print(f'DataType: {node.get_data_type_as_variant_type().name}')
        print(f'ValueRank: {node.get_value_rank().name}')
        print(f'Value: {node.get_value()}')
        print(f'AccessLevel: {[item.name for item in node.get_access_level()]}')
        print()
    else: print('ERROR: node is NOT a Variable!')
# end getVariableInfo()

if __name__ == '__main__':
    # client initialization
    client = Client('opc.tcp://localhost:4840')
    # client.set_security_string('Basic256Sha256,Sign,security/client_cert.pem,security/client_prikey.pem')
    # client.set_security_string('Basic256Sha256,SignAndEncrypt,security/client_cert.pem,security/client_prikey.pem')
    # username/password authentication => opcua/server/user_manager.py
    # username = input('Enter username: ')
    # password = input('Enter password: ')
    # hashed_password = hashlib.sha3_256(password.encode(encoding='UTF-8')).hexdigest()
    # # must set user/password before connect
    # client.set_user(username)
    # client.set_password(hashed_password)
    
    try:
        client.connect()
        print('Username/Password authentication passed')
        # print()

        # get namespace index
        ns_index = client.get_namespace_array().index('OPCUA_SERVER')

        # (1) get nodes via nodeid
        var = client.get_node(f'ns={ns_index};i=1')
        getVariableInfo(var)
        # # array = client.get_node(f'ns={ns_index};i=4')
        # # getVariableInfo(array)
        # # prop = client.get_node(f'ns={ns_index};i=8')
        # # getVariableInfo(prop)

        # # (2) get nodes via browse path
        # obj = client.get_root_node().get_child(['0:Objects', f'{ns_index}:object'])
        # # for node in obj.get_children():
        # #     getVariableInfo(node)

        # # method call
        # obj = client.get_node(f'ns={ns_index};i=1')
        # result = obj.call_method(f'{ns_index}:method', 2, 123) # call_method(nodeid, args)
        # print(f"Method's return value: {result}")
        # print()

        # # Historical Data Access
        # server_node = client.get_node(ua.ObjectIds.Server)
        # end_time = datetime.utcnow()
        # var_history = var.read_raw_history(None, end_time, 0)
        # # error => obj_event_history = obj.read_event_history(None, end_time, 0)
        # server_node_event_history = server_node.read_event_history(None, end_time, 0)
        # # print out length of historical data
        # print(f'length of var history: {len(var_history)}')
        # print(f'length of server_node history: {len(server_node_event_history)}')
        # print()

        # # subscription
        # handler = SubHandler()
        # sub = client.create_subscription(500, handler)
        # # subscribe to data changes
        # sub.subscribe_data_change(var)
        # # subscribe to default events
        # sub.subscribe_events()
        # # subscribe to custom events
        # obj = client.get_node(f'ns={ns_index};i=1')
        # event = client.get_root_node().get_child(['0:Types', '0:EventTypes', '0:BaseEventType', '2:event'])
        # sub.subscribe_events(obj, event)
        # #
        # while True: time.sleep(0.1)
    except ua.uaerrors._auto.BadUserAccessDenied:
        print('Username/Password authentication failed')
    #finally:
       # try: client.disconnect()
       # except OSError: pass
    # end try-except-finally
# end if