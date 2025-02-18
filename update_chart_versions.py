from packaging.version import Version
import ruamel.yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
import argparse

def increment_version(version):
    v = Version(version)
    return f"{v.major}.{v.minor}.{v.micro + 1}"

parser = argparse.ArgumentParser(description='Upgrade Versions')
parser.add_argument('--appVersion', help='New App-Version')
parser.add_argument('--pathToChart', help='Path to superior Chart.yaml')
parser.add_argument('--pathToBackendChart', help='Path to backend Chart.yaml')
parser.add_argument('--pathToFrontendChart', help='Path to frontend Chart.yaml')
args = parser.parse_args()

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

with open(args.pathToChart, "r") as file:
    chart_file_data = yaml.load(file)
with open(args.pathToBackendChart, "r") as file:
    backend_chart_file_data = yaml.load(file)
with open(args.pathToFrontendChart, "r") as file:
    frontend_chart_file_data = yaml.load(file)

if backend_chart_file_data["appVersion"] != args.appVersion:
    backend_chart_file_data["version"] = increment_version(backend_chart_file_data["version"])
    backend_chart_file_data["appVersion"] = DoubleQuotedScalarString(args.appVersion)
    backend_entry_index = chart_file_data["dependencies"].index(next(filter(lambda entry: entry['name'] == 'backend', chart_file_data["dependencies"]), None))
    chart_file_data["dependencies"][backend_entry_index]["version"] = backend_chart_file_data["version"]
    
if frontend_chart_file_data["appVersion"] != args.appVersion:
    frontend_chart_file_data["version"] = increment_version(frontend_chart_file_data["version"])
    frontend_chart_file_data["appVersion"] = DoubleQuotedScalarString(args.appVersion)
    frontend_entry_index = chart_file_data["dependencies"].index(next(filter(lambda entry: entry['name'] == 'frontend', chart_file_data["dependencies"]), None))
    chart_file_data["dependencies"][frontend_entry_index]["version"] = frontend_chart_file_data["version"]

with open(args.pathToChart, "w") as file:
    yaml.dump(chart_file_data, file)
with open(args.pathToBackendChart, "w") as file:
    yaml.dump(backend_chart_file_data, file)
with open(args.pathToFrontendChart, "w") as file:
    yaml.dump(frontend_chart_file_data, file)
