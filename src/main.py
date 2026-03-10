from textnode import *
from htmlnode import *
from process_functions import *
from blocks import *
import os, shutil
from constants import *
import sys

def main():
    if sys.argv != "":
        basepath = "./"
    else:
        basepath = sys.argv[0]
    copy_site_content_to(PUBLIC_DIRECTORY)
    generate_pages_recursive(basepath, SITE_PAGES, "./template.html", PUBLIC_DIRECTORY)

def generate_site_map(content_folder): #incomplete
    if os.path.exists(content_folder):
        site_map = os.listdir(content_folder)

    else:
        os.mkdir(content_folder)
        raise Exception(f"No site pages exist in {content_folder}")

def delete_folder_content(directory_path, content_list):
    if len(content_list) > 0:
        for content in content_list:
            content_path = os.path.join(directory_path, content)
            if os.path.isfile(content_path):
                print(f"Deleted file: {content_path}")
                os.remove(content_path)
            else:
                 delete_folder_content(content_path, os.listdir(content_path))
                 os.rmdir(content_path)

def copy_folder_content(from_directory, content_list, to_directory):
    for content in content_list:
        content_path = os.path.join(from_directory, content)
        if os.path.isfile(content_path):
            shutil.copy(content_path, to_directory)
            print(f"Copied: {content_path} to {to_directory}")
        else:
            new_directory = os.path.join(to_directory, content)
            os.mkdir(new_directory)
            new_content = os.listdir(content_path)
            copy_folder_content(content_path, new_content, new_directory)

def copy_site_content_to(final_directory_path):
    if os.path.exists(final_directory_path):
        contents = os.listdir(final_directory_path)
        if len(contents) > 0:
             delete_folder_content(final_directory_path, contents)
    else:
        os.mkdir(final_directory_path)
    copy_folder_content(SITE_CONTENT, os.listdir(SITE_CONTENT), PUBLIC_DIRECTORY)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        path = os.path.join(dir_path_content, item)
        new_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(path):
            print(f"Generating page from {path} to {dest_dir_path} using {template_path}")
            with open(path, "r") as file:
                content = file.read()
            with open(template_path, "r") as file:
                template = file.read()
            html_string = markdown_to_html_node(content).to_html()
            page_title = extract_title(content)
            updated_template = template.replace("{{ Title }}", page_title)
            updated_template = updated_template.replace("{{ Content }}", html_string)
            updated_template = updated_template.replace('href="/', 'href="{basepath}')
            updated_template = updated_template.replace('src="/', 'src="{basepath}')
            new_path = new_path.replace(".md", ".html")
            with open(new_path, "w") as file:
                file.write(updated_template)
        else:
            if os.path.exists(new_path) == False:
                os.mkdir(new_path)
            generate_pages_recursive(basepath, path, template_path, new_path)

if __name__ == "__main__":
    main()