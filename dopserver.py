from datetime import datetime
import os
import json
import xml.etree.ElementTree as ET


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def insert_node(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert_node(root.left, key)
    else:
        root.right = insert_node(root.right, key)
    return root


def build_binary_tree(data):
    root = None
    for num in data:
        root = insert_node(root, num)
    return root


def create_folder():
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    folder_name = f"{current_time}"
    os.makedirs(folder_name)
    return folder_name


def save_data(number, folder_name, format):
    data = [number]

    file_name = f"{len(os.listdir(folder_name)) + 1}.{format}"
    if format == 'json':
        with open(os.path.join(folder_name, file_name), 'w') as file:
            json.dump(data, file)
    elif format == 'xml':
        root = ET.Element("data")
        for num in data:
            ET.SubElement(root, "number").text = str(num)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(folder_name, file_name), encoding='utf-8', xml_declaration=True)


def tree_to_dict(node):
    if node is None:
        return None
    return {
        'key': node.key,
        'left': tree_to_dict(node.left),
        'right': tree_to_dict(node.right)
    }


def save_tree(root, folder_name):
    tree_dict = tree_to_dict(root)
    with open(os.path.join(folder_name, "tree.json"), 'w') as file:
        json.dump(tree_dict, file, indent=4)
