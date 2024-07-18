import json

#===CONFIG===

def load_data(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

#===CHECK===

def check_server(data, new_server_id):
    """Checks whether a server with the given server_id already exists."""
    for server in data['servers']:
        if server['server_id'] == new_server_id:
            return False 
    return True  

def check_custom_mess(data, server_id, type):
    """Checks if any welcome/goodbye message exists on the given server."""
    for server in data['servers']:
        if server['server_id'] == server_id:
            if type == 'welcome':
                if server['welocme_mess']:
                    return True
            elif type == 'bye':
                if server['bye_mess']:
                    return True
            else:
                return False  
    return False

def check_autorole_mess(path, server_id):
    """Checks if any autorole message exists."""
    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            autorole_mess = server.get('autorole_mess', [])
            if autorole_mess and len(autorole_mess) > 0:
                last_message = autorole_mess[-1]
                if 'message_id' in last_message:
                    return last_message['message_id'], last_message['channel_id']
                else:
                    return False
            else:
                return False
    
    return False
#===ADD===

def add_server(data, server_name, server_id):
    """Adds a new server with default values."""
    # Finding the highest id and setting a new id
    if data['servers']:
        new_id = max(server['id'] for server in data['servers']) + 1
    else:
        new_id = 0
    
    # Adding a new server with default values
    new_server = {
        "id": new_id,
        "server_name": server_name,
        "server_id": server_id,
        "dev_mode": False,
        "welocme_mess": [],
        "bye_mess": [],
        "autorole_mess": [],
        "on_join_roles": []
    }
    data['servers'].append(new_server)

    return data

def add_welcome_message(path, server_id, channel_id, title, desc):
    """Adds a welcome message to a server."""

    data = load_data(path)

    new_welcome_mess = {
        "channel_id" : channel_id,
        "title": title,
        "desc": desc
    }

    for server in data['servers']:
        if server['server_id'] == server_id:
            server['welocme_mess'] = []
            server['welocme_mess'].append(new_welcome_mess)
            save_data(path, data)
            return True
    return False

def add_leave_message(path, server_id, channel_id, message):
    """Adds a leave message to a server."""

    data = load_data(path)

    new_welcome_mess = {
        "channel_id" : channel_id,
        "message": message
    }

    for server in data['servers']:
        if server['server_id'] == server_id:
            server['bye_mess'] = []
            server['bye_mess'].append(new_welcome_mess)
            save_data(path, data)
            return True
    return False

def add_role_on_join(path, server_id, role_id):
    """Adds a role to be given to users when they join a server."""

    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            new_role = {
                "id": len(server['on_join_roles']),
                "role_id": role_id
            }
            server['on_join_roles'].append(new_role)
            save_data(path, data)
            return True

    return False

def add_autorole(path, server_id, message_id, channel_id):
    """Adds an autorole on server to a database."""

    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            new_tracked_mess = {
                "id": len(server['autorole_mess']),
                "message_id": message_id,
                "channel_id": channel_id,
                "content": []
            }
            server['autorole_mess'].append(new_tracked_mess)
            save_data(path, data)
            return True

    return False

def add_autorole_content(path, server_id, message_id, emoji, role_id, role_name):
    """Adds content to an autorole message on a server."""

    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            for mess in server['autorole_mess']:
                if mess['message_id'] == message_id:
                    new_content = {
                        "role_id": role_id,
                        "role_name": role_name,
                        "emoji": emoji
                    }
                    mess['content'].append(new_content)
                    save_data(path, data)
                    return True

    return False

#===DELETE===


#===CHANGE===

def change_dev_mode(path, server_id: int, new_dev_mode: bool):
    """Changes the dev_mode value"""
    data = load_data(path)
    for server in data['servers']:
        if server['server_id'] == server_id:
            server['dev_mode'] = new_dev_mode
            save_data(path, data)
            return True
    return False

#===GET===

def get_welcome_message(path, server_id):
    """Reads the welcome message from the server and returns its details."""
    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            welcome_mess = server.get('welocme_mess', [])
            if welcome_mess:
                return {
                    "channel_id": welcome_mess[0].get("channel_id"),
                    "title": welcome_mess[0].get("title"),
                    "desc": welcome_mess[0].get("desc")
                }
    return None

def get_leave_message(path, server_id):
    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            welcome_mess = server.get('bye_mess', [])
            if welcome_mess:
                return {
                    "channel_id": welcome_mess[0].get("channel_id"),
                    "message": welcome_mess[0].get("message")
                }
    return None    

def get_join_roles(path, server_id):
    """Returns a list of roles assigned to users when joining the server."""
    
    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            if 'on_join_roles' in server:
                return [role['role_id'] for role in server['on_join_roles']]
            else:
                return [] 

    return None

def get_autorole_content(path, server_id, message_id):
    """
    Retrieve autorole message content based on server_id and message_id.
    Returns None if no matching server or autorole message is found.
    """
    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            for autorole_message in server['autorole_mess']:
                if autorole_message['message_id'] == message_id:
                    return autorole_message['content']

    return None

x = get_autorole_content('data/db/db_servers.json', 1203308589557620738, 1254162800964800563)
print(x)