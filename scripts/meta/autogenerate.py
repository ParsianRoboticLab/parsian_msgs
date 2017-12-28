#!/usr/bin/env python3.5

import pystache
import datetime
import os
import re

PARSIAN_TYPE_MAP = {
    "bool": "bool",
    "uint8": "unsigned char",
    "int8": "char",
    "uint16": "unsigned short",
    "int16": "short",
    "uint32": "unsigned int",
    "int32": "int",
    "uint64": "unsigned long",
    "int64": "long",
    "float32": "float",
    "float64": "double",
    "string": "std::string",
    "enum": "enum",
    "vector2D": "Vector2D",
    "parsian_msgs/vector2D": "Vector2D",
    "parsian_msgs/parsian_skill_gotoPoint": 'gotoPoint'
}

PARSIAN_DEFAULT_VALUE_MAP = {
    "bool": " = false",
    "unsigned char": " = 0",
    "char": " = 0",
    "unsigned short": " = 0",
    "short": " = 0",
    "unsigned int": " = 0",
    "int": " = 0",
    "unsigned long": " = 0",
    "long": " = 0",
    "float": " = 0.0",
    "double": " = 0.0",
    "std::string": " = \"\"",
    "enum": " = 0",
    "Vector2D": ".assign(5000,5000)"
}

PARSIAN_PROPERTIES_LIST = ["Vector2D"]

min_max_regex = re.compile('\[([0-9\.\-]+)\:([0-9\.\-]+)\]')
rend = pystache.Renderer()


def strip_text(text):
    return re.sub("\s\s+", " ", text.strip().replace('\n', '').replace('\r', '')).replace('"', '').replace("'", "")


def cap_word(text):
    return text.lower().title()


def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def convert_property(ros_property):
    print('type : ' + ros_property[0], 'name :' + ros_property[1])
    if str(ros_property[0]).endswith('[]'):
        return "std::list<" + PARSIAN_TYPE_MAP.get(ros_property[0][:-2]) + ">", ros_property[1]
    else:
        return PARSIAN_TYPE_MAP.get(ros_property[0]), ros_property[1]


def get_fulldict(file, properties_list):
    action_name = file.split('.')[0].split('_')
    if len(action_name):
        action_name = cap_word(action_name[len(action_name) - 1]) + 'Action'
    print(action_name)

    print(file.split('.')[0])
    new_dict = {"action_name": action_name,
                "has_base": False,
                "base_message": '',
                "properties": [],
                "parsian_properties": [],
                "list_properties": [],
                "message": file.split('.')[0],
                "file_name": action_name.lower()
                }

    # message name
    for m_property in properties_list:
        if str(m_property[1]) == 'base':
            new_dict["has_base"] = True
            new_dict["base_action"] = cap_word(m_property[0].replace('parsian_msgs/', '')) + 'Action'
            new_dict["base_action_file"] = str(new_dict["base_action"]).lower() + '.h'
            new_dict["base_message"] = "parsian_skill_" + str(m_property[0].replace('parsian_msgs/', ''))
        else:
            p = {"type": m_property[0], "name": m_property[1].title(), "local": m_property[1]}
            if m_property[0] in PARSIAN_DEFAULT_VALUE_MAP.keys():
                p["default_value"] = PARSIAN_DEFAULT_VALUE_MAP[m_property[0]]
            if m_property[0] in PARSIAN_PROPERTIES_LIST:
                new_dict['parsian_properties'].append(p)
            elif m_property[0].endswith('>'):
                p["m_type"] = m_property[0][10:-1]
                new_dict['list_properties'].append(p)
            else:
                new_dict['properties'].append(p)
    print(new_dict)
    return new_dict


def generate_actions(folder):
    # Clean Out Folder
    if os.path.isdir(os.getcwd() + os.sep + 'out'):
        for f in os.listdir(os.path.join(os.getcwd(), 'out')):
            os.remove(os.getcwd() + os.sep + 'out' + os.sep + f)
    else:
        os.mkdir(os.getcwd() + os.sep + 'out')

    for m_file in os.listdir(folder):

        if m_file.startswith('parsian_skill_'):
            ros_property_list = []
            with open(os.path.join(folder, m_file)) as msg:
                for line in msg.readlines():
                    line = line.replace("\n", '')
                    ros_property_list.append(tuple(line.split(' ')))
                parsian_property_list = [convert_property(ros_property) for ros_property in ros_property_list if
                                         len(ros_property) is 2]
                parsian_dict = get_fulldict(m_file, parsian_property_list)

            with open("out/" + parsian_dict['action_name'].lower() + '.h', "w") as f:
                f.write(rend.render_path('templates/action.h.mustache', parsian_dict))

            with open("out/" + parsian_dict['action_name'].lower() + '.cpp', "w") as f:
                f.write(rend.render_path('templates/action.cpp.mustache', parsian_dict))
                # print(rend.render_path('templates/action.h.mustache', parsian_dict))
                # print(file)


def main():
    # Setup stuff
    if os.getcwd().endswith('/parsian_ssl/parsian_msgs/scripts/meta') is False:
        print("Please run script on /scripts/meta folder")
        exit(1)

    generate_actions(os.pardir + os.sep + os.pardir + os.sep + 'msg')


if __name__ == "__main__":
    main()
