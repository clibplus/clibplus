import sys, os, requests, subprocess

HELP_BANNER = rf"""
        cLib+ Package Manager | v0.0.1 [BETA]
Usage: {sys.argv[0]} [OPTIONS]....

   Flag            Description
______________________________________________
   -l             List of cLib+ sub-pkg and sub-libs
   -i             Install a cLib+ sub-pkg or sub-library
"""

ORG_URL = "https://github.com/orgs/clibplus"
REPO_LIST_URL = "https://github.com/orgs/clibplus/repositories"

cLib_DefaultPkgs = {
	"String": ["libstr.a", "str.h"],
	"Array": ["libarr.a", "arr.h"],
	"Map": ["libmap.a", "arr.h"],
	"OS": {
		"File": ["OS/libfile.a", "OS/file.h"]
	}
}

class cLibPkgManager():
	def __init__(self):
		self.RepoList 		= []
		self.InstalledPkgs 	= []
		self.get_installed_pkgs()
		self.get_repo_list()

	""" Get the installed clib sub-libs """
	def get_installed_pkgs(self) -> None:

		# check for libs
		for pkg in cLib_DefaultPkgs:
			if isinstance(cLib_DefaultPkgs[pkg], list):
				if os.path.exists(f"/usr/local/lib/{cLib_DefaultPkgs[pkg][0]}") and os.path.exists(f"/usr/local/include/{cLib_DefaultPkgs[pkg][1]}"):
					print(f"[ + ] Found installed clibs sub-lib {pkg}....!")
					self.InstalledPkgs.append(pkg)
			elif isinstance(cLib_DefaultPkgs[pkg], dict):
				for sub_pkg in cLib_DefaultPkgs[pkg]:
					if os.path.exists(f"/usr/local/lib/{cLib_DefaultPkgs[pkg][sub_pkg][0]}") and os.path.exists(f"/usr/local/include/{cLib_DefaultPkgs[pkg][sub_pkg][1]}"):
						print(f"[ + ] Found installed clibs sub-lib {sub_pkg}....!")
						self.InstalledPkgs.append(sub_pkg)

	""" Get the list of repo from github organization """
	def get_repo_list(self) -> None:
		req = requests.get(REPO_LIST_URL)
		if req.status_code != 200:
			print(f"[ x ] Error, Unable to connect to github...!\n")
			return

		resp = req.text.split(">")
		for line in resp:
			if "<a class=\"Text__StyledText-sc-17v1xeu-0 hWqAbU TitleHeader-module__inline--rL27T Title-module__anchor--SyQM6\"" in line:
				self.RepoList.append(line.split(" ")[6].replace("href=", "").replace("\"", ""))

	def is_lib_installed(self, q: str) -> bool:
		for arg in self.InstalledPkgs:
			if arg == q:
				return True

		return False

	def search_lib_in_repo(self, q: str):
		for lib in self.RepoList:
			if lib.endswith(q):
				print(lib)
				return True, lib

		return False, ""

	def install_lib(self, sub: str) -> bool:
		sub_name = sub.split("/")[len(sub.split("/")) - 1]
		os.system(f"git clone https://github.com{sub}")

		file_count = int(subprocess.getoutput(f"ls {sub_name}/*.c | wc -l").split(" ")[0])
		files = os.listdir(sub_name)

		if file_count > 1:
			os.system(f"mkdir /usr/local/include/{sub_name}")
			os.system(f"cp {sub_name}/*.h /usr/local/include/{sub_name}")

		for file in files:
			if ".c" in file:
				name = file.replace(".c", "")
				os.system(f"gcc -c {sub_name}/{file}")
				os.system(f"ar rcs {name}.a {name}.o; rm {name}.o; mv {name}.a /usr/local/lib/lib{name}.a")

		os.system("sudo ldconfig")

def get_flag_value(args: list, idx: int) -> str:
	if idx + 1 >= len(args):
		return "[ x ] Error, Invalid argument provided....! Use '--help' for a list of commands"

	return args[idx + 1]

if len(sys.argv) < 2:
	print(f"[ x ] Error, Invalid arguments provided...!\n{HELP_BANNER}")
	exit(0)

pkg_mgr = cLibPkgManager()
i = 0
for arg in sys.argv:
	if arg == "--help":
		print(HELP_BANNER)
		exit(0)
	elif arg == "-i":
		v = get_flag_value(sys.argv, i)
		if "[ x ]" in v:
			print(v)
			exit(0)

		chk = pkg_mgr.is_lib_installed(v)
		if chk:
			print("[ - ] This lib is already installed...!")
			exit(0)

		chk, lib = pkg_mgr.search_lib_in_repo(v)
		if chk == False:
			print(f"[ x ] Lib: {v} was not found...!\n")
			exit(0)
			
		pkg_mgr.install_lib(lib)

	i += 1
