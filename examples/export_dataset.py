import os
import shutil

if __name__ == "__main__":
    root = "/Users/wgj/SPECTRE/skyfall"
    target = "/Users/wgj/SPECTRE/spectre-public"
    folders = [os.path.join(root, f) for f in os.listdir(root) if not f.startswith(".")]

    for folder in folders:
        if not folder.endswith("reference"):
            raw_meas_name = os.path.split(folder)[-1].split("_")[-1]  # Extract measurement id
            target_directory = os.path.join(target, raw_meas_name)
            try:
                os.mkdir(target_directory)
            except FileExistsError:
                pass  # Folder already existing

            for f in os.listdir(folder):
                if "raw_frame" in f or "spectrum" in f:
                    f_new = f.replace("raw_", "")
                    shutil.copyfile(os.path.join(folder, f), os.path.join(target_directory, f_new))
