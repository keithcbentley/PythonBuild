import os
import subprocess
from typing import TextIO
from pathlib import Path

def generate_cpp_source_filenames():
    pass

def figure_project_base_directory():
    # check for given directory
    # check for current working directory
    # check that project file exists
    # check that any auxilliary files exist
    pass

class Compiler:

    compiler_path:str = \
        "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/cl.exe"
    response_filename:str = "c:/CppTestFile/build/CompilerResponseFile.rsp"
    compile_cmd:str = compiler_path + " @" + response_filename

    def __init__(self):
        pass

    def write_output_directory(self, response_file: TextIO):
        response_file.write('/Fo:"c:/CppTestFile/build/"\n')

    def write_source_files(self, response_file: TextIO):
        response_file.write('"c:/CppTestFile/Main.Cpp"\n')
        response_file.write('"c:/CppTestFile/StaticLibCode.Cpp"\n')
        response_file.write('"c:/CppTestFile/DllCode.Cpp"\n')


    def generate_response_file(self):
        with open(self.response_filename, "wt") as response_file:
            response_file.write('/c\n')
            self.write_output_directory(response_file)
            self.write_source_files(response_file)


    def compile(self):
        self.generate_response_file()
        #print(self.compile_cmd)
        completed_process  = subprocess.run(self.compile_cmd,
                                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))


class CompileJob:
    def __init__(self):
        pass



class StaticLibrarian:

    librarian_path:str = \
        "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/lib.exe"
    response_filename:str = "c:/CppTestFile/build/LibrarianResponseFile.rsp"
    librarian_cmd:str = librarian_path + " @" + response_filename

    def __init__(self):
        pass

    def write_output_library_name(self, response_file: TextIO):
        response_file.write('/OUT:"c:/CppTestFile/build/StaticLib.lib"\n')

    def write_input_obj_names(self, response_file: TextIO):
        response_file.write('"c:/CppTestFile/build/StaticLibCode.obj"\n')

    def generate_response_file(self):
        with open(self.response_filename, "wt") as response_file:
            self.write_input_obj_names(response_file)
            self.write_output_library_name(response_file)

    def make_static_lib(self):
        self.generate_response_file()
        #print(self.librarian_cmd)
        completed_process  = subprocess.run(self.librarian_cmd,
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))


class DllLinker:
    dll_linker_path:str = \
        "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/link.exe"
    response_filename = "c:/CppTestFile/build/DllLinkerResponseFile.rsp"
    dll_link_cmd:str = dll_linker_path + " @" + response_filename

    def __init__(self):
        pass

    def write_dll_output_filename(self, response_file: TextIO):
        response_file.write('/OUT:"c:/CppTestFile/build/Dll.dll"\n')

    def write_input_obj_filenames(self, response_file: TextIO):
        response_file.write('"c:/CppTestFile/build/DllCode.obj"\n')

    def write_standard_lib_filenames(self, response_file: TextIO):
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/lib/libcmt.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/lib/oldnames.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/lib/libvcruntime.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/SDK/lib/kernel32.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/SDK/lib/libucrt.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/SDK/lib/uuid.lib"\n')


    def generate_response_file(self):
        with open(self.response_filename, "wt") as response_file:
            response_file.write('/DLL\n')
            self.write_dll_output_filename(response_file)
            self.write_input_obj_filenames(response_file)
            self.write_standard_lib_filenames(response_file)


    def link(self):
        self.generate_response_file()
        #print(self.dll_link_cmd)
        completed_process  = subprocess.run(self.dll_link_cmd,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))



class ExeLinker:
    exe_linker_path:str = \
        "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/link.exe"
    response_filename = "c:/CppTestFile/build/ExeLinkerResponseFile.rsp"
    exe_link_cmd:str = exe_linker_path + " @" + response_filename

    def __init__(self):
        pass

    def write_exe_output_filename(self, response_file: TextIO):
        response_file.write('/OUT:"c:/CppTestFile/build/Main.exe"\n')

    def write_input_obj_filenames(self, response_file: TextIO):
        response_file.write('"c:/CppTestFile/build/Main.obj"\n')

    def write_standard_lib_filenames(self, response_file: TextIO):
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/lib/libcmt.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/lib/oldnames.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/lib/libvcruntime.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/SDK/lib/kernel32.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/SDK/lib/libucrt.lib"\n')
        response_file.write(
            '"c:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/SDK/lib/uuid.lib"\n')

    def generate_response_file(self):
        with open(self.response_filename, "wt") as response_file:
            self.write_exe_output_filename(response_file)
            self.write_input_obj_filenames(response_file)
            self.write_standard_lib_filenames(response_file)

    def link(self):
        self.generate_response_file()
#        print(self.exe_link_cmd)
        completed_process  = subprocess.run(self.exe_link_cmd,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))


def main():
    compiler = Compiler()
    compiler.compile()
    static_librarian = StaticLibrarian()
    static_librarian.make_static_lib()
    dll_linker = DllLinker()
    dll_linker.link()
    exe_linker = ExeLinker()
    exe_linker.link()
    print("current working directory: " + os.getcwd())
    p:Path = Path(os.getcwd())
    print(" p: ", p, "  is_dir:", p.is_dir(), "  is_file:", p.is_file())
    print("drive: ", p.drive)
    print("root: ", p.root)
    print("anchor: ", p.anchor)
    print("parent: ", p.parent)
    print("name: ", p.name)
    print("suffix: ", p.suffix)
    print("stem: ", p.stem)
    print("is_absolute(): ", p.is_absolute())


if __name__ == "__main__":
    main()