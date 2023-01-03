import os, sys, fnmatch, platform

if len(sys.argv) <= 1:
    s = """
You need to launch this Python script with the command line arguments.

build.py build_type build_arch

Example:
python3 build.py release 32-bit
    """
    print(s)
    exit(1)

from pathlib import Path
WORKING_DIRECTORY: str = Path(__file__).parent.absolute()
os.chdir(WORKING_DIRECTORY)
PATH_SEPARATOR: str = os.path.sep

################################################################################
#### Project Configuration
################################################################################
ProjectName: str = "SFMLApplication"
ExecutableName: str = ""
BuildType: str = ""
BuildArchitechure: str
SourceDirectory: str = f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Source"
IncludeDirectory: str = f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Source{PATH_SEPARATOR}Include"

BuildRootDirectory: str = f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Build"
BuildDirectory: str = ""
BinaryRootDirectory: str = f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Binary"
BinaryDirectory: str = ""
AssetsDirectory: str = f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Assets"


#Other
if len(sys.argv) > 1:
    BuildType = sys.argv[1]
    if BuildType.upper() != "RELEASE" and BuildType.upper() != "DEBUG":
        print("Please choose a build type of either Release or Debug (non-case sensitive)")
        exit(1)
    if len(sys.argv) > 2:
        BuildArchitechure = sys.argv[2]
        if BuildArchitechure.upper() != "32BIT" and BuildArchitechure.upper() != "64BIT":
            print(f"Build architecture is not set to a valid value ('32BIT' or '64BIT' non-case sensitive) so it has been defaulted to {platform.architecture()[0]}.")
            BuildArchitechure = platform.architecture()[0]
    else:
        BuildArchitechure = platform.architecture()[0]
else:
    exit(1)
################################################################################
#### Functions
################################################################################
def find(pattern: str, path: str):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def find_all(name: str, path: str):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

################################################################################
#### Compiler Configuration
################################################################################
Compiler: str = ""

Sources: list[str] = find("*.cpp", f"{SourceDirectory}")
Includes: list[str] = [
    f"{IncludeDirectory}",
    f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}include"
]
LinkerLibraries: list[str] = []

CPreprocessorFlags: list[str] = ["-std=c++11", "-Wall", "-Wpedantic", "-Wextra"]
CFlags: list[str] = []
LinkerLibrariesDirectories: list[str] = []
LinkerFlags: list[str] = []
################################################################################
#### Build Configuration
################################################################################

#Windows
if platform.system() == "Windows":

    if BuildArchitechure.upper() == "32BIT":

        Compiler = f"g++.exe"
        Includes += []
        LinkerLibrariesDirectories += [f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86{PATH_SEPARATOR}External"]
        LinkerLibraries += ["flac", "freetype", "ogg", "openal32", "vorbis", "vorbisenc", "vorbisfile"]
        CFlags += []

        if BuildType.upper() == "RELEASE":

            LinkerLibrariesDirectories += [
                f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86{PATH_SEPARATOR}Release"
            ]

            LinkerLibraries += [
                "sfml-graphics", "sfml-window", 
                "sfml_system", "sfml-audio", 
                "sfml-network"
            ]

        elif BuildType.upper() == "DEBUG":

            LinkerLibrariesDirectories += [
                f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86{PATH_SEPARATOR}Debug"
            ]

            LinkerLibraries += [
                "sfml-graphics-d", "sfml-window-d", 
                "sfml_system-d", "sfml-audio-d", 
                "sfml-network-d"
            ]

        else:
            print(f"A fatal error had occured, BuildType was set to {BuildType} and not RELEASE or DEBUG (non-case sensitive) which is not valid.")
            exit(1)
else:
    print("")
    exit(1)

args: str = ""
for libdir in LinkerLibrariesDirectories:
    args += f' -L"{libdir}"'

for lib in LinkerLibraries:
    args += f'  -l"{lib}"'

os.system(f"g++ {args}")