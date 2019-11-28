####### Input a URL and this script will download all the Images related to the product and store it in a folder containing the same name of the product #######


# Importing Regex and HTTP Requests
import os
import re
import requests
import csv
import chardet

exists = False
while exists == False:
    list_file = input("Enter CSV filename: ")
    if os.path.exists(f'./{list_file}.csv'):
        exists = True
    else:
        print("CSV file does not exist in script directory. Please try again.")

# with open('test.csv', 'r', encoding='utf-8') as csv_file:
encodings = ['utf-8', 'ansi', 'utf-16']
for enc in encodings:
    try:
        with open(f'{list_file}.csv', 'r', encoding=enc) as csv_file:
            csv_reader = csv.reader(csv_file)

            # Check if downloads folder exists. Create if not
            if not os.path.isdir('downloads'):
                os.mkdir('downloads')
            os.chdir('downloads')

            print(
                'It will take few minutes, please be patient... \nOr press [Ctrl+C] to quit...')
            lists = []

            for line in csv_reader:
                lists.append(line)

            urls = lists[1:]
            for csv_url in urls:
                url = csv_url[0]

                # Getting the product name
                product = url.split('/')[-1]

                # Create a directory and hit into it
                filename = product
                if not os.path.isdir(filename):
                    os.mkdir(filename)
                os.chdir(filename)

                # Getting response
                response = requests.get(url)

                # Getting the source code
                source_code = response.text

                # RegEx pattern for getting images URL
                pattern = re.compile(
                    r'([\:\/\.\-\w]+)\/([\-\_\w]+)\.(jpg|png)(?=[\"\'])')
                matches = pattern.findall(source_code)

                # List for Unique names along with URLs
                unique_names = []
                unique_urls = []

                # Sorting Unique Image names and URLs in the List
                for match in matches:
                    # tuple destructuring
                    (url, name, extension) = match
                    if name in unique_names:
                        pass
                    elif name.startswith(product):
                        unique_names.append(name)
                        unique_urls.append(match)

                # Iterate every product and download it according to the name
                for similar_url in unique_urls:
                    # tuple destructuring
                    (image_url, image_name, image_extension) = similar_url
                    # Getting the Image response
                    image_request = requests.get(
                        image_url + '/' + image_name + '.' + image_extension)
                    # Saving the image
                    with open(f'{image_name}.{image_extension}', 'wb') as image:
                        image.write(image_request.content)
                print(f'successfully download images for {product}')
                os.chdir('../')
        break
    except UnicodeDecodeError as e:
        os.chdir('../')
        continue
