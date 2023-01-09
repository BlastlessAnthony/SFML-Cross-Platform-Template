import os, sys, fnmatch, platform, subprocess, time

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


CPreprocessorFlags: list[str] = ["-std=c++11", "-Wall", "-Wpedantic", "-Wextra"]
CFlags: list[str] = []
LibraryDirectories: list[str] = []
Libraries: list[str] = []
FrameworkDirectories: list[str] = []
Frameworks: list[str] = []
LinkerFlags: list[str] = []
################################################################################
#### Build Configuration
################################################################################

#Windows
if platform.system() == "Windows":

    if BuildArchitechure.upper() == "32BIT":

        Compiler = f'{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}Compilers{PATH_SEPARATOR}MinGW{PATH_SEPARATOR}bin{PATH_SEPARATOR}g++.exe'
        Includes += []
        LibraryDirectories += [f'{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86{PATH_SEPARATOR}External']
        Libraries += ["flac", "freetype", "ogg", "openal32", "vorbis", "vorbisenc", "vorbisfile"]
        CFlags += []

        if BuildType.upper() == "RELEASE":

            LibraryDirectories += [
                f'{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86{PATH_SEPARATOR}Release'
            ]

            Libraries += [
                "sfml-graphics", "sfml-window", 
                "sfml_system", "sfml-audio", 
                "sfml-network"
            ]

        elif BuildType.upper() == "DEBUG":

            LibraryDirectories += [
                f'{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86{PATH_SEPARATOR}Debug'
            ]

            Libraries += [
                "sfml-graphics-d", "sfml-window-d", 
                "sfml_system-d", "sfml-audio-d", 
                "sfml-network-d"
            ]
        else:
            print(f"A fatal error has occured, BuildType was set to {BuildType} and not RELEASE or DEBUG (non-case sensitive) which is not valid.")

    elif BuildArchitechure.upper() == "64BIT":
        Compiler = f'{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}Compilers{PATH_SEPARATOR}MinGW64{PATH_SEPARATOR}bin{PATH_SEPARATOR}g++.exe'
        Includes += []
        LibraryDirectories += [f'{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86_64{PATH_SEPARATOR}External']
        Libraries += ["flac", "freetype", "ogg", "openal32", "vorbis", "vorbisenc", "vorbisfile"]
        CFlags += []

        if BuildType.upper() == "RELEASE":

            LibraryDirectories += [
                f'{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86_64{PATH_SEPARATOR}Release'
            ]

            Libraries += [
                "sfml-graphics", "sfml-window", 
                "sfml_system", "sfml-audio", 
                "sfml-network"
            ]

        elif BuildType.upper() == "DEBUG":

            LibraryDirectories += [
                f"{WORKING_DIRECTORY}{PATH_SEPARATOR}Dependencies{PATH_SEPARATOR}SFML{PATH_SEPARATOR}Windows{PATH_SEPARATOR}x86_64{PATH_SEPARATOR}Debug"
            ]

            Libraries += [
                "sfml-graphics-d", "sfml-window-d", 
                "sfml_system-d", "sfml-audio-d", 
                "sfml-network-d"
            ]

        else:
            print(f"A fatal error has occured, BuildType was set to {BuildType} and not RELEASE or DEBUG (non-case sensitive) which is not valid.")
            exit(1)
    else:
        print(f"A fatal error has")

elif platform.system == "Darwin":
    Compiler = f'clang++'
    Includes += []
    LibraryDirectories += []
    Libraries += []
    CFlags += []

    if BuildType.upper() == "RELEASE":

        LibraryDirectories += []
        Libraries += []

    elif BuildType.upper() == "DEBUG":

        LibraryDirectories += []
        Libraries += []

    else:
        print(f"A fatal error has occured, BuildType was set to {BuildType} and not RELEASE or DEBUG (non-case sensitive) which is not valid.")
        exit(1)
else:
    print("Your operating system is not supported. Please add support for other operating systems if needed.")
    exit(1)

################################################################################
#### Final Setup
################################################################################
BuildDirectory = f'{BuildRootDirectory}{PATH_SEPARATOR}'
BinaryDirectory = f"{BinaryRootDirectory}{PATH_SEPARATOR}"

if platform.system == "Windows":
    ExecutableName = f'{ProjectName}.exe'

if platform.system != "Darwin":
    if BuildArchitechure.upper() == "32BIT":
        CFlags += ['-m32']
    elif BuildArchitechure.upper() == "64BIT":
        CFlags += ['-m64']
    else:
        print("")
        exit(1)

    if BuildArchitechure.upper() == '32BIT':
        BuildDirectory = f'{BuildDirectory}x86{PATH_SEPARATOR}'
        BinaryDirectory = f'{BinaryDirectory}x86{PATH_SEPARATOR}'
    elif BuildArchitechure.upper() == '64BIT':
        BuildDirectory = f'{BuildDirectory}x86_64{PATH_SEPARATOR}'
        BinaryDirectory = f'{BinaryDirectory}x86_64{PATH_SEPARATOR}'
    
if BuildType.upper() == 'RELEASE':
    BuildDirectory = f'{BuildDirectory}Release'
    BinaryDirectory = f'{BinaryDirectory}Release'
    CFlags += ['-O3']
    CPreprocessorFlags += ['-DNDEBUG']
elif BuildType.upper() == 'DEBUG':
    BuildDirectory = f'{BuildDirectory}Debug'
    BinaryDirectory = f'{BuildDirectory}Debug'
    CFlags += ['-O0']
else:
    print("")
    exit(1)

linkerArguments: str = ""
for libdir in LibraryDirectories:
    linkerArguments += f' -L"{libdir}"'

for lib in Libraries:
    linkerArguments += f' -l"{lib}"'

compilerArguments: str = ''
for flag in CFlags:
    compilerArguments += f' {flag}'

for ppflag in CPreprocessorFlags:
    compilerArguments += f' {ppflag}'

Objects: list[str] = []

for source in Sources:
    s = source.replace(f'{SourceDirectory}', f'{BuildDirectory}')
    Objects.append(s.replace(".cpp", ".o"))

#print(Objects)

def mkdir(path: str) -> bool:
    import os
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        del os
        return True
    else:
        del os
        return False

if not os.path.isdir(f'{BuildDirectory}'):
    mkdir(f'{BuildDirectory}')



for _i in range(len(Sources)):
    print(f'"{Compiler}" -c "{Sources[_i]}" {compilerArguments} -o "{Objects[_i]}"')
    subprocess.run(f'"{Compiler}" -c "{Sources[_i]}" {compilerArguments} -o "{Objects[_i]}"')
    time.sleep(4)