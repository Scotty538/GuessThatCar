import requests
import random
import re
import sys
import os
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from PIL import Image, ImageDraw

# Constants
CAR_IMAGES_FOLDER = "car_images"
TEST_FOLDER = "car_images_test"
MYSTERY_IMAGE = "MysteryCar.png"
SQUARE_SIZE = 200 


def scrape_images(url):
    """Scrape appropriately labelled 1024w images from a previously researched website"""
    
    print("The programme is contacting the relevant website and will begin downloadng images shortly.\nThis will take approximately 10 seconds. Please be patient.")
    # Send a request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    image_tags = soup.find_all('img')

    # Create folders for images and test image
    os.makedirs(CAR_IMAGES_FOLDER, exist_ok=True)
    os.makedirs(TEST_FOLDER, exist_ok=True)

    # Regex to extract 1024w from srcset
    pattern = r"(\S+)\s(\d+)w"

    # Download and name images using the alt text
    for index, img_tag in enumerate(image_tags):
        srcset = img_tag.get('srcset')
        img_url = None

        # If srcset exists, look for 1024w
        if srcset:
            matches = re.findall(pattern, srcset)
            for match in matches:
                url, width = match
                if width == "1024":
                    img_url = url
                    break  # Use the first match for 1024w

        # Obtain alt text
        alt_text = img_tag.get('alt', '').strip()
        
        if not alt_text:
            alt_text = f"image_{index + 1}"  # Name to use if alt text is missing
        
        # Make the alt_text safe for filenames
        safe_alt_text = "".join(c if c.isalnum() or c in " _-" else "_" for c in alt_text)

        try:
            # Screen by name to filter out undesirable/irrelevant images 
            if ("The " not in safe_alt_text) and ("A " not in safe_alt_text) and ("image" not in safe_alt_text) and ("Supra" not in safe_alt_text) and ("Charles" not in safe_alt_text) and ("Essex" not in safe_alt_text): 
                
                # Fetch and process the image
                img_response = requests.get(img_url)
                img = Image.open(BytesIO(img_response.content))
            
                img_name = CAR_IMAGES_FOLDER + f"/{safe_alt_text}.jpg"
                img.save(img_name)
                if safe_alt_text == "Nissan Skyline GT-R":
                    img.save(TEST_FOLDER + f"/{safe_alt_text}.jpg")

        except Exception:
            # Debugging
            # print(f"Failed to process {img_url}")
            pass

    return "Image downloading and naming completed!"


# Helper function to assist in testing scrape_images
def count_images(folder):
    """Counts the number of files in the designated folder."""
    
    image_count = 0
    for _ in os.listdir(folder):
            image_count += 1
    return image_count


def random_pic(designated_folder):
    """Randomly select an image from the downloaded folder of car images."""

    # List all images in the folder
    images = os.listdir(designated_folder)

    # Select a random image file
    if not images:
        print("No images found in the folder.")
        return

    return random.choice(images)


def guess(folder_name_cars,chosen_pic):
    """Provide user 5 chances to guess the car brand, revealing another square for each incorrect guess."""
    # Create an empty list for locations_of_transparent_squares
    locations_of_transparent_squares = []
    tries = 0
    # Extract make and model from filename to use when revealing answer
    match = re.match(r"^[\d+ ]*([\w]+ [\w]+)", chosen_pic)

    while(tries < 5):
        try:
            mystery_car = Image.open(os.path.join(folder_name_cars, chosen_pic))
        
        except FileNotFoundError:
            sys.exit("Image does not exist")
        
        else:
            # Create an image for the mask (same size as the designated car image)
            mask = Image.new("RGBA", mystery_car.size, (0, 0, 0, 255))  # RGBA for transparency
            w, h = mystery_car.size
            # Define the size and position of the transparent square
            top_left = (random.randint(1, w - SQUARE_SIZE),random.randint(1, h - SQUARE_SIZE))  # Position of the top-left corner of the square
            bottom_right = (top_left[0] + SQUARE_SIZE, top_left[1] + SQUARE_SIZE)
            locations_of_transparent_squares.append((top_left,bottom_right))
            # Create a draw object and add relevant number of transparent squares
            draw = ImageDraw.Draw(mask)
            for i in locations_of_transparent_squares:
                draw.rectangle([i[0], i[1]], fill=(0, 0, 0, 0))  # (0, 0, 0, 0) for fully transparent

            # Paste the mask onto the original image (using the mask as an alpha channel) and save
            image_with_mask = Image.alpha_composite(mystery_car.convert("RGBA"), mask)
            image_with_mask.save(MYSTERY_IMAGE)
        
        guess = input("What is the make/model of the car in the image?: ").lower()

        # My son found cheats such as single letters/spaces which produced correct answers
        while guess == " " or guess == "" or len(guess) < 3:
            guess = input("Please enter a valid guess: ")

        if guess in chosen_pic.lower():
            #print("Great work! You are correct! The car was a " + match.group(1) + ".\nYou are a walking encyclopedia of car brands!")
            # Reveal complete image
            mystery_car = Image.open(os.path.join(CAR_IMAGES_FOLDER, chosen_pic))
            mystery_car.save(MYSTERY_IMAGE)
            sys.exit("Great work! You are correct! The car was a " + match.group(1) + ".\nYou are a walking encyclopedia of car brands!")
        else:
            print("Not a bad guess, but, unfortunately, incorrect.\nPlease try again.")
            tries += 1

    # Reveal complete image
    mystery_car = Image.open(os.path.join(CAR_IMAGES_FOLDER, chosen_pic))
    mystery_car.save(MYSTERY_IMAGE)
    sys.exit("Your five attempts are up. The car was a " + match.group(1) + ".\nBetter luck next time.")
            

def main():        
    url = "https://robbreport.com/motors/cars/lists/the-50-greatest-sports-cars-of-all-time-1235871704/"

    # Call scrape_images to download images only if folder of car images does not already exist
    if os.path.isdir(CAR_IMAGES_FOLDER):
        print("Lucky you! The folder of car images already exists.")
    else:
        print(scrape_images(url))
        
    chosen_pic = random_pic(CAR_IMAGES_FOLDER)

    guess(CAR_IMAGES_FOLDER, chosen_pic)

if __name__ == "__main__":
    main()
