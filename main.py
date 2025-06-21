import os
import subprocess
from typing import TextIO
from pathlib import Path


g_src_root_dir_name:str = "src"
g_build_root_dir_name:str = "build"

def is_relative(path:Path) -> bool:
    return not path.is_absolute()


class ProjectRoot:

    def __init__(self) -> None:
        self.m_project_root_dir_path: Path = Path(os.getcwd())

        self.m_src_root_dir_path: Path= Path(g_src_root_dir_name)
        if is_relative(self.m_src_root_dir_path):
            self.m_src_root_dir_path = self.m_project_root_dir_path / self.m_src_root_dir_path

        self.m_build_root_dir_path: Path = Path(g_build_root_dir_name)
        if is_relative(self.m_build_root_dir_path):
            self.m_build_root_dir_path = self.m_project_root_dir_path / self.m_build_root_dir_path

        print("project root: " + str(self.m_project_root_dir_path))
        print("src root: " + str(self.m_src_root_dir_path))
        print("build root: " + str(self.m_build_root_dir_path))

        self.m_build_root_dir_path.mkdir(exist_ok=True)


g_project_root: ProjectRoot = ProjectRoot()


class CompileJob:

    def __init__(self) -> None:
        self.m_source_file_paths: list[Path] = []
        self.m_output_directory_path: Path = Path()

    def add_source_file_path(self, source_file_path: Path) -> None:
        self.m_source_file_paths.append(source_file_path)

    def set_output_directory_path(self, output_directory_path: Path) -> None:
        self.m_output_directory_path = output_directory_path

    def print_source_paths(self) -> None:
        for source_file_path in self.m_source_file_paths:
            print(source_file_path)


class CppCompiler:

    def __init__(self) -> None:
        self.m_compiler_path: str = \
            "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/cl.exe"
        self.m_response_file_name: str = "build/CompilerResponseFile.rsp"
        self.m_compile_cmd: str = self.m_compiler_path + " @" + self.m_response_file_name

    @staticmethod
    def write_output_directory_name(response_file: TextIO, output_directory_path: Path) -> None:
        response_file.write(f'/Fo:"{output_directory_path}/"\n')

    @staticmethod
    def write_source_file_names(response_file: TextIO, source_file_paths: list[Path]) -> None:
        for source_file_path in source_file_paths:
            response_file.write(f'"{source_file_path}"\n')


    def generate_response_file(self, compile_job: CompileJob) -> None:
        with open(self.m_response_file_name, "wt") as response_file:
            response_file.write('/c\n')
            self.write_output_directory_name(response_file, compile_job.m_output_directory_path)
            self.write_source_file_names(response_file, compile_job.m_source_file_paths)


    def compile(self, compile_job: CompileJob) -> None:
        self.generate_response_file(compile_job)
        completed_process  = subprocess.run(
            self.m_compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))


class StaticLibrarianJob:

    def __init__(self) -> None:
        self.m_obj_file_paths: list[Path] = []
        self.m_output_library_path: Path = Path()

    def add_obj_file_path(self, obj_file_path: Path) -> None:
        self.m_obj_file_paths.append(obj_file_path)

    def set_output_library_path(self, output_library_path: Path) -> None:
        self.m_output_library_path = output_library_path


class StaticLibrarian:

    def __init__(self) -> None:
        self.m_librarian_path: str = \
            "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/lib.exe"
        self.m_response_file_name: str = "build/LibrarianResponseFile.rsp"
        self.m_librarian_cmd: str = self.m_librarian_path + " @" + self.m_response_file_name

    @staticmethod
    def write_output_library_name(response_file: TextIO, output_library_path: Path) -> None:
        response_file.write(f'/OUT:"{output_library_path}"\n')

    @staticmethod
    def write_input_obj_names(response_file: TextIO, input_object_file_paths: list[Path]):
        for input_object_file_path in input_object_file_paths:
            response_file.write(f'"{input_object_file_path}"\n')

    def generate_response_file(self, static_lib_job: StaticLibrarianJob) -> None:
        with open(self.m_response_file_name, "wt") as response_file:
            self.write_input_obj_names(response_file, static_lib_job.m_obj_file_paths)
            self.write_output_library_name(response_file, static_lib_job.m_output_library_path)

    def make_static_lib(self, static_lib_job: StaticLibrarianJob) -> None:
        self.generate_response_file(static_lib_job)
        completed_process  = subprocess.run(
            self.m_librarian_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))

class DllLinkJob:

    def __init__(self) -> None:
        self.m_obj_file_paths: list[Path] = []
        self.m_output_dll_path: Path = Path()

    def add_obj_file_path(self, obj_file_path: Path) -> None:
        self.m_obj_file_paths.append(obj_file_path)

    def set_output_dll_path(self, output_dll_path: Path) -> None:
        self.m_output_dll_path = output_dll_path




class DllLinker:

    def __init__(self) -> None:
        self.m_dll_linker_path: str = \
            "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/link.exe"
        self.m_response_file_name: str = "build/DllLinkerResponseFile.rsp"
        self.m_dll_link_cmd: str = self.m_dll_linker_path + " @" + self.m_response_file_name

    @staticmethod
    def write_output_dll_name(response_file: TextIO, output_dll_path: Path) -> None:
        response_file.write(f'/OUT:"{output_dll_path}"\n')

    @staticmethod
    def write_obj_file_names(response_file: TextIO, obj_file_paths: list[Path]):
        for obj_file_path in obj_file_paths:
            response_file.write(f'"{obj_file_path}"\n')

    @staticmethod
    def write_standard_lib_file_names(response_file: TextIO):
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


    def generate_response_file(self, dll_link_job: DllLinkJob) -> None:
        with open(self.m_response_file_name, "wt") as response_file:
            response_file.write('/DLL\n')
            self.write_output_dll_name(response_file, dll_link_job.m_output_dll_path)
            self.write_obj_file_names(response_file, dll_link_job.m_obj_file_paths)
            self.write_standard_lib_file_names(response_file)


    def link(self, dll_link_job: DllLinkJob) -> None:
        self.generate_response_file(dll_link_job)
        completed_process  = subprocess.run(
            self.m_dll_link_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))


class ExeLinkJob:

    def __init__(self) -> None:
        self.m_obj_file_paths: list[Path] = []
        self.m_output_exe_path: Path = Path()

    def add_obj_file_path(self, obj_file_path: Path) -> None:
        self.m_obj_file_paths.append(obj_file_path)

    def set_output_exe_path(self, output_exe_path: Path) -> None:
        self.m_output_exe_path = output_exe_path


class ExeLinker:

    def __init__(self) -> None:
        self.m_exe_linker_path: str = \
            "C:/Program Files/Microsoft Visual Studio/2022/Enterprise/SDK/ScopeCppSDK/vc15/VC/bin/link.exe"
        self.m_response_file_name: str = "build/ExeLinkerResponseFile.rsp"
        self.m_exe_link_cmd: str = self.m_exe_linker_path + " @" + self.m_response_file_name

    @staticmethod
    def write_output_exe_file_name(response_file: TextIO, output_exe_path: Path) -> None:
        response_file.write(f'/OUT:"{output_exe_path}"\n')

    @staticmethod
    def write_obj_file_names(response_file: TextIO, obj_file_paths: list[Path]):
        for obj_file_path in obj_file_paths:
            response_file.write(f'"{obj_file_path}"\n')

    @staticmethod
    def write_standard_lib_file_names(response_file: TextIO):
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

    def generate_response_file(self, exe_link_job: ExeLinkJob) -> None:
        with open(self.m_response_file_name, "wt") as response_file:
            self.write_output_exe_file_name(response_file, exe_link_job.m_output_exe_path)
            self.write_obj_file_names(response_file, exe_link_job.m_obj_file_paths)
            self.write_standard_lib_file_names(response_file)

    def link(self, exe_link_job: ExeLinkJob) -> None:
        self.generate_response_file(exe_link_job)
        completed_process  = subprocess.run(
            self.m_exe_link_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(completed_process.stdout.decode("utf-8"))




def main():

    compile_job = CompileJob()
    compile_job.set_output_directory_path(Path("build"))
    compile_job.add_source_file_path(Path("Main.cpp"))
    compile_job.add_source_file_path(Path("StaticLibCode.cpp"))
    compile_job.add_source_file_path(Path("DllCode.cpp"))
    cpp_compiler = CppCompiler()
    cpp_compiler.compile(compile_job)

    static_librarian_job = StaticLibrarianJob()
    static_librarian_job.set_output_library_path(Path("build/StaticLib.lib"))
    static_librarian_job.add_obj_file_path(Path("build/StaticLibCode.obj"))
    static_librarian = StaticLibrarian()
    static_librarian.make_static_lib(static_librarian_job)

    dll_link_job = DllLinkJob()
    dll_link_job.set_output_dll_path(Path("build/DLL.dll"))
    dll_link_job.add_obj_file_path(Path("build/DLLCode.obj"))
    dll_linker = DllLinker()
    dll_linker.link(dll_link_job)

    exe_link_job = ExeLinkJob()
    exe_link_job.set_output_exe_path(Path("build/Main.exe"))
    exe_link_job.add_obj_file_path(Path("build/Main.obj"))
    exe_linker = ExeLinker()
    exe_linker.link(exe_link_job)


if __name__ == "__main__":
    main()
