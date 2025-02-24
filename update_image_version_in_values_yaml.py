from packaging.version import Version
import ruamel.yaml
import argparse

def increment_version(version):
    v = Version(version)
    return f"{v.major}.{v.minor}.{v.micro + 1}"

parser = argparse.ArgumentParser(description='Upgrade Versions in values.yaml')
parser.add_argument('--pathToValuesYaml', help='Path to values.yaml')
parser.add_argument('--imageTag', help='New Image-Tag')
parser.add_argument('--pathToImageTagField', help='Path to Image-Tag Field in values.yaml file')
parser.add_argument('--pathToChart', help='Path to updated Chart.yaml')
args = parser.parse_args()

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
yaml.indent(offset=2, sequence=4)
yaml.width = 100

# Load values.yaml file
with open(args.pathToValuesYaml, "r") as file:
    values_yaml_data = yaml.load(file)

# Update Image-Tag in values.yaml
keys = args.pathToImageTagField.split('.')
current_value = values_yaml_data
for key in keys[:-1]:
    current_value = current_value.setdefault(key, {})
current_value[keys[-1]] = args.imageTag

# Write data to values.yaml
with open(args.pathToValuesYaml, "w") as file:
    yaml.dump(values_yaml_data, file)

# Load Chart.yaml
with open(args.pathToChart, "r") as file:
    chart_file_data = yaml.load(file)

# Update Chart version
chart_file_data["version"] = increment_version(chart_file_data["version"])

# Write data to Chart.yaml file
with open(args.pathToChart, "w") as file:
    yaml.dump(chart_file_data, file)
