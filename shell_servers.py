file_name = "servers"
sep = '	'
import justsimplestdb
_db = justsimplestdb.Instance(file_name, separator=sep)
user_query = ""
performed_query = ""
available_methods_dict = {}

def scrap_methods_and_their_comment():
        methods_list = []
        comments_list = []
        read_file = _db.code()
        for index in range(len(read_file)):
            line = read_file[index]
            line = line[4:]
            if line.startswith("def ") and not "def __" in line:
                line = line[4:]
                line = line.split()
                line[0] = line[0].split("(")
                line[0] = line[0][0]
                methods_list.append(line[0])
            try:
                if '#start' in read_file[index]:
                    comment = ""
                    subindex = 2
                    while not '#end' in read_file[index+subindex]:
                        
                        comment += read_file[index+subindex]
                        subindex += 1
                    comments_list.append(comment[:-5])
            except IndexError:
                pass
        return {"methods_list": methods_list, "comments_list": comments_list}

for i in range(len(scrap_methods_and_their_comment()["methods_list"])):
    available_methods_dict[scrap_methods_and_their_comment()["methods_list"][i]] = scrap_methods_and_their_comment()["comments_list"][i]

def print_available_methods(method_name: str = "all"):
    global available_methods_dict
    available_methods = list(available_methods_dict.keys())
    methods_decription = list(available_methods_dict.values())
    if method_name == 'all':
        print('-'*100)
        for index, method_description in enumerate(methods_decription):
            print()
            print(f'Method name: {available_methods[index]}')
            print('Method description: ')
            print(f'{method_description}')
            print()
        print('-'*100)
    else:
        for index, method_description in enumerate(methods_decription):
            if method_name not in available_methods:
                print(f'No such "{method_name}" exists in DBMS methods.')
                break
            if available_methods[index] == method_name:
                print('-'*100)
                print()
                print(f'Method name: {available_methods[index]}')
                print('Method description: ')
                print(f'{method_description}')
                print('-'*100)
                break

while user_query != "exit":
    print()
    user_query = input("Your query: ")
    if user_query == "?" or user_query == "help":
        print_available_methods()
    elif user_query.startswith("?") or user_query.startswith("help"):
        user_query = user_query.split()
        print_available_methods(user_query[1])
    else:
        try:
            exec(
                f'''
import justsimplestdb
db = justsimplestdb.Instance("{file_name}", separator="{sep}")
executed_query = db.{user_query}
if executed_query != None:
    print(executed_query)
'''
            )
        except Exception as exception:
            print(exception)
            print()
            print("If you don't know DBMS methods, "+ 'type "?" or "help" for help.')
            print('You can also get help for specific methods, by typing "? <method name>" or "help <method name>"(WITHOUT BRACES)')
