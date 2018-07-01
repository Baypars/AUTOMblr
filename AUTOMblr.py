import os
import pytumblr
import random

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    '<consumer_key>',
    '<consumer_secret>',
    '<oauth_token>',
    '<oauth_secret>'
)

# Make the request
# client.info()

runway_path = os.path.abspath(r"C:\Users\You\Directory")


# returns a path to a folder which has un-posted content
def find_folder():
    # find items in the directory that are only folders
    runway_dirs = [x for x in os.listdir(runway_path) if os.path.isdir(os.path.join(runway_path, x))]
    rtn_dir_index = random.randint(0, len(runway_dirs) - 1)
    rtn_dir = os.path.basename(runway_dirs[rtn_dir_index])

    # check if everything has already been posted
    posted_dir = 0
    for some_dir in runway_dirs:
        if some_dir[:7] == 'POSTED-':
            posted_dir += 1
    if posted_dir == len(runway_dirs):
        return 'NO NEW FOLDERS FOR UPLOADING'

    # from folders find folders that have un-posted content
    while rtn_dir[:7] == "POSTED-":
        rtn_dir_index = random.randint(0, len(runway_dirs) - 1)
        rtn_dir = os.path.basename(runway_dirs[rtn_dir_index])

    return os.path.join(runway_path, rtn_dir)


# returns a list of image paths
def find_images(posting_dir):
    image_paths = []
    for file_path in os.listdir(posting_dir):
        file_name, file_ext = os.path.splitext(file_path)
        if file_ext == '.jpg' or file_ext == '.png':
            if file_name[:7] != 'POSTED-':
                image_paths.append(os.path.join(runway_path, posting_dir, file_path))

                if len(image_paths) == 4:
                    return image_paths

    return []


# posts the images found in the path to Tumblr
def post_image(posting_dir, image_paths):
    errors_while_posting = []
    tags = os.path.basename(posting_dir).split(' ')
    tags.append('Fashion')
    caption = ' '.join(tags)
    tags += ['Fashion', 'Runway', 'Clothes', 'Apparel']

    for path in image_paths:
        print('posting:', path)
        response = client.create_photo('yourblog', state="published", tags=tags, caption=caption, data=path)

        if response['state'] != 'published':
            errors_while_posting.append(path)

    return errors_while_posting


# change the names of files we just posted
def change_image_names(image_paths):
    for path in image_paths:
        new_name = os.path.join(os.path.dirname(path), "POSTED-" + os.path.basename(path))
        os.rename(path, new_name)


# change the name of the folder if necessary
def change_folder_name(dir_name):
    image_file_paths = [x for x in os.listdir(dir_name) if os.path.splitext(x)[1] == '.jpg' or os.path.splitext(x)[1] == '.png']

    posted_amount = 0
    for file_name in image_file_paths:
        if file_name[0:7] == 'POSTED-':
            posted_amount += 1

    if posted_amount == len(image_file_paths):
        os.rename(dir_name, os.path.join(runway_path, 'POSTED-' + os.path.basename(dir_name)))


def main():
    print('Finding a directory')
    posting_dir = find_folder()
    if posting_dir == 'NO NEW FOLDERS FOR UPLOADING':
        print('NO NEW FOLDERS FOR UPLOADING')
        return

    print('Finding images')
    image_paths = find_images(posting_dir)
    if image_paths == []:
        print("NOT ENOUGH IMAGES IN DIRECTORY", posting_dir)
        return

    print('Posting images')
    errors_with_uploads = post_image(posting_dir, image_paths)
    if errors_with_uploads != []:
        print("Errors while posting: ", errors_with_uploads)
        return

    print('Finishing up task')
    change_image_names(image_paths)
    change_folder_name(posting_dir)

    print('POSTING SUCCESSFUL')


if __name__ == '__main__':
    main()
