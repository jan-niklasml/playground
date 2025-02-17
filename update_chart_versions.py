from packaging.version import Version
import ruamel.yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
import argparse

def increment_version(version):
    v = Version(version)
    return f"{v.major}.{v.minor}.{v.micro + 1}"

parser = argparse.ArgumentParser(description='Upgrade Versions')
parser.add_argument('--appVersion', help='New App-Version')
args = parser.parse_args()

yaml = ruamel.yaml.YAML()
with open("Chart.yaml", "r") as file:
    chart_file_data = yaml.load(file)

chart_file_data["version"] = increment_version(chart_file_data["version"])
chart_file_data["appVersion"] = DoubleQuotedScalarString(args.appVersion)

with open("outputChart.yaml", "w") as file:
    yaml.preserve_quotes = True
    yaml.dump(chart_file_data, file)
