"""
		[ Temporary Quick cLib+ Package Manager Write Up ]

	@author: algo1337
	@since: 4/11/24
"""
import sys, os, requests, subprocess, time

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
	"str": "str",
	"Array": "arr",
	"Map": "map",
	"OS": {
		"file": "file",
		"utils": "utils"
	},
	"Net": {
		"socket": "socket"
	}
}

class Package():
	def __init__(self, PKG: str, name: str):
		self.FileName 		= name
		self.SubName 		= PKG
		self.LibName 		= f"lib{name}.a"
		self.HeaderName 	= f"{name}.h"
		self.SubPKG 		= False

		if PKG: 
			self.SubPKG = True

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
			if isinstance(cLib_DefaultPkgs[pkg], dict):
				for sub_pkg in cLib_DefaultPkgs[pkg]:
					package = Package(pkg, cLib_DefaultPkgs[pkg][sub_pkg])
					if os.path.exists(f"/usr/local/lib/{package.SubName}/{package.LibName}") and os.path.exists(f"/usr/local/include/{package.SubName}/{package.HeaderName}"):
						self.InstalledPkgs.append(package)
				continue

			package = Package(None, cLib_DefaultPkgs[pkg])
			if os.path.exists(f"/usr/local/lib/{package.LibName}") and os.path.exists(f"/usr/local/include/{package.HeaderName}"):
				self.InstalledPkgs.append(package)

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

	""" Ckeck for all installed libs """
	def is_lib_installed(self, q: str) -> bool:
		for arg in self.InstalledPkgs:
			if arg.FileName != None:
				if q == arg.FileName:
					return True

			if arg.SubName != None:
				if q in arg.SubName:
					return True

		return False

	""" CHeck for all libs on the org repo list"""
	def search_lib_in_repo(self, q: str):
		for lib in self.RepoList:
			if lib.endswith(q):
				return True, lib

		return False, ""

	def install_lib(self, sub: str) -> bool:
		sub_name = sub.split("/")[len(sub.split("/")) - 1]
		subprocess.getoutput(f"git clone https://github.com{sub}")

		file_count = int(subprocess.getoutput(f"ls {sub_name}/*.c | wc -l").split(" ")[0])
		if file_count == 0:
			print("[ x ] Error, Unable to find C Files...!")
			exit(0)

		files = os.listdir(sub_name)

		if file_count > 1:
			subprocess.getoutput(f"mkdir /usr/local/include/{sub_name}")
			subprocess.getoutput(f"mkdir /usr/local/lib/{sub_name}")
			subprocess.getoutput(f"cp {sub_name}/*.h /usr/local/include/{sub_name}/")

		for file in files:
			if ".c" in file:
				name = file.replace(".c", "")
				if file_count == 1:
					self.add_to_local_path(sub_name, name)
				else:
					self.add_to_path(sub_name, name)

		subprocess.getoutput("sudo ldconfig")
		subprocess.getoutput(f"rm -rf {sub_name}")

	def add_to_local_path(self, sub_name: str, name: str) -> None:
		subprocess.getoutput(f"gcc -c {sub_name}/{name}.c")
		subprocess.getoutput(f"ar rcs {name}.a {name}.o; rm {name}.o; mv {name}.a /usr/local/lib/lib{name}.a; mv {sub_name}/{name}.h /usr/local/include/")


	def add_to_path(self, sub_name: str, name: str) -> None:
		subprocess.getoutput(f"gcc -c {sub_name}/{name}.c")
		subprocess.getoutput(f"ar rcs {name}.a {name}.o; rm {name}.o; mv {name}.a /usr/local/lib/{sub_name}/lib{name}.a; mv {sub_name}/{name}.h /usr/local/include/{sub_name}/{name}.h")

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
	elif arg == "-l":
		i = 0
		for pkg in pkg_mgr.InstalledPkgs:
			if pkg.SubName:
				print(f"[{i}]: {pkg.SubName}/{pkg.HeaderName}")
			else:
				print(f"[{i}]: {pkg.HeaderName}")

			i += 1
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
		print(f"[ + ] Lib: {v} was successfully installed")

	elif arg == "-r":
		for repo in pkg_mgr.RepoList:
			print(f"Repo: {repo}")


	i += 1
