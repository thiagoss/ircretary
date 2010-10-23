def get_properties():
    property_file = open('config.properties', 'r')
    properties_str = property_file.readlines()
    properties = {}
    for property_line in properties_str:
        values = property_line.split('=')
        key, value = values[0].strip(), values[1].strip()
        if key == "channels":
            value = [val.strip() for val in value.split(',')]
        properties.update({key:value})
    return properties
    
print get_properties()
