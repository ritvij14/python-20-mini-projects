import os
import shutil
import pathlib


def organize_files():
    path = input("Enter the path to the directory you want to organize: ")
    if not os.path.exists(path) or not os.path.isdir(path):
        print("Path does not exist")
        return
    file_types = {
        "Images": [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".tiff", ".ico"],
        "Documents": [
            ".pdf",
            ".doc",
            ".docx",
            ".txt",
            ".rtf",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
        ],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma"],
        "Video": [".mp4", ".mov", ".wmv", ".avi", ".mkv", ".flv", ".webm"],
        "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Executable": [".exe", ".msi"],
        "Code": [
            ".py",
            ".java",
            ".cpp",
            ".c",
            ".html",
            ".css",
            ".js",
            ".php",
            ".sql",
            ".xml",
        ],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot", ".svg"],
    }

    file_moved_count = 0
    for item in os.scandir(path):
        if item.is_file():
            ext = pathlib.Path(item).suffix.lower()
            for folder, exts in file_types.items():
                if ext in exts:
                    print(f"Moving {item.name} to {folder} folder")
                    folder_path = os.path.join(path, folder)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    shutil.move(item.path, os.path.join(folder_path, item.name))
                    file_moved_count += 1
                    break
                else:
                    print(f"No folder found for {item.name}")
    print(f"\n\nTotal {file_moved_count} files moved")


if __name__ == "__main__":
    try:
        organize_files()
    except Exception as e:
        print(f"An error occurred: {e}")
