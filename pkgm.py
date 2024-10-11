import requests

URL = "https://github.com/orgs/clibplus/repositories"

def get_repo_list() -> str | None:
	req = requests.get(URL)
	if req.status_code != 200:
		print(f"[ x ] Error, Unable to connect to github...!\n")
		return None

	resp = req.text
	lines = resp.split("\n")
	for line in lines:
		if "href=\"clibplus/" in line:
			print(f"{line}")

get_repo_list()
