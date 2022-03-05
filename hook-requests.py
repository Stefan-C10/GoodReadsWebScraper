print("Custom hook for requsts")
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files
hiddenimports = collect_submodules('requests')

datas = collect_data_files('requests')