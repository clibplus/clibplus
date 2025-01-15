#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <str.h>
#include <arr.h>
#include <map.h>

#include "OS/utils.h"

typedef struct Package {
    String      Name;
    String      Filepath;
    String      Lib;
    String      Header;
    int         SubLib;

    void        *Handler;
} Package;

#define CLIB_ORG "https://github.com/orgs/clibplus"
#define CLIB_REPO_LIST "https://github.com/orgs/clibplus/repositories"

void *BUILT_IN[] = {
    "str", "arr", "map",        // Builtin Libs
    "OS", "Net", NULL           // External Sub-Libs
};

Array Retrieve_Installed_Libs() {

}

int main() {
    return 0;
}