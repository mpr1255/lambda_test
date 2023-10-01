#%%
import sys
import hashlib
import  exiftool
import os
import subprocess
import yaml
from PIL import Image
# from tika import parser
import pytesseract
import magic
import json

# Function to hash a file
def hash_file(file):
    sha1 = hashlib.sha1()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1.update(byte_block)
    return sha1.hexdigest()

# Function to get metadata of a file
def get_metadata(file):
    try:
        with exiftool.ExifToolHelper() as et:
            result = et.get_metadata(file)
            print(result)
    except Exception as e:
        print(f"Error occurred while getting metadata: {str(e)}")
        return None, None

    try:
        for i, d in enumerate(result):
            for key, value in d.items():
                if isinstance(value, bytes):
                    try:
                        result[i][key] = value.decode('utf-8')
                    except UnicodeDecodeError:
                        result[i][key] = value.decode('utf-8', 'replace')
    except Exception as e:
        print(f"Error occurred while decoding bytes: {str(e)}")

    # Extract key-value pairs into a new dictionary
    metadata_dict = {}
    for item in result:
            for key, value in item.items():
                    metadata_dict[key] = value

        # Print the resulting dictionary
    try:
        sha1 = hash_file(file)
    except:
        sha1 = "Hashing error"
   
    first_create_date = next((key for key in metadata_dict.keys() if "CreateDate" in key), None)
    create_date = metadata_dict.get(first_create_date) if first_create_date else None

    doc_dict = {
        'sha1': sha1,
        'filename_exif': metadata_dict.get("File:FileName", ""),
        'extension_exif': metadata_dict.get("File:FileTypeExtension", ""),
        'last_modified_exif': metadata_dict.get("File:FileModifyDate", ""),
        'create_date_exif': create_date,
        'access_date_exif': metadata_dict.get("File:FileAccessDate", ""),
        'modify_date_exif': metadata_dict.get("File:FileModifyDate", ""),
        'mime_type_exif': metadata_dict.get("File:MIMEType", ""),
        'file_size_exif':  metadata_dict.get("File:FileSize", ""),
        'title_exif': metadata_dict.get("Title", ""),  
        'path_components_exif' : metadata_dict.get("SourceFile", "").split("/")[1:-1],
        'publication_date_exif': metadata_dict.get("Publication Date", ""),  
        'author_exif': metadata_dict.get("Author", ""),  
        'organizational_unit_exif': metadata_dict.get("Organizational Unit", ""), 
        'content': '',  
    }

    return doc_dict, metadata_dict
    

# Function to get content of a file
def get_content(file, mime_type_exif):
    print(file, mime_type_exif)
    content = ""
    try:
        if mime_type_exif in ["image/jpeg", "image/png", "image/bmp", "image/tiff", "image/gif"]:
            content = subprocess.run(["tesseract", file, "stdout", "-l", "chi_sim"], capture_output=True, text = True)
            content = content.stdout
            return content
        elif mime_type_exif in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            print("Not doing excel for now.")
            pass
        elif mime_type_exif in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/csv", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.ms-powerpoint", "application/pdf", "text/html", "application/xhtml+xml", "text/plain", "application/msword"]:
            raw = parser.from_file(file)
            return raw['content']
        else:
            print(f"Unsupported file type: {mime_type_exif}")
    except Exception as e:
        print(f"Error occurred while processing file: {file}. Error message: {str(e)}")
    return

def list_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for name in files:
            file_paths.append(os.path.join(root, name))
    return file_paths
#%%

if __name__ == "__main__":
    dir = "./data"  # Replace with your directory

    
    files = list_files(dir)
    # files = [f for f in files if hash_file(f) not in existing_hashes]
    
    for file in files:
        print(file)

        doc_dict, exif_full_dict = get_metadata(file)
        if doc_dict is not None:        
            try:
                # doc_dict['content'] = get_content(file, doc_dict['mime_type_exif'])
                with open(f"./out/{doc_dict['sha1']}.json", "w") as f:
                    json.dump(doc_dict, f)
                with open(f"./out/{doc_dict['sha1']}_exif.json", "w") as f:
                    json.dump(exif_full_dict, f)
            except:
                pass
        # insert_data(table_name, doc_dict, indexApi)

        # content = get_content(file)
        # print(content)




# %%
