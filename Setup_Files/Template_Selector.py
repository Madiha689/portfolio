import os
import shutil
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
DEFAULT_EXCLUDE_ENTRIES = {
    "css",
    "js",
    "assets",
    "Setup_Files",
    "_site",
    ".jekyll-cache",
    "_config.yml",
    "Localhost_Setup",
}
ROOT_DIR = "../"


def cleanup_minimalist_css_folder(folder_name):
    """
    🎯 Moves contents of 'Minimalist_Professional/css' to root 'css' folder
    without deleting root. Then deletes the original internal 'css' folder.
    """
    css_path = os.path.join(ROOT_DIR, folder_name, "css")
    root_css_dest = os.path.join(ROOT_DIR, "css")

    print(f"{Fore.MAGENTA}🔍 DEBUG: css_path = {css_path}")
    print(f"{Fore.MAGENTA}🔍 DEBUG: root_css_dest = {root_css_dest}")

    if os.path.isdir(css_path):
        try:
            # Ensure root css exists
            os.makedirs(root_css_dest, exist_ok=True)

            # Move files and folders inside internal css to root css
            for item in os.listdir(css_path):
                src = os.path.join(css_path, item)
                dst = os.path.join(root_css_dest, item)

                if os.path.exists(dst):
                    # Remove if file/folder already exists at destination
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)

                shutil.move(src, dst)
                print(f"{Fore.CYAN}📦 Moved: {item}")

            # Delete the now-empty internal css folder
            folder_path = os.path.join(ROOT_DIR, folder_name)
            shutil.rmtree(folder_path)
            print(f"{Fore.RED}🗑️ Deleted original {folder_name} folder")

        except Exception as e:
            print(f"{Fore.RED}⚠️ Failed to move css contents: {e}")
    else:
        print(f"{Fore.YELLOW}⚠️ No css folder found at: {css_path}")


def print_banner(text):
    banner = pyfiglet.figlet_format(text)
    width = os.get_terminal_size().columns
    for line in banner.split("\n"):
        print(Fore.CYAN + line.center(width))


def display_selected_ascii(template_name):
    prefixes_to_remove = ["Minimalist_Professional_", "Minimalist_Professional"]
    display_name = template_name
    for prefix in prefixes_to_remove:
        if display_name.startswith(prefix):
            display_name = display_name[len(prefix) :]
            break
    display_name = display_name.replace("_", " ").strip().title()

    ascii_art = pyfiglet.figlet_format(display_name)
    width = os.get_terminal_size().columns
    print("\n" + Fore.MAGENTA + "=" * width)
    for line in ascii_art.split("\n"):
        print(Fore.GREEN + line.center(width))
    print(Fore.MAGENTA + "=" * width + "\n")


def get_valid_folders(path):
    return [
        f
        for f in os.listdir(path)
        if os.path.isdir(os.path.join(path, f)) and f not in DEFAULT_EXCLUDE_ENTRIES
    ]


def print_numbered_folders(folders):
    for idx, folder in enumerate(folders, 1):
        print(f"{Fore.YELLOW}{idx}. {Fore.GREEN}{folder}")


def clean_folders(path, keep, extra_preserve=set()):
    preserve_all = DEFAULT_EXCLUDE_ENTRIES.union(extra_preserve)
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if item == keep or item in preserve_all:
            print(f"{Fore.GREEN}✅ Kept: {item}")
            continue

        try:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
                print(f"{Fore.RED}🗑️ Deleted folder: {item}")
            else:
                os.remove(full_path)
                print(f"{Fore.RED}🗑️ Deleted file: {item}")
        except Exception as e:
            print(f"{Fore.RED}⚠️ Could not delete {item}: {e}")


def move_contents_to_root(selected_path, final_name):
    display_selected_ascii(final_name)

    try:
        for dirpath, dirnames, filenames in os.walk(selected_path):
            rel_path = os.path.relpath(dirpath, selected_path)
            target_dir = (
                os.path.join(ROOT_DIR, rel_path) if rel_path != "." else ROOT_DIR
            )
            os.makedirs(target_dir, exist_ok=True)

            for file in filenames:
                src_file = os.path.join(dirpath, file)
                dst_file = os.path.join(target_dir, file)

                if os.path.exists(dst_file):
                    os.remove(dst_file)
                    print(f"{Fore.YELLOW}♻️ Overwriting: {file}")

                shutil.move(src_file, dst_file)
                print(f"{Fore.CYAN}📦 Moved file: {file}")

        # Remove only sibling folders inside base template dir (not css/js/assets)
        base_template_dir = (
            os.path.dirname(selected_path)
            if os.path.basename(selected_path) == final_name
            else selected_path
        )

        if os.path.basename(selected_path) != final_name:
            if os.path.exists(base_template_dir) and os.path.isdir(base_template_dir):
                print(
                    f"\n{Fore.MAGENTA}🧹 Cleaning up: {os.path.basename(base_template_dir)}"
                )
                for item in os.listdir(base_template_dir):
                    item_path = os.path.join(base_template_dir, item)
                    if item in DEFAULT_EXCLUDE_ENTRIES or item == final_name:
                        print(f"{Fore.GREEN}✅ Preserved: {item}")
                        continue
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            print(f"{Fore.RED}🗑️ Deleted folder: {item}")
                        else:
                            os.remove(item_path)
                            print(f"{Fore.RED}🗑️ Deleted file: {item}")
                    except Exception as e:
                        print(f"{Fore.RED}⚠️ Could not delete {item}: {e}")
        else:
            # If it's a top-level template, remove entire folder
            if os.path.exists(selected_path) and os.path.isdir(selected_path):
                shutil.rmtree(selected_path)
                print(f"{Fore.BLUE}🧹 Removed folder: {final_name}")

    except Exception as e:
        print(f"{Fore.RED}⚠️ Failed during move: {e}")


def get_user_preserve_list():
    response = input(
        f"{Fore.YELLOW}📝 Enter comma-separated files/folders to preserve (or press Enter to skip):\n> "
    ).strip()
    return (
        {item.strip() for item in response.split(",") if item.strip()}
        if response
        else set()
    )


def main():
    print_banner("Portfolio Template Picker")

    top_templates = get_valid_folders(ROOT_DIR)
    if not top_templates:
        print(Fore.RED + "❌ No valid templates found.")
        return

    print(f"{Fore.MAGENTA}\n✨ Available Portfolio Templates:")
    print_numbered_folders(top_templates)

    try:
        choice = (
            int(
                input(f"\n{Fore.YELLOW}🔢 Enter your choice (1-{len(top_templates)}): ")
            )
            - 1
        )
        if not (0 <= choice < len(top_templates)):
            raise ValueError
    except ValueError:
        print(Fore.RED + "❌ Invalid selection.")
        return

    selected_template = top_templates[choice]
    selected_path = os.path.join(ROOT_DIR, selected_template)
    final_selection = selected_template
    final_path = selected_path

    # Allow additional preservation
    extra_preserve = get_user_preserve_list()

    # Handle Minimalist_Professional sub-template selection
    if selected_template == "Minimalist_Professional":
        subfolders = get_valid_folders(selected_path)
        if subfolders:
            print(f"\n{Fore.BLUE}📂 Sub-templates inside Minimalist_Professional:")
            print_numbered_folders(subfolders)
            try:
                sub_choice = (
                    int(
                        input(
                            f"\n{Fore.YELLOW}🔢 Enter sub-template choice (1-{len(subfolders)}): "
                        )
                    )
                    - 1
                )
                if not (0 <= sub_choice < len(subfolders)):
                    raise ValueError
            except ValueError:
                print(Fore.RED + "❌ Invalid sub-template selection.")
                return

            final_selection = subfolders[sub_choice]
            final_path = os.path.join(selected_path, final_selection)

            print(f"\n{Fore.MAGENTA}🧹 Cleaning sibling sub-templates...")
            for folder in subfolders:
                if folder != final_selection:
                    folder_path = os.path.join(selected_path, folder)
                    if folder in DEFAULT_EXCLUDE_ENTRIES:
                        print(f"{Fore.GREEN}✅ Preserved system folder: {folder}")
                        continue
                    try:
                        shutil.rmtree(folder_path)
                        print(f"{Fore.RED}🗑️ Deleted: {folder}")
                    except Exception as e:
                        print(f"{Fore.RED}⚠️ Could not delete {folder}: {e}")
            print(f"{Fore.GREEN}✅ Kept: {final_selection}")
        else:
            print(Fore.YELLOW + "⚠️ No subfolders to select.")

    print(f"\n{Fore.MAGENTA}🧹 Cleaning other templates...")
    clean_folders(ROOT_DIR, selected_template, extra_preserve)

    move_contents_to_root(final_path, final_selection)

    if selected_template == "Minimalist_Professional":
        cleanup_minimalist_css_folder(selected_template)

    print(
        f"\n{Fore.GREEN}🎉 Setup complete! Your selected template is: {final_selection}"
    )


if __name__ == "__main__":
    main()
