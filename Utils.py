import os

def read_datasheet_contents():
    folder_path = './Data/Datasheet'
    datasheet_contents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                datasheet_contents.append(content)
    return datasheet_contents
