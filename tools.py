import os
from dotenv import load_dotenv, find_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv(find_dotenv())

def authenticate_to_cloudinary():
  cloudinary.config( 
    cloud_name = os.environ.get("CLOUD_NAME"), 
    api_key = os.environ.get("API_KEY"),
    api_secret = os.environ.get("API_SECRET") 
  )
  print('Cloud Name:', os.environ.get("CLOUD_NAME"))


def upload_files_from_folder(folder_path, exts, cloudinary_folder, tags):
  print("Upload folder:", folder_path)
  for f in os.listdir(folder_path):
    if assert_file_extension(f, exts):
      file_path = os.path.join(folder_path, f)
      public_id = os.path.splitext(f)[0]
      upload_file(file_path, cloudinary_folder, public_id, tags)

def assert_file_extension(f, exts):
  res = False
  for ext in exts:
    if f.endswith(ext):
      res = True
      break
  return res

def upload_file(file_path, folder, public_id, tags):
  # https://cloudinary.com/documentation/django_integration
  print("--Upload----\nfile_path: {}\nfolder: {}\npublic_id: {}".format(file_path, folder, public_id))
  cloudinary.uploader.upload(file_path, 
    folder=folder,                      # folder name (auto create)
    public_id=public_id,                # Don't include extension. Cloudinary will add it.
    resource_type='auto',
    tags=tags                           # str list. Useful to create client assets list
    )

def delete_file(public_id):
  # public_id == folder/folder/id (without extension)
  res = cloudinary.uploader.destroy(public_id)
  print('delete: {}\n\t{}'.format(public_id, res))

def create_client_assets_list(tag):
  # Deactivated by default. Go in Security, Restricted media types, uncheck Resource list
  # Creates a list of files accessible without authentication for the client
  json_name = '{}.json'.format(tag)
  res = cloudinary.utils.cloudinary_url(json_name, type='list')
  print('Client assets list:', res)
  return res

