import os
import stat

def get_permissions(path):
    try:
        st = os.stat(path)
        mode = st.st_mode
        perms = stat.filemode(mode)
        return perms
    except OSError as e:
        return f"Error: {e}"

def scan_directory(dir_path):
    files_with_exec = []
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            path = os.path.join(root, name)
            perms = get_permissions(path)
            if not perms.startswith("Error") and perms[-1] == 'x':
                print(f"{perms} {path}")
                files_with_exec.append(path)
    return files_with_exec

if __name__ == "__main__":
    dir_path = input("Enter the directory path to scan: ")
    if os.path.isdir(dir_path):
        files_with_exec = scan_directory(dir_path)
        if files_with_exec:
            choice = input("Do you want to remove execute permissions for others on these files? (y/n): ").strip().lower()
            if choice == 'y':
                for path in files_with_exec:
                    try:
                        current_mode = os.stat(path).st_mode
                        new_mode = current_mode & ~0o001
                        os.chmod(path, new_mode)
                        new_perms = get_permissions(path)
                        print(f"Successfully removed execute permission for others on {path}. New permissions: {new_perms}")
                    except OSError as e:
                        print(f"Error modifying {path}: {e}")
    else:
        print("Invalid directory path.")