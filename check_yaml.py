import yaml

with open("changelog.yaml") as f:
    data = yaml.safe_load(f)

print(data["product"], data["release"])
for change in data["changes"]:
    print(change["id"], "|", change["title"], "|", change["visibility"])