import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_files():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        if ".git" in root or ".venv" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                modified = False

                # Replace single-quoted page_path
                target_sq = "'page_path': window.location.pathname + window.location.search"
                replacement_sq = "'page_path': '/' + window.location.hostname + window.location.pathname + window.location.search"
                if target_sq in content:
                    content = content.replace(target_sq, replacement_sq)
                    modified = True

                # Replace double-quoted page_path
                target_dq = 'page_path: window.location.pathname + window.location.search'
                replacement_dq = 'page_path: "/" + window.location.hostname + window.location.pathname + window.location.search'
                if target_dq in content:
                    content = content.replace(target_dq, replacement_dq)
                    modified = True

                if modified:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Fixed page_path in: {os.path.relpath(file_path, ROOT_DIR)}")
                    count += 1

    print(f"\nCompleted! Updated {count} HTML files in Gunnarguy-Portfolio.")

if __name__ == "__main__":
    fix_files()
