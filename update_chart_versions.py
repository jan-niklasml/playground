from packaging.version import Version
import ruamel.yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
import argparse

def increment_version(version):
    v = Version(version)
    return f"{v.major}.{v.minor}.{v.micro + 1}"

parser = argparse.ArgumentParser(description='Upgrade Versions')
parser.add_argument('--appVersion', help='New App-Version')
parser.add_argument('--pathToChart', help='Path to Chart.yaml')
parser.add_argument('--pathToParentChart', help='Path to parent Chart.yaml')
args = parser.parse_args()

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

with open(args.pathToChart, "r") as file:
    chart_file_data = yaml.load(file)
with open(args.pathToParentChart, "r") as file:
    parent_chart_file_data = yaml.load(file)

if chart_file_data["appVersion"] != args.appVersion:
    chart_file_data["version"] = increment_version(chart_file_data["version"])
    chart_file_data["appVersion"] = DoubleQuotedScalarString(args.appVersion)
    entry_index = parent_chart_file_data["dependencies"].index(next(filter(lambda entry: entry['name'] == chart_file_data["name"], parent_chart_file_data["dependencies"]), None))
    parent_chart_file_data["dependencies"][entry_index]["version"] = chart_file_data["version"]
    parent_chart_file_data["version"] = increment_version(parent_chart_file_data["version"])

with open(args.pathToChart, "w") as file:
    yaml.dump(chart_file_data, file)
with open(args.pathToParentChart, "w") as file:
    yaml.dump(parent_chart_file_data, file)
