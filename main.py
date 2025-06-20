import os
import subprocess
from typing import TextIO
from pathlib import Path



g_build_dir:Path

def make_build_dir() -> None:
    global g_build_dir
    g_build_dir=Path(os.getcwd()) / "build"
    g_build_dir.mkdir(exist_ok=True)


class CompileJob:
    source_file_paths: list[Path]
    output_directory_path: Path

    def __init__(self):
        self.source_file_paths = []

    def add_source_file_path(self, source_file_path: Path) -> None:
        self.source_file_paths.append(source_file_path)

    def set_output_directory_path(self, output_directory_path: Path) -> None:
        self.output_directory_path = output_directory_path

    def print_source_paths(self) -> None:
        for source_file_path in self.source_file_paths:
            print(source_file_path)


class CppCompiler:

    compiler_path:str = \
        "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/cl.exe"
    response_filename:str = "build/CompilerResponseFile.rsp"
    compile_cmd:str = compiler_path + " @" + response_filename

    def __init__(self):
        pass

    @staticmethod
    def write_output_directory(response_file: TextIO, output_directory_path: Path) -> None:
        response_file.write(f'/Fo:"{output_directory_path}/"\n')

    @staticmethod
    def write_source_files(response_file: TextIO, source_file_paths: list[Path]) -> None:
        for source_file_path in source_file_paths:
            response_file.write(f'"{source_file_path}"\n')


    def generate_response_file(self, compile_job: CompileJob) -> None:
        with open(self.response_filename, "wt") as response_file:
            response_file.write('/c\n')
            self.write_output_directory(response_file, compile_job.output_directory_path)
            self.write_source_files(response_file, compile_job.source_file_paths)


    def compile(self, compile_job: CompileJob) -> None:
        self.generate_response_file(compile_job)
        #print(self.compile_cmd)
        completed_process  = subprocess.run(self.compile_cmd,
                                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))




class StaticLibrarian:

    librarian_path:str = \
        "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/lib.exe"
    response_filename:str = "build/LibrarianResponseFile.rsp"
    librarian_cmd:str = librarian_path + " @" + response_filename

    def __init__(self):
        pass

    @staticmethod
    def write_output_library_name(response_file: TextIO):
        response_file.write('/OUT:"build/StaticLib.lib"\n')

    @staticmethod
    def write_input_obj_names(response_file: TextIO):
        response_file.write('"build/StaticLibCode.obj"\n')

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
    response_filename = "build/DllLinkerResponseFile.rsp"
    dll_link_cmd:str = dll_linker_path + " @" + response_filename

    def __init__(self):
        pass

    @staticmethod
    def write_dll_output_filename(response_file: TextIO):
        response_file.write('/OUT:"build/Dll.dll"\n')

    @staticmethod
    def write_input_obj_filenames(response_file: TextIO):
        response_file.write('"build/DllCode.obj"\n')

    @staticmethod
    def write_standard_lib_filenames(response_file: TextIO):
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
    response_filename = "build/ExeLinkerResponseFile.rsp"
    exe_link_cmd:str = exe_linker_path + " @" + response_filename

    def __init__(self):
        pass

    @staticmethod
    def write_exe_output_filename(response_file: TextIO):
        response_file.write('/OUT:"build/Main.exe"\n')

    @staticmethod
    def write_input_obj_filenames(response_file: TextIO):
        response_file.write('"build/Main.obj"\n')

    @staticmethod
    def write_standard_lib_filenames(response_file: TextIO):
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
    print("current working directory: " + os.getcwd())
    p:Path = Path(os.getcwd())

    make_build_dir()
    compile_job = CompileJob()
    compile_job.add_source_file_path(Path("Main.cpp"))
    compile_job.add_source_file_path(Path("StaticLibCode.cpp"))
    compile_job.add_source_file_path(Path("DllCode.cpp"))
    compile_job.set_output_directory_path(Path("build/"))
    compile_job.print_source_paths()

    cpp_compiler = CppCompiler()
    cpp_compiler.compile(compile_job)
    static_librarian = StaticLibrarian()
    static_librarian.make_static_lib()
    dll_linker = DllLinker()
    dll_linker.link()
    exe_linker = ExeLinker()
    exe_linker.link()


if __name__ == "__main__":
    main()