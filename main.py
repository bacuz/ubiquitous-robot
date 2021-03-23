import os


def header():
    print("----------------------------------------")
    print("|                                      |")
    print("|                                      |")
    print("|      Antenna File Formatter v01      |")
    print("|                                      |")
    print("|                                      |")
    print("----------------------------------------")


def user_loop():
    while True:
        print('Available actions:')
        print('* [c]heck a folder')
        print('* e[x]it')
        print()
        ch = input(": ").strip().lower()
        if ch == 'c':
            check_files()
        elif not ch or ch == 'x':
            print('Goodbye')
            break


def check_files():
    root = input("Enter the folder route: ")
    models = set()
    freqs = set()
    ports = set()
    polarizations = set()
    antennas = set()

    folders = [folder for folder in os.listdir(root) if os.path.isdir(root + "/" + folder)]
    masks = [mask for mask in os.listdir(root) if os.path.isfile(root + "/" + mask)]

    for mask in masks:
        element = mask.split("_")
        if len(element) > 1:
            models.add(element[0])
            freqs.add(element[1])
            ports.add(element[-1].split('.')[0])
            polarizations.add(element[-3])

    files = dict()

    for mask in masks:
        for model in models:
            for freq in freqs:
                for port in ports:
                    for polarization in polarizations:
                        antennas.add(model + "_" + freq + "_X_CO_" + polarization + "_" + port)
                        key = model + "_" + freq + "_X_CO_" + polarization + "_" + port
                        if key not in files:
                            files[key] = list()
                        if model in mask and freq in mask and port in mask and polarization in mask:
                            files[key].append(mask)

    keys = list(files)
    for key in keys:
        if len(files[key]) == 0:
            files.pop(key)

    keys = list(files)
    for key in keys:
        ftilt = files[key][0].split("_")[-2]
        ltilt = files[key][-1].split("_")[-2]
        element = key.split("_")
        new_folder = (element[0] + "_" + element[1] + "_" +
                      element[2] + "_" + element[3] + "_" +
                      element[4] + "_" + ftilt + "_" + ltilt + "_" +
                      element[5])
        files[new_folder] = files.pop(key)

    print(folders)
    keys = list(files)
    for key in keys:
        if key not in folders:
            os.mkdir(root+"\\"+key)
            print(f"{key}, is created in route {root}/{key}")
            for file in files[key]:
                os.rename(root + "\\" + file, root + "\\" + key + "\\" + file)

    print("Ready")


if __name__ == '__main__':
    header()
    user_loop()
