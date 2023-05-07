import os
import sys
import copy
import hashlib


class FileHandler:
    def __init__(self, root):
        self.root = root
        self.files = {}
        self.files_chosen_format = {}
        self.duplicate_files = {}
        self.sorted_duplicate_files = {}
        self.file_format = ""
        self.sort_by = None

        # step 3/4
        self.path_size_hash_dict = {}
        self.hash_duplicate_dict = {}

        # step 4/4
        self.counter = 0
        self.dict_with_id = {}
        self.bytes_deleted = 0
        self.delete_ids = []
        self.test_dict = {}

    def add_files(self):
        for folder in os.walk(self.root):
            for file in folder[2]:
                file_path = folder[0] + "/" + file
                self.files[file_path] = os.path.getsize(file_path)

    def get_duplicates(self):
        duplicate_files = {}
        duplicate_values = []
        files_copy = copy.deepcopy(self.files_chosen_format)
        for file in files_copy:
            size = files_copy[file]
            if list(files_copy.values()).count(size) > 1 and size not in duplicate_values:
                duplicate_values.append(size)

        for size in duplicate_values:
            duplicates = []
            for file in files_copy:
                if files_copy[file] == size:
                    duplicates.append(file)
            duplicate_files[size] = duplicates
        self.duplicate_files = duplicate_files

    def get_file_format(self):
        print("Enter file format:")
        self.file_format = input("")
        print()

    def filter_files(self):
        for file in self.files.items():
            if file[0].endswith(self.file_format):
                self.files_chosen_format[file[0]] = file[1]

    def get_sort_by(self):
        print("Size sorting options:")
        print("1. Descending")
        print("2. Ascending")
        print()
        while True:
            print("Enter a sorting option:")
            option = input("")
            if option == "1":
                self.sort_by = "Descending"
                break
            elif option == "2":
                self.sort_by = "Ascending"
                break
            else:
                print()
                print("Wrong option")
                print()
                continue

    def sort_files(self):
        if self.sort_by == "Ascending":
            self.sorted_duplicate_files = dict(sorted(self.duplicate_files.items(), key=lambda item: item[0]))
        elif self.sort_by == "Descending":
            self.sorted_duplicate_files = dict(
                sorted(self.duplicate_files.items(), key=lambda item: item[0], reverse=True))

    def print_results(self):
        for size in self.sorted_duplicate_files:
            print()
            print(f"{size} bytes")
            for file in self.sorted_duplicate_files[size]:
                print(file)
        print()

    @staticmethod
    def input_for_implementation(implementation):
        valid_choices = {"yes", "no"}
        while True:
            if implementation == "duplicates":
                print("Check for duplicates?")
                choice = input("")
                print("")
            elif implementation == "delete":
                print("Delete files?")
                choice = input("")
            if choice not in valid_choices:
                print("Wrong option")
                continue
            else:
                if choice == "no":
                    exit()
                else:
                    return

    def update_dict(self):
        for item in self.sorted_duplicate_files.items():
            file_size = item[0]
            for file in item[1]:
                with open(file, "rb") as f:
                    hash_object = hashlib.md5()
                    hash_object.update(f.read())
                    hash_hex = hash_object.hexdigest()
                self.path_size_hash_dict[file] = [file_size, hash_hex]

    def check_for_duplicates(self):
        for item_1 in self.path_size_hash_dict.items():
            self.hash_duplicate_dict[(item_1[1][0], item_1[1][1])] = []
            self.hash_duplicate_dict[(item_1[1][0], item_1[1][1])].append(item_1[0])
            for item_2 in self.path_size_hash_dict.items():
                if item_1[0] != item_2[0]:
                    if item_1[1] == item_2[1]:
                        self.hash_duplicate_dict[(item_1[1][0], item_1[1][1])].append(item_2[0])
        copy_dict = copy.deepcopy(self.hash_duplicate_dict)
        for item in copy_dict.items():
            if len(item[1]) == 1:
                del self.hash_duplicate_dict[item[0]]

    def print_results_2(self):
        sizes = []
        hashes = []
        for item in self.hash_duplicate_dict.items():
            if item[0][0] not in sizes:
                print("")
                print(f"{item[0][0]} bytes")
                sizes.append(item[0][0])
            for item_2 in self.hash_duplicate_dict.items():
                if item[0][0] == item_2[0][0] and item_2[0][1] not in hashes:
                    print(f"Hash: {item_2[0][1]}")
                    hashes.append(item_2[0][1])
                    for file in item_2[1]:
                        print(f"{self.counter + 1}. {file}")
                        self.test_dict[self.counter + 1] = [file, item[0][0]]
                        self.counter += 1
        print()

    def update_dict_with_ids(self):
        counter = 1
        for item in self.hash_duplicate_dict.items():
            for path in item[1]:
                my_list = [x for x in item[0]]
                my_list.append(counter)
                my_list = tuple(my_list)
                self.dict_with_id[my_list] = path
                counter += 1

    def get_delete_ids(self):
        valid_ids = [str(i) for i in range(1, self.counter + 1)]
        while True:
            delete_ids = []
            print()
            print("Enter file numbers to delete:")
            input_ids = input("")
            delete_ids += input_ids.split()
            if not delete_ids:
                print("Wrong format")
                continue
            for file_id in delete_ids:
                if file_id not in valid_ids:
                    print("Wrong format")
                    break
            else:
                self.delete_ids += delete_ids
                break

    def file_deleter(self):
        for index in self.delete_ids:
            for item in self.dict_with_id.items():
                if int(index) == int(item[0][2]):
                    self.bytes_deleted += item[0][0]
                    os.remove(item[1])
        print()
        print(f"Total freed up space: {self.bytes_deleted} bytes")


def main():
    try:
        root = sys.argv[1]
    except IndexError:
        print("Directory is not specified")
        sys.exit()
    program = FileHandler(root)
    program.add_files()
    program.get_file_format()
    program.filter_files()
    program.get_sort_by()
    program.get_duplicates()
    program.sort_files()
    program.print_results()

    # step 3/4 starts here
    program.update_dict()
    program.input_for_implementation("duplicates")
    program.check_for_duplicates()
    program.print_results_2()

    # step 4/4

    # theodor
    program.input_for_implementation("delete")
    program.get_delete_ids()
    # lukas
    program.update_dict_with_ids()
    program.file_deleter()

    #print(program.test_dict)

if __name__ == "__main__":
    main()
