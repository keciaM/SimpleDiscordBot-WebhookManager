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
    """Sprawdza, czy na danym serwerze istnieje jakakolwiek wiadomość powitalna/pożegnalna."""
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
    """Odczytuje wiadomość powitalną z serwera i zwraca jej szczegóły."""
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
    """Zwraca listę ról przypisywanych użytkownikom przy dołączaniu do serwera."""
    
    data = load_data(path)

    for server in data['servers']:
        if server['server_id'] == server_id:
            if 'on_join_roles' in server:
                return [role['role_id'] for role in server['on_join_roles']]
            else:
                return [] 

    return None

# x = get_join_roles('data/db/db_servers.json', 942844318702534717)
# print(x)
